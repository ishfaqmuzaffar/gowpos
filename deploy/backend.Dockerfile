# syntax=docker/dockerfile:1.5
# Multi-stage backend image for the GowPOS API service
# The file assumes a Node.js/TypeScript backend that exposes a build step.
# Adjust package manager commands if you are using pnpm/yarn/etc.

ARG NODE_VERSION=20.11.1
FROM node:${NODE_VERSION}-slim AS base
ENV NODE_ENV=production
WORKDIR /app

FROM base AS deps
# Install dependencies separately to leverage Docker layer caching
COPY backend/package*.json ./
RUN npm ci --omit=dev

FROM deps AS build
COPY backend .
RUN npm run build

FROM base AS runner
USER node
WORKDIR /app
COPY --from=build /app/dist ./dist
COPY --from=deps /app/node_modules ./node_modules
ENV PORT=8080
EXPOSE 8080
CMD ["node", "dist/index.js"]
