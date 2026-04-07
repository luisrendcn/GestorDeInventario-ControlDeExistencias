# Build stage
FROM node:20-alpine AS builder

WORKDIR /app

# Copy package files
COPY package.json pnpm-lock.yaml pnpm-workspace.yaml ./
COPY artifacts/inventario-ui ./artifacts/inventario-ui
COPY lib ./lib

# Install dependencies
RUN npm install -g pnpm
RUN pnpm install --frozen-lockfile

# Build
WORKDIR /app/artifacts/inventario-ui
RUN pnpm run build

# Runtime stage - Nginx
FROM nginx:alpine

# Copy nginx config
COPY artifacts/inventario-ui/nginx.conf /etc/nginx/conf.d/default.conf

# Copy built app
COPY --from=builder /app/artifacts/inventario-ui/dist /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
