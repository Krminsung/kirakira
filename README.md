# Kirakira

Kirakira is a character chat service with a Vite/React frontend and a FastAPI
backend. The current runtime on this server is a 3-node minikube cluster.

## Runtime

Current production flow:

```text
client
-> edge-nginx Docker container on 80/443
-> minikube NodePort services on the kirakira-lab Docker network
   - frontend: kirakira-lab:32003 -> service/frontend:3003
   - backend: kirakira-lab:32083 -> service/backend:8003
-> minikube Pods
```

The public reverse proxy remains outside Kubernetes at:

```text
/root/infra/reverse-proxy
```

The app itself runs in minikube:

- minikube profile: `kirakira-lab`
- Kubernetes namespace: `kirakira`
- Frontend Deployment: `kirakira-frontend:latest`
- Backend Deployment: `kirakira-backend:latest`
- Upload storage: `uploads` PVC using minikube `standard` storage class
- Database: existing host PostgreSQL outside the cluster, reached through `host.minikube.internal`

## Repository Layout

```text
backend/              FastAPI application
frontend/             Vite React application
database/migrations/  SQL migrations
k8s/                  Kubernetes manifests and deployment notes
docker-compose.yml    Image build definition and legacy local runtime
```

## Local Builds

Frontend:

```sh
cd frontend
npm ci
npm run build
```

Backend syntax check:

```sh
python3 -m compileall backend/app
```

Docker images:

```sh
docker-compose -f docker-compose.yml build kirakira-frontend kirakira-backend
```

## Deploy to minikube

This server's `/usr/local/bin/kubectl` is currently the k3s wrapper. Use
`minikube -p kirakira-lab kubectl -- ...` for minikube commands.

Start the lab cluster if needed:

```sh
minikube start -p kirakira-lab --nodes=3 --driver=docker --memory=1800 --cpus=2 --force --extra-config=kubelet.cgroup-driver=systemd
```

If worker nodes fail with `too many open files`, raise the host inotify limits:

```sh
sudo sysctl -w fs.inotify.max_user_instances=8192 fs.inotify.max_user_watches=1048576
```

Load locally built images into minikube:

```sh
minikube -p kirakira-lab image load kirakira-backend:latest
minikube -p kirakira-lab image load kirakira-frontend:latest
```

Create or update the application Secret from the local `.env`, then patch
runtime-only values:

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

## Verify Production

Cluster state:

```sh
minikube -p kirakira-lab kubectl -- get nodes -o wide
minikube -p kirakira-lab kubectl -- -n kirakira get deploy,pods,svc,pvc -o wide
```

Expected app services:

```text
frontend  NodePort 3003:32003
backend   NodePort 8003:32083
```

Current pod placement on the 3-node profile:

```text
frontend -> kirakira-lab
backend  -> kirakira-lab-m02
m03      -> available for scheduling practice
```

Public route checks:

```sh
curl -k -I --resolve kirakira.cukee.world:443:127.0.0.1 https://kirakira.cukee.world/
curl -k -i --resolve kirakira.cukee.world:443:127.0.0.1 https://kirakira.cukee.world/api/auth/me
```

Expected results:

- `/` returns `200`
- `/api/auth/me` returns `401` when not logged in

## Reverse Proxy

`edge-nginx` must be connected to the minikube Docker network and should proxy
by Docker DNS name:

```text
frontend upstream: http://kirakira-lab:32003
backend upstream:  http://kirakira-lab:32083
```

The reverse proxy compose file includes `kirakira-lab` as an external network so
this survives container recreation.

## PostgreSQL Access

The host PostgreSQL must allow the minikube node and Pod CIDRs for the
`kirakira` database user. Current required `pg_hba.conf` rules:

```conf
host    kirakira        kirakira        192.168.49.0/24          scram-sha-256
host    kirakira        kirakira        10.244.0.0/16            scram-sha-256
```

Reload PostgreSQL after editing:

```sh
sudo -u postgres psql -Atqc "select pg_reload_conf();"
```

## Notes

- The minikube profile is a 3-node lab cluster on one physical server.
- Current nodes are `kirakira-lab`, `kirakira-lab-m02`, and `kirakira-lab-m03`.
- It is useful for multi-node scheduling practice, but it is not equivalent to a real multi-server production cluster.
- The previous k3s Kirakira deployments are scaled to `0` replicas.
- `edge-nginx` is still the only public ingress on host ports `80/443`.
- Do not commit `.env`, API keys, or Kubernetes Secret manifests.
