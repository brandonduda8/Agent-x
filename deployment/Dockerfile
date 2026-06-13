FROM node:20-alpine

WORKDIR /app

# Copy package files first for better caching
COPY agent-x-core/package.json ./agent-x-core/
COPY digital-twin/package.json ./digital-twin/
COPY communication/package.json ./communication/

# Install dependencies
RUN cd agent-x-core && npm install --production
RUN cd digital-twin && npm install --production
RUN cd communication && npm install --production || true

# Copy application code
COPY agent-x-core/ ./agent-x-core/
COPY digital-twin/ ./digital-twin/
COPY communication/ ./communication/

# Expose ports
EXPOSE 3000 3001

# Start both services
CMD ["sh", "-c", "cd agent-x-core && node index.js & cd digital-twin && node index.js & wait"]
