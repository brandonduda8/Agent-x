# =============================================================================
# Agent X — Dockerfile (Linux/cloud deployment only)
#
# ⚠  TERMUX USERS: Docker is NOT available in standard Termux.
#    Use termux/setup.sh + termux/start.sh directly.
#
# Build:
#   docker build -t agent-x -f deployment/Dockerfile .
# Run:
#   docker run -d --env-file .env -p 3000:3000 -p 3002:3002 agent-x
# =============================================================================

FROM node:20-alpine

# Install Python + pip for the Python intelligence layer
RUN apk add --no-cache \
    python3 \
    py3-pip \
    bash \
    curl \
    jq \
    && ln -sf python3 /usr/bin/python

WORKDIR /opt/agent-x

# ── Node.js dependencies ─────────────────────────────────────────────────────
COPY package*.json             ./
COPY agent-x-core/package*.json agent-x-core/
COPY digital-twin/package*.json digital-twin/
COPY communication/package*.json communication/
COPY webhook-listener/package*.json webhook-listener/

RUN npm install --omit=dev --silent \
 && (cd agent-x-core    && npm install --omit=dev --silent) \
 && (cd digital-twin    && npm install --omit=dev --silent) \
 && (cd communication   && npm install --omit=dev --silent) \
 && (cd webhook-listener && npm install --omit=dev --silent)

# ── Python dependencies ───────────────────────────────────────────────────────
COPY requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt

# ── Application source ────────────────────────────────────────────────────────
COPY . .

# Runtime directories
RUN mkdir -p memory data generated logs products/deliverables products/catalog

# Install PM2 globally for process management inside container
RUN npm install -g pm2

EXPOSE 3000 3002 5000

ENV NODE_ENV=production

CMD ["pm2-runtime", "start", "termux/start.sh", "--interpreter", "bash"]
