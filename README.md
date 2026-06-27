<div align="center">

<!-- Header -->
<img src="https://capsule-render.vercel.app/api?type=waving&color=gradient&customColorList=5,12,19&height=210&section=header&text=KIRAKIRA&fontSize=76&fontColor=fff&animation=twinkling&fontAlignY=36&desc=AI%20Character%20Chat%20Platform&descSize=20&descAlignY=57" width="100%"/>

<!-- Typing Animation -->
<a href="https://git.io/typing-svg">
  <img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=600&size=22&duration=3000&pause=1000&color=FFB703&center=true&vCenter=true&multiline=true&repeat=false&width=760&height=100&lines=%EC%BA%90%EB%A6%AD%ED%84%B0%EB%A5%BC+%EB%A7%8C%EB%93%A4%EA%B3%A0+AI%EC%99%80+%EB%8C%80%ED%99%94%ED%95%98%EB%8A%94+%EC%B1%84%ED%8C%85+%ED%94%8C%EB%9E%AB%ED%8F%BC;Create%2C+Discover%2C+and+Chat+with+AI+Characters" alt="Typing SVG" />
</a>

<!-- Badges -->
<p>
  <img src="https://img.shields.io/badge/React-19.2-61DAFB?style=for-the-badge&logo=react&logoColor=black" alt="React"/>
  <img src="https://img.shields.io/badge/TypeScript-5.9-3178C6?style=for-the-badge&logo=typescript&logoColor=white" alt="TypeScript"/>
  <img src="https://img.shields.io/badge/Vite-7.2-646CFF?style=for-the-badge&logo=vite&logoColor=white" alt="Vite"/>
  <img src="https://img.shields.io/badge/FastAPI-0.109-009688?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI"/>
</p>

<p>
  <img src="https://img.shields.io/badge/PostgreSQL-AsyncPG-4169E1?style=for-the-badge&logo=postgresql&logoColor=white" alt="PostgreSQL"/>
  <img src="https://img.shields.io/badge/Google%20Gemini-AI-8E75B2?style=for-the-badge&logo=googlegemini&logoColor=white" alt="Gemini"/>
  <img src="https://img.shields.io/badge/Docker-Image%20Build-2496ED?style=for-the-badge&logo=docker&logoColor=white" alt="Docker"/>
  <img src="https://img.shields.io/badge/minikube-3%20Nodes-326CE5?style=for-the-badge&logo=kubernetes&logoColor=white" alt="minikube"/>
  <img src="https://img.shields.io/badge/Nginx-Edge%20Proxy-009639?style=for-the-badge&logo=nginx&logoColor=white" alt="Nginx"/>
</p>

<a href="https://kirakira.cukee.world">
  <img src="https://img.shields.io/badge/LIVE%20SERVICE-kirakira.cukee.world-FFB703?style=for-the-badge&logo=googlechrome&logoColor=black" alt="Live Service"/>
</a>

</div>

---

## ✨ 서비스 소개 / 대상 사용자

**KIRAKIRA**는 사용자가 직접 AI 캐릭터를 만들고, 공개된 캐릭터를 탐색하며, 캐릭터의 세계관과 성격에 맞춰 대화할 수 있는 **AI 캐릭터 채팅 플랫폼**입니다.

<table>
<tr>
<td width="50%" valign="top">

### 💡 핵심 차별점

| | 특징 |
|:---:|:---|
| 🎭 | **캐릭터 중심 대화** - 성격, 말투, 비밀 설정, 예시 대화 기반 페르소나 구성 |
| 🌍 | **세계관 기반 몰입감** - 캐릭터별 배경과 세계관을 대화 컨텍스트에 반영 |
| ⚡ | **크레딧 기반 운영** - 메시지 모델별 Kira 차감, 일일 무료 크레딧, 거래 이력 관리 |
| 🧠 | **멀티 AI Provider** - Gemini, FriendliAI, Cukee AI 라우팅 구조 |

</td>
<td width="50%" valign="top">

### 🎯 대상 사용자

| | 대상 | 설명 |
|:---:|:---:|:---|
| 💬 | **AI 채팅 사용자** | 캐릭터와 롤플레잉/일상 대화를 즐기는 사용자 |
| ✍️ | **캐릭터 제작자** | 캐릭터 설정, 프로필, 말투를 구성해 공유하고 싶은 사용자 |
| 🧪 | **AI 서비스 운영 학습자** | 크레딧, 인증, 배포, Kubernetes 운영을 실습하려는 개발자 |

</td>
</tr>
</table>

---

## 🔍 사용자 및 문제 정의

<div align="center">

### 기존 문제점 vs KIRAKIRA 솔루션

</div>

| 😫 기존 문제 | 💡 KIRAKIRA 솔루션 |
|:---|:---|
| 단순 챗봇은 캐릭터 정체성과 말투 유지가 약함 | 캐릭터 설명, 성격, 비밀 설정, 예시 대화를 조합한 시스템 프롬프트 구성 |
| 대화 대상 캐릭터를 직접 만들고 관리하기 어려움 | 캐릭터 생성/수정, 이미지 업로드, 공개 캐릭터 탐색 제공 |
| AI 사용량 비용을 서비스 레벨에서 제어하기 어려움 | Kira 크레딧 잔액, 모델별 차감, 일일 보상, 충전 UI 제공 |
| 단일 모델 장애/비용 변화에 취약함 | Gemini, FriendliAI, Cukee AI를 선택 가능한 Provider 구조로 분리 |
| 로컬 개발과 운영 배포 환경이 섞이기 쉬움 | Docker 이미지 빌드와 3노드 minikube 운영 매니페스트 분리 |

---

## 🛠️ 기술 스택

<div align="center">

### Frontend

![React](https://img.shields.io/badge/React-61DAFB?style=for-the-badge&logo=react&logoColor=black)
![TypeScript](https://img.shields.io/badge/TypeScript-3178C6?style=for-the-badge&logo=typescript&logoColor=white)
![Vite](https://img.shields.io/badge/Vite-646CFF?style=for-the-badge&logo=vite&logoColor=white)
![React Router](https://img.shields.io/badge/React%20Router-CA4245?style=for-the-badge&logo=reactrouter&logoColor=white)
![Tailwind CSS](https://img.shields.io/badge/Tailwind%20CSS-06B6D4?style=for-the-badge&logo=tailwindcss&logoColor=white)

### Backend

![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0-D71F00?style=for-the-badge&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)
![JWT](https://img.shields.io/badge/JWT-Auth-000000?style=for-the-badge&logo=jsonwebtokens&logoColor=white)

### AI / Infrastructure

![Gemini](https://img.shields.io/badge/Gemini-8E75B2?style=for-the-badge&logo=googlegemini&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![Kubernetes](https://img.shields.io/badge/minikube-326CE5?style=for-the-badge&logo=kubernetes&logoColor=white)
![Nginx](https://img.shields.io/badge/Nginx-009639?style=for-the-badge&logo=nginx&logoColor=white)

</div>

---

## 🚀 주요 기능 & 핵심 플로우

### 사용자 시나리오

```text
🔑 로그인/회원가입 → 🎭 캐릭터 탐색 → 💬 채팅 시작 → ⚡ Kira 차감 → 🧾 사용 이력 확인 → ✍️ 새 캐릭터 제작
```

<table>
<tr>
<td width="50%">

### 🎭 캐릭터 기능

| 기능 | 설명 |
|:---|:---|
| **캐릭터 목록** | 공개 캐릭터 탐색 및 상세 페이지 제공 |
| **캐릭터 생성** | 이름, 설명, 성격, 세계관, 예시 대화 입력 |
| **이미지 업로드** | 캐릭터 프로필 이미지 업로드 및 `/uploads` 정적 제공 |
| **세계관 연결** | 캐릭터 배경 설정을 대화 컨텍스트로 사용 |
| **마이페이지** | 내가 만든 캐릭터와 활동 정보 확인 |

</td>
<td width="50%">

### 💬 채팅 / 크레딧 기능

| 기능 | 설명 |
|:---|:---|
| **대화방 관리** | 캐릭터별 Conversation 생성 및 메시지 기록 저장 |
| **AI 스트리밍 응답** | Provider별 REST API 기반 응답 처리 |
| **모델 선택** | Gemini 2.5 Flash, Gemini 3.0 Flash, EXAONE, Cukee AI 구조 |
| **Kira 차감** | 메시지 전송 시 모델별 크레딧 차감 |
| **일일 크레딧** | 24시간 기준 무료 크레딧 지급 및 최대 보유량 제한 |
| **충전 UI** | `/recharge` 페이지에서 크레딧 패키지 안내 |

</td>
</tr>
</table>

---

## ✅ 구현 결과

### 핵심 요건

| 요건 | 상태 | 구현 내용 |
|:---|:---:|:---|
| **사용자 인증** | ✅ | 회원가입, 로그인, JWT 기반 현재 사용자 조회 |
| **캐릭터 CRUD** | ✅ | 캐릭터 생성/조회/상세, 작성자 관계 모델링 |
| **대화 저장** | ✅ | Conversation, Message 테이블 기반 대화 기록 저장 |
| **AI 응답 연동** | ✅ | Gemini/FriendliAI/Cukee AI Provider 라우팅 |
| **크레딧 시스템** | ✅ | Kira 잔액, 차감, 지급, 거래 내역, 일일 보상 |
| **이미지 업로드** | ✅ | base64 업로드 후 `/app/uploads` 저장 및 정적 제공 |
| **운영 배포** | ✅ | Docker 이미지 + minikube 3노드 + edge Nginx 라우팅 |

### 추가 구현 기능

<table>
<tr>
<td width="50%">

| 기능 | 설명 |
|:---|:---|
| **모델별 비용 정책** | AI 모델별 차등 Kira 비용 적용 |
| **거래 이력** | credit_transactions 테이블로 잔액 변화 추적 |
| **일일 보상 제한** | 24시간 단위 수령 제한과 최대 보유량 제한 |
| **Provider Fail Message** | API 키 누락/오류 시 사용자에게 명확한 메시지 반환 |

</td>
<td width="50%">

| 기능 | 설명 |
|:---|:---|
| **Kubernetes PVC** | 업로드 파일을 `uploads` PVC에 보관 |
| **NodePort 라우팅** | edge Nginx에서 minikube NodePort로 프록시 |
| **3노드 실습 환경** | control-plane 1개 + worker 2개 구성 |
| **k3s 롤백 여지** | 이전 `k8s/kirakira.yaml`을 참조용으로 보존 |

</td>
</tr>
</table>

---

## 🏗️ 아키텍처

```text
client
  |
  v
edge-nginx Docker container (:80/:443)
  |
  |-- /              -> http://kirakira-lab:32003 -> frontend service -> frontend pod
  |-- /api/*         -> http://kirakira-lab:32083 -> backend service  -> backend pod
  |-- /uploads/*     -> http://kirakira-lab:32083 -> backend static files
  |
  v
minikube profile: kirakira-lab
  |-- kirakira-lab      control-plane  192.168.49.2
  |-- kirakira-lab-m02  worker         192.168.49.3
  |-- kirakira-lab-m03  worker         192.168.49.4

backend pod
  |
  |-- host.minikube.internal:5432 -> host PostgreSQL
  |-- Gemini / FriendliAI / Cukee AI external APIs
  |-- uploads PVC -> /app/uploads
```

### Kubernetes 리소스

| 리소스 | 이름 | 설명 |
|:---|:---|:---|
| Namespace | `kirakira` | 애플리케이션 전용 네임스페이스 |
| Deployment | `frontend` | Vite 정적 빌드 Nginx 서빙 |
| Deployment | `backend` | FastAPI Uvicorn API 서버 |
| Service | `frontend` | NodePort `32003` |
| Service | `backend` | NodePort `32083` |
| PVC | `uploads` | 업로드 파일 영속 저장 |
| Secret | `kirakira-env` | `.env` 기반 런타임 Secret |

---

## 🔐 보안 / 운영 원칙

```text
┌─────────────────────────────────────────────────────────────────┐
│                         Security Layers                         │
├─────────────────────────────────────────────────────────────────┤
│  1. Public ingress is limited to edge-nginx :80/:443             │
│  2. App containers do not bind host ports                        │
│  3. Runtime secrets are created as Kubernetes Secret             │
│  4. PostgreSQL access is restricted by pg_hba.conf CIDR rules    │
│  5. Unknown hosts are blocked at the shared reverse proxy layer  │
└─────────────────────────────────────────────────────────────────┘
```

| 항목 | 적용 방식 |
|:---|:---|
| **인증** | JWT 기반 사용자 인증, 비밀번호 bcrypt 해시 |
| **Secret 관리** | `.env`는 커밋하지 않고 `kirakira-env` Secret으로 주입 |
| **DB 접근 제한** | minikube node/Pod CIDR만 Kirakira DB 사용자에 허용 |
| **Ingress 통제** | 호스트 공개 포트는 reverse proxy의 `80/443`만 허용 |
| **파일 업로드** | backend 내부 `/app/uploads` 저장 후 Nginx 경유 제공 |

---

## 📁 프로젝트 구조

```text
backend/              FastAPI application
backend/app/api/      API routers and endpoint modules
backend/app/models/   SQLAlchemy ORM models
backend/app/services/ AI provider and credit services
frontend/             Vite React application
frontend/src/pages/   Route-level pages
database/             SQL schema and migrations
k8s/                  Kubernetes manifests and deployment notes
docker-compose.yml    Local image build definition and legacy compose runtime
```

---

## ⚙️ 로컬 빌드

### Frontend

```sh
cd frontend
npm ci
npm run build
```

### Backend syntax check

```sh
python3 -m compileall backend/app
```

### Docker images

```sh
docker-compose -f docker-compose.yml build kirakira-frontend kirakira-backend
```

---

## 🚢 minikube 배포

이 서버의 `/usr/local/bin/kubectl`은 k3s wrapper입니다. minikube 명령은 다음 형식을 사용합니다.

```sh
minikube -p kirakira-lab kubectl -- <kubectl-args>
```

### 1. 3노드 클러스터 시작

```sh
minikube start -p kirakira-lab --nodes=3 --driver=docker --memory=1800 --cpus=2 --force --extra-config=kubelet.cgroup-driver=systemd
```

worker node에서 `too many open files`가 발생하면 host inotify limit을 올립니다.

```sh
sudo sysctl -w fs.inotify.max_user_instances=8192 fs.inotify.max_user_watches=1048576
```

### 2. 이미지 로드

```sh
minikube -p kirakira-lab image load kirakira-backend:latest
minikube -p kirakira-lab image load kirakira-frontend:latest
```

### 3. Secret 생성

```sh
minikube -p kirakira-lab kubectl -- create namespace kirakira --dry-run=client -o yaml | minikube -p kirakira-lab kubectl -- apply -f -
minikube -p kirakira-lab kubectl -- -n kirakira create secret generic kirakira-env --from-env-file=.env --dry-run=client -o yaml | minikube -p kirakira-lab kubectl -- apply -f -
minikube -p kirakira-lab kubectl -- -n kirakira patch secret kirakira-env --type merge -p '{"stringData":{"DATABASE_URL":"postgresql://<user>:<password>@host.minikube.internal:5432/kirakira","FRONTEND_URL":"https://kirakira.cukee.world","BACKEND_CORS_ORIGINS":"[\"https://kirakira.cukee.world\"]"}}'
```

### 4. Manifest 적용

```sh
minikube -p kirakira-lab kubectl -- apply -f k8s/minikube.yaml
minikube -p kirakira-lab kubectl -- -n kirakira rollout status deployment/frontend
minikube -p kirakira-lab kubectl -- -n kirakira rollout status deployment/backend
```

---

## 🧪 운영 검증

### Cluster state

```sh
minikube -p kirakira-lab kubectl -- get nodes -o wide
minikube -p kirakira-lab kubectl -- -n kirakira get deploy,pods,svc,pvc -o wide
```

Expected nodes:

```text
kirakira-lab      Ready  control-plane  192.168.49.2
kirakira-lab-m02  Ready  worker         192.168.49.3
kirakira-lab-m03  Ready  worker         192.168.49.4
```

Expected services:

```text
frontend  NodePort 3003:32003
backend   NodePort 8003:32083
```

### Public route checks

```sh
curl -k -I --resolve kirakira.cukee.world:443:127.0.0.1 https://kirakira.cukee.world/
curl -k -i --resolve kirakira.cukee.world:443:127.0.0.1 https://kirakira.cukee.world/api/auth/me
```

Expected results:

| Route | Expected |
|:---|:---:|
| `/` | `200` |
| `/api/auth/me` without login | `401` |

---

## 🗄️ PostgreSQL 접근 허용

host PostgreSQL은 Kirakira DB 사용자에 대해 minikube node/Pod CIDR만 허용합니다.

```conf
host    kirakira        kirakira        192.168.49.0/24          scram-sha-256
host    kirakira        kirakira        10.244.0.0/16            scram-sha-256
```

변경 후 reload:

```sh
sudo -u postgres psql -Atqc "select pg_reload_conf();"
```

---

## 📝 운영 메모

| 항목 | 현재 상태 |
|:---|:---|
| Runtime | 3-node minikube on one physical server |
| Public ingress | `/root/infra/reverse-proxy` edge Nginx |
| k3s migration state | previous k3s Kirakira deployments scaled to `0` replicas |
| Host ports | only `80/443` should be publicly bound |
| Secrets | `.env` and Kubernetes Secret manifests must not be committed |
| Limitation | minikube multi-node is useful for scheduling practice, not a real multi-server HA cluster |

