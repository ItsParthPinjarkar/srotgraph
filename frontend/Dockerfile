FROM node:22-alpine

# Set environment variables
ENV NODE_ENV=production \
    PORT=3000 \
    HOSTNAME=0.0.0.0

# Set working directory
WORKDIR /app

# Install pnpm
RUN corepack enable pnpm

# Copy package files
COPY frontend/pnpm-lock.yaml ./pnpm-lock.yaml
COPY frontend/package.json ./package.json

# Install dependencies
RUN pnpm install --frozen-lockfile

# Copy application code
COPY frontend/src ./src
COPY frontend/public ./public
COPY frontend/next.config.ts ./next.config.ts
COPY frontend/tsconfig.json ./tsconfig.json
COPY frontend/tsconfig.app.json ./tsconfig.app.json
COPY frontend/tsconfig.json ./tsconfig.json

# Build the application
RUN pnpm build

# Expose port
EXPOSE 3000

# Health check
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD wget -q --spider http://localhost:3000 || exit 1

# Start the application
CMD ["pnpm", "start"]
