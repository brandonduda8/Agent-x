"""
core/llm_client.py — LLM Provider Fallback Chain

Supports an ordered list of LLM providers defined in config/settings.yaml.
On a non-2xx response, timeout, or any provider error the client automatically
tries the next provider in the chain and logs each fallback event to
memory/brain.json so the rest of the system has a full audit trail.

Supported provider types
------------------------
openrouter  — OpenRouter.ai proxy (OpenAI-compatible endpoint)
openai      — Direct OpenAI API
anthropic   — Anthropic Messages API
ollama      — Local Ollama instance (OpenAI-compatible /api/chat)
huggingface — Local HuggingFace transformers pipeline (CPU/GPU, no network)

config/settings.yaml schema (llm section)
------------------------------------------
llm:
  timeout: 120          # seconds per provider attempt (optional, default 120)
  providers:
    - name: openrouter
      model: openai/gpt-4o-mini
      base_url: https://openrouter.ai/api/v1
      api_key_env: OPENROUTER_API_KEY   # env-var name that holds the key
    - name: anthropic
      model: claude-3-haiku-20240307
      base_url: https://api.anthropic.com
      api_key_env: ANTHROPIC_API_KEY
    - name: openai
      model: gpt-4o-mini
      base_url: https://api.openai.com/v1
      api_key_env: OPENAI_API_KEY
    - name: ollama
      model: mistral
      base_url: http://localhost:11434
    - name: huggingface
      model: gpt2             # any text-generation model on HuggingFace Hub
      max_new_tokens: 512     # optional, overrides max_tokens for local pipeline

Backward-compat: if no `providers` list is present the old single-provider
keys (provider / model / base_url) are wrapped into a one-element list so
existing deployments need zero config changes.
"""

from __future__ import annotations

import json
import logging
import os
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import httpx
import yaml

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
_HERE = Path(__file__).parent
_CONFIG_PATH = _HERE / "../config/settings.yaml"
_BRAIN_PATH = _HERE / "../memory/brain.json"

# Termux-specific .env fallback (kept for backward compat)
_TERMUX_ENV = Path("/data/data/com.termux/files/home/agent-x/.env")
# Standard project-root .env
_LOCAL_ENV = _HERE / "../.env"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _load_dotenv(path: Path) -> dict[str, str]:
    """Parse a simple KEY=VALUE .env file into a dict. Never raises."""
    env: dict[str, str] = {}
    try:
        for raw in path.read_text().splitlines():
            line = raw.strip().replace("\r", "")
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, _, v = line.partition("=")
            env[k.strip()] = v.strip().strip('"').strip("'")
    except Exception:
        pass
    return env


def _resolve_api_key(env_var: str | None, dot_envs: list[dict]) -> str | None:
    """
    Resolve an API key by checking (in order):
      1. process environment
      2. .env files supplied in dot_envs (local project .env first, then Termux)
    """
    if not env_var:
        return None
    # 1. process environment
    val = os.environ.get(env_var)
    if val:
        return val
    # 2. dot-env files
    for d in dot_envs:
        val = d.get(env_var)
        if val:
            return val
    return None


def _append_brain_event(event: dict) -> None:
    """
    Append a structured event to memory/brain.json.

    The file is expected to be either:
      • a JSON object  → an "llm_fallback_log" array is maintained inside it
      • a JSON array   → event is appended directly
      • missing/empty  → created as {"llm_fallback_log": [...]}
    """
    try:
        _BRAIN_PATH.parent.mkdir(parents=True, exist_ok=True)

        data: Any = None
        if _BRAIN_PATH.exists():
            try:
                data = json.loads(_BRAIN_PATH.read_text())
            except json.JSONDecodeError:
                data = None

        if isinstance(data, list):
            data.append(event)
        else:
            if not isinstance(data, dict):
                data = {}
            log: list = data.setdefault("llm_fallback_log", [])
            log.append(event)

        _BRAIN_PATH.write_text(json.dumps(data, indent=2))
    except Exception as exc:  # never crash the caller over logging
        logger.warning("brain.json write failed: %s", exc)


# ---------------------------------------------------------------------------
# Per-provider call implementations
# ---------------------------------------------------------------------------

async def _call_openrouter_or_openai(
    base_url: str,
    api_key: str,
    model: str,
    system_prompt: str,
    prompt: str,
    max_tokens: int,
    timeout: float,
    extra_headers: dict | None = None,
) -> str:
    """Shared implementation for OpenAI-compatible endpoints (openrouter, openai, ollama)."""
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    if extra_headers:
        headers.update(extra_headers)

    async with httpx.AsyncClient(timeout=timeout) as client:
        resp = await client.post(
            f"{base_url.rstrip('/')}/chat/completions",
            headers=headers,
            json={
                "model": model,
                "max_tokens": max_tokens,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt},
                ],
            },
        )
        if resp.status_code != 200:
            raise RuntimeError(
                f"HTTP {resp.status_code}: {resp.text[:300]}"
            )
        return resp.json()["choices"][0]["message"]["content"]


async def _call_ollama(
    base_url: str,
    model: str,
    system_prompt: str,
    prompt: str,
    timeout: float,
) -> str:
    """Ollama /api/chat endpoint (non-streaming)."""
    async with httpx.AsyncClient(timeout=timeout) as client:
        resp = await client.post(
            f"{base_url.rstrip('/')}/api/chat",
            json={
                "model": model,
                "stream": False,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt},
                ],
            },
        )
        if resp.status_code != 200:
            raise RuntimeError(
                f"Ollama HTTP {resp.status_code}: {resp.text[:300]}"
            )
        return resp.json()["message"]["content"]


async def _call_anthropic(
    base_url: str,
    api_key: str,
    model: str,
    system_prompt: str,
    prompt: str,
    max_tokens: int,
    timeout: float,
) -> str:
    """Anthropic Messages API."""
    async with httpx.AsyncClient(timeout=timeout) as client:
        resp = await client.post(
            f"{base_url.rstrip('/')}/v1/messages",
            headers={
                "x-api-key": api_key,
                "anthropic-version": "2023-06-01",
                "Content-Type": "application/json",
            },
            json={
                "model": model,
                "max_tokens": max_tokens,
                "system": system_prompt,
                "messages": [{"role": "user", "content": prompt}],
            },
        )
        if resp.status_code != 200:
            raise RuntimeError(
                f"Anthropic HTTP {resp.status_code}: {resp.text[:300]}"
            )
        return resp.json()["content"][0]["text"]


def _call_huggingface(
    model: str,
    system_prompt: str,
    prompt: str,
    max_new_tokens: int,
) -> str:
    """
    Local HuggingFace transformers text-generation pipeline.
    Imported lazily so the rest of the system works without `transformers`
    installed (it only becomes required when this provider is actually reached).
    """
    try:
        from transformers import pipeline as hf_pipeline  # type: ignore
    except ImportError as exc:
        raise RuntimeError(
            "transformers package not installed — cannot use huggingface provider"
        ) from exc

    full_prompt = f"{system_prompt}\n\n{prompt}"
    pipe = hf_pipeline("text-generation", model=model)
    result = pipe(full_prompt, max_new_tokens=max_new_tokens, num_return_sequences=1)
    generated: str = result[0]["generated_text"]
    # Strip the prompt prefix that some models echo back
    if generated.startswith(full_prompt):
        generated = generated[len(full_prompt):].strip()
    return generated


# ---------------------------------------------------------------------------
# Main client class
# ---------------------------------------------------------------------------

class LLMClient:
    """
    Multi-provider LLM client with automatic fallback.

    Usage is identical to the previous single-provider version:

        response = await llm.generate("Tell me about revenue strategies")
    """

    def __init__(self) -> None:
        # ------------------------------------------------------------------ #
        # Load YAML config                                                     #
        # ------------------------------------------------------------------ #
        with open(_CONFIG_PATH, "r") as fh:
            raw_cfg: dict = yaml.safe_load(fh)

        llm_cfg: dict = raw_cfg.get("llm", {})

        # Global timeout (seconds) — individual providers may override
        self._timeout: float = float(llm_cfg.get("timeout", 120))

        # ------------------------------------------------------------------ #
        # Build provider list                                                  #
        # ------------------------------------------------------------------ #
        if "providers" in llm_cfg and isinstance(llm_cfg["providers"], list):
            provider_defs: list[dict] = llm_cfg["providers"]
        else:
            # Backward-compat: wrap legacy single-provider keys
            provider_defs = [
                {
                    "name": llm_cfg.get("provider", "openrouter"),
                    "model": llm_cfg.get("model", "openai/gpt-4o-mini"),
                    "base_url": llm_cfg.get("base_url", "https://openrouter.ai/api/v1"),
                    "api_key_env": "OPENROUTER_API_KEY",
                }
            ]

        # ------------------------------------------------------------------ #
        # Pre-load .env files once (cheapest IO path)                         #
        # ------------------------------------------------------------------ #
        self._dot_envs: list[dict] = [
            _load_dotenv(_LOCAL_ENV),
            _load_dotenv(_TERMUX_ENV),
        ]

        # ------------------------------------------------------------------ #
        # Resolve each provider's API key eagerly (for startup diagnostics)   #
        # ------------------------------------------------------------------ #
        self._providers: list[dict] = []
        for pdef in provider_defs:
            name = pdef.get("name", "unknown")
            api_key = _resolve_api_key(pdef.get("api_key_env"), self._dot_envs)
            entry = {**pdef, "_resolved_api_key": api_key}
            self._providers.append(entry)

            if name in ("openrouter", "openai", "anthropic") and not api_key:
                logger.warning(
                    "⚠️  [LLM] Provider '%s' has no API key for env-var '%s' — "
                    "it will be skipped at runtime.",
                    name,
                    pdef.get("api_key_env", "<unset>"),
                )
            elif api_key:
                logger.info(
                    "🔑 [LLM] Provider '%s' key loaded: %s…",
                    name,
                    api_key[:12],
                )
            else:
                logger.info("🏠 [LLM] Provider '%s' configured (no key needed).", name)

        if not self._providers:
            raise ValueError("No LLM providers configured in config/settings.yaml [llm.providers]")

        logger.info(
            "✅ [LLM] Fallback chain: %s",
            " → ".join(p["name"] for p in self._providers),
        )

    # ---------------------------------------------------------------------- #
    # Public API                                                               #
    # ---------------------------------------------------------------------- #

    async def generate(
        self,
        prompt: str,
        system_prompt: str = "You are an expert AI agent.",
        max_tokens: int = 8000,
    ) -> str:
        """
        Generate a completion, trying each provider in order.

        Raises RuntimeError only if *every* provider in the chain fails.
        """
        errors: list[str] = []
        chain = [p["name"] for p in self._providers]

        for idx, provider in enumerate(self._providers):
            name: str = provider["name"]
            model: str = provider.get("model", "")
            timeout: float = float(provider.get("timeout", self._timeout))

            logger.info(
                "🧠 [LLM] Attempting provider %d/%d: %s (model=%s, max_tokens=%d)",
                idx + 1,
                len(self._providers),
                name,
                model,
                max_tokens,
            )

            try:
                result = await self._dispatch(
                    provider=provider,
                    name=name,
                    model=model,
                    system_prompt=system_prompt,
                    prompt=prompt,
                    max_tokens=max_tokens,
                    timeout=timeout,
                )
                logger.info("✅ [LLM] Success from provider '%s'.", name)
                return result

            except Exception as exc:
                err_msg = f"{name}: {exc}"
                errors.append(err_msg)
                logger.warning("⚠️  [LLM] Provider '%s' failed — %s", name, exc)

                # Log fallback event to memory/brain.json
                next_provider = self._providers[idx + 1]["name"] if idx + 1 < len(self._providers) else None
                _append_brain_event(
                    {
                        "event": "llm_fallback",
                        "timestamp": datetime.now(timezone.utc).isoformat(),
                        "failed_provider": name,
                        "next_provider": next_provider,
                        "error": str(exc)[:500],
                        "chain": chain,
                        "attempt": idx + 1,
                        "total_providers": len(self._providers),
                    }
                )

                if next_provider:
                    logger.info("🔄 [LLM] Falling back to provider '%s'…", next_provider)
                # continue to next provider

        # All providers exhausted
        summary = "; ".join(errors)
        _append_brain_event(
            {
                "event": "llm_chain_exhausted",
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "chain": chain,
                "errors": errors,
            }
        )
        raise RuntimeError(
            f"All LLM providers in the fallback chain failed. Errors: {summary}"
        )

    # ---------------------------------------------------------------------- #
    # Internal dispatch                                                        #
    # ---------------------------------------------------------------------- #

    async def _dispatch(
        self,
        provider: dict,
        name: str,
        model: str,
        system_prompt: str,
        prompt: str,
        max_tokens: int,
        timeout: float,
    ) -> str:
        """Route to the correct provider implementation."""
        api_key: str | None = provider.get("_resolved_api_key")
        base_url: str = provider.get("base_url", "")

        if name == "openrouter":
            if not api_key:
                raise RuntimeError("No API key available for openrouter")
            return await _call_openrouter_or_openai(
                base_url=base_url or "https://openrouter.ai/api/v1",
                api_key=api_key,
                model=model,
                system_prompt=system_prompt,
                prompt=prompt,
                max_tokens=max_tokens,
                timeout=timeout,
                extra_headers={
                    "HTTP-Referer": "https://agent-x.local",
                    "X-Title": "Agent-X Autopilot",
                },
            )

        elif name == "openai":
            if not api_key:
                raise RuntimeError("No API key available for openai")
            return await _call_openrouter_or_openai(
                base_url=base_url or "https://api.openai.com/v1",
                api_key=api_key,
                model=model,
                system_prompt=system_prompt,
                prompt=prompt,
                max_tokens=max_tokens,
                timeout=timeout,
            )

        elif name == "anthropic":
            if not api_key:
                raise RuntimeError("No API key available for anthropic")
            return await _call_anthropic(
                base_url=base_url or "https://api.anthropic.com",
                api_key=api_key,
                model=model,
                system_prompt=system_prompt,
                prompt=prompt,
                max_tokens=max_tokens,
                timeout=timeout,
            )

        elif name == "ollama":
            return await _call_ollama(
                base_url=base_url or "http://localhost:11434",
                model=model,
                system_prompt=system_prompt,
                prompt=prompt,
                timeout=timeout,
            )

        elif name == "huggingface":
            # HuggingFace pipeline is synchronous — run in executor so we
            # don't block the event loop.
            import asyncio
            max_new_tokens: int = int(provider.get("max_new_tokens", min(max_tokens, 512)))
            loop = asyncio.get_event_loop()
            return await loop.run_in_executor(
                None,
                _call_huggingface,
                model,
                system_prompt,
                prompt,
                max_new_tokens,
            )

        else:
            raise RuntimeError(f"Unknown provider type: '{name}'")


# ---------------------------------------------------------------------------
# Module-level singleton (preserves the existing public API surface)
# ---------------------------------------------------------------------------
llm = LLMClient()
