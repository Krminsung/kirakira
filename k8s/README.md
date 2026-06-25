# Kirakira on k3s

This directory contains the Kubernetes manifests for running Kirakira on the
single-node k3s cluster used by this server.

## Runtime Layout

- `frontend`: Vite production build served by Nginx on port `3003`
- `backend`: FastAPI served by Uvicorn on port `8003`
- `uploads`: local-path PVC mounted at `/app/uploads`
- `kirakira-env`: Kubernetes Secret created from the local `.env`
- Existing host PostgreSQL remains outside the cluster

The public edge remains `/root/infra/reverse-proxy` `edge-nginx`, which proxies:

- frontend: `10.43.120.10:3003`
- backend: `10.43.120.11:8003`

## Deploy

Build and import local images into k3s containerd:

```sh
docker-compose -f docker-compose.yml build kirakira-frontend kirakira-backend
docker save kirakira-backend:latest kirakira-frontend:latest | k3s ctr images import -
```

Create the Secret without committing secrets:

```sh
kubectl create namespace kirakira --dry-run=client -o yaml | kubectl apply -f -
kubectl -n kirakira create secret generic kirakira-env --from-env-file=.env --dry-run=client -o yaml | kubectl apply -f -
kubectl -n kirakira patch secret kirakira-env --type merge -p '{"stringData":{"DATABASE_URL":"postgresql://kirakira:kirakira123@192.168.0.1:5432/kirakira","FRONTEND_URL":"https://kirakira.cukee.world"}}'
```

Apply manifests:

```sh
kubectl apply -f k8s/kirakira.yaml
kubectl -n kirakira rollout status deployment/frontend
kubectl -n kirakira rollout status deployment/backend
```

PostgreSQL must allow the k3s Pod CIDR for this app:

```conf
host    kirakira        kirakira        10.42.0.0/16             scram-sha-256
```
