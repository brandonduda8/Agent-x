import os
import asyncio
import subprocess

def write_file(filepath: str, content: str):
    """Safely write content to a file in the workspace."""
    os.makedirs(os.path.dirname(filepath) or '.', exist_ok=True)
    with open(filepath, 'w') as f:
        f.write(content)
    print(f"💾 [CODE TOOL] Wrote {len(content)} bytes to {filepath}")

def run_terminal_command(command: str) -> str:
    """Execute a shell command safely and return output."""
    print(f"⚙️ [CODE TOOL] Executing: {command}")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            return result.stdout.strip()
        else:
            return f"Error: {result.stderr.strip()}"
    except Exception as e:
        return f"Exception: {str(e)}"
