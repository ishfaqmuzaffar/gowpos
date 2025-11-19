# syntax=docker/dockerfile:1.5
# Multi-stage image for the GowPOS web frontend.
# By default we expect a React/Vite app that builds to static assets.

ARG NODE_VERSION=20.11.1
FROM node:${NODE_VERSION}-slim AS base
WORKDIR /app

FROM base AS deps
COPY frontend/package*.json ./
RUN npm ci

FROM deps AS build
COPY frontend .
RUN npm run build

FROM nginx:1.25-alpine AS runner
COPY --from=build /app/dist /usr/share/nginx/html
# The default nginx.conf already serves static files.
EXPOSE 80
