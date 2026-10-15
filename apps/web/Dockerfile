FROM node:20-alpine

# Set environment variables
ENV NODE_ENV=production \
    PORT=3000 \
    HOSTNAME=0.0.0.0

# Set working directory
WORKDIR /app

# Install pnpm
RUN corepack enable pnpm

# Copy package files
COPY apps/web/package.json apps/web/pnpm-lock.yaml ./

# Install dependencies
RUN pnpm install --frozen-lockfile

# Copy application code
COPY apps/web/src ./src
COPY apps/web/public ./public
COPY apps/web/next.config.js ./next.config.js
COPY apps/web/tsconfig.json ./tsconfig.json
COPY apps/web/.env.local ./.env.local

# Build the application
RUN pnpm build

# Expose port
EXPOSE 3000

# Health check
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD wget -q --spider http://localhost:3000 || exit 1

# Start the application
CMD ["pnpm", "start"]
