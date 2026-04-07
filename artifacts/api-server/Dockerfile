# Build stage
FROM node:20-alpine AS builder

WORKDIR /app

# Copy package files
COPY package.json pnpm-lock.yaml pnpm-workspace.yaml ./
COPY artifacts/api-server ./artifacts/api-server
COPY lib ./lib

# Install dependencies
RUN npm install -g pnpm
RUN pnpm install --frozen-lockfile

# Build
WORKDIR /app/artifacts/api-server
RUN pnpm run build

# Runtime stage
FROM node:20-alpine

WORKDIR /app

# Install pnpm
RUN npm install -g pnpm

# Copy package files
COPY package.json pnpm-lock.yaml pnpm-workspace.yaml ./
COPY artifacts/api-server ./artifacts/api-server
COPY lib ./lib

# Install production dependencies only
RUN pnpm install --frozen-lockfile --prod

# Copy built application
COPY --from=builder /app/artifacts/api-server/dist ./artifacts/api-server/dist

WORKDIR /app/artifacts/api-server

# Expose port
EXPOSE 3000

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD node -e "require('http').get('http://localhost:3000/health', (r) => {if (r.statusCode !== 200) throw new Error(r.statusCode)})"

# Start application
CMD ["node", "--enable-source-maps", "--env-file=../../.env", "dist/index.mjs"]
