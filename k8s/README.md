# Kirakira on minikube

This directory contains Kubernetes manifests for running Kirakira on this
server's minikube profile.

## Files

- `minikube.yaml`: current runtime manifest for the `kirakira-lab` minikube profile
- `kirakira.yaml`: previous k3s manifest with fixed k3s ClusterIP services, kept for reference/rollback only

## Runtime Layout

- minikube profile: `kirakira-lab`
- nodes: `kirakira-lab` control-plane, `kirakira-lab-m02` worker, and `kirakira-lab-m03` worker
- `frontend`: Vite production build served by Nginx on port `3003`
- `backend`: FastAPI served by Uvicorn on port `8003`
- `uploads`: PVC mounted at `/app/uploads`
- `kirakira-env`: Kubernetes Secret created from the local `.env`
- existing host PostgreSQL remains outside the cluster

The public edge remains `/root/infra/reverse-proxy` `edge-nginx`, which proxies:

- frontend: `http://kirakira-lab:32003`
- backend: `http://kirakira-lab:32083`

## Deploy

Build and load local images into minikube:

```sh
docker-compose -f docker-compose.yml build kirakira-frontend kirakira-backend
minikube -p kirakira-lab image load kirakira-backend:latest
minikube -p kirakira-lab image load kirakira-frontend:latest
```

If worker nodes fail with `too many open files`, raise the host inotify limits:

```sh
sudo sysctl -w fs.inotify.max_user_instances=8192 fs.inotify.max_user_watches=1048576
```

Create the Secret without committing secrets:

```sh
minikube -p kirakira-lab kubectl -- create namespace kirakira --dry-run=client -o yaml | minikube -p kirakira-lab kubectl -- apply -f -
minikube -p kirakira-lab kubectl -- -n kirakira create secret generic kirakira-env --from-env-file=.env --dry-run=client -o yaml | minikube -p kirakira-lab kubectl -- apply -f -
minikube -p kirakira-lab kubectl -- -n kirakira patch secret kirakira-env --type merge -p '{"stringData":{"DATABASE_URL":"postgresql://<user>:<password>@host.minikube.internal:5432/kirakira","FRONTEND_URL":"https://kirakira.cukee.world","BACKEND_CORS_ORIGINS":"[\"https://kirakira.cukee.world\"]"}}'
```

Apply manifests:

```sh
minikube -p kirakira-lab kubectl -- apply -f k8s/minikube.yaml
minikube -p kirakira-lab kubectl -- -n kirakira rollout status deployment/frontend
minikube -p kirakira-lab kubectl -- -n kirakira rollout status deployment/backend
```

## Verify

```sh
minikube -p kirakira-lab kubectl -- get nodes -o wide
minikube -p kirakira-lab kubectl -- -n kirakira get pods,svc,pvc -o wide
curl -k -I --resolve kirakira.cukee.world:443:127.0.0.1 https://kirakira.cukee.world/
curl -k -i --resolve kirakira.cukee.world:443:127.0.0.1 https://kirakira.cukee.world/api/auth/me
```

PostgreSQL must allow the minikube node and Pod CIDRs for this app:

```conf
host    kirakira        kirakira        192.168.49.0/24          scram-sha-256
host    kirakira        kirakira        10.244.0.0/16            scram-sha-256
```
