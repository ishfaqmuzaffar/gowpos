# GowPOS Deployment Assets

This directory centralizes container images, local development compose files, Kubernetes manifests, monitoring configuration, and operational guidance.

## Containers

- `backend.Dockerfile` – multi-stage Node.js/TypeScript build that outputs a slim runtime image for the API.
- `frontend.Dockerfile` – multi-stage build for the React/Vite SPA served by nginx.
- `docker-compose.yml` – local development stack including Postgres, Redis, Prometheus, and Grafana.

To build images locally:

```bash
docker build -f deploy/backend.Dockerfile -t gowpos-backend ..
docker build -f deploy/frontend.Dockerfile -t gowpos-frontend ..
```

To start the compose stack:

```bash
cd deploy
docker compose up --build
```

## Kubernetes Layout

```
deploy/k8s
├── base              # Shared resources (Deployments, Services, config, monitoring)
├── staging           # Staging overlay (debug logging, staging URLs)
└── production        # Production overlay (higher replicas/resources)
```

Use Kustomize to render each environment:

```bash
kustomize build deploy/k8s/staging | kubectl apply -f -
kustomize build deploy/k8s/production | kubectl apply -f -
```

### Secret Management

Secrets are **never** committed. Instead, the cluster uses [`ExternalSecret`](https://external-secrets.io/) resources (`base/external-secret.yaml`) wired to a `ClusterSecretStore` named `gowpos-secret-store`. Configure the store to point at AWS Secrets Manager, GCP Secret Manager, or Vault depending on the cluster. The ExternalSecret pulls `DATABASE_URL`, `REDIS_URL`, and `JWT_SECRET` into a `gowpos-secrets` Secret that is mounted by the backend Deployment.

For local development, replicate the same values through the `.env` files consumed by the backend/frontend and the compose services.

## Monitoring

Prometheus and Grafana manifests live under `deploy/monitoring`. When running via Compose, the Prometheus scrape config and Grafana provisioning files are bind-mounted automatically. In Kubernetes, the `ServiceMonitor` resources (in `k8s/base/monitoring.yaml`) integrate with the Prometheus Operator. The Grafana dashboard `gowpos-overview.json` focuses on API latency, request throughput, and bundle size metrics—extend as required.

## Environments

| Environment | Namespace         | Notes |
|-------------|-------------------|-------|
| Staging     | `gowpos-staging`  | Single backend replica, verbose logging, staging URLs. |
| Production  | `gowpos-prod`     | Scales replicas/resources, production URLs. |

