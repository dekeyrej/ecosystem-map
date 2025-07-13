# 🧭 “Data Flow at a Glance”

## 🎯 Purpose
A high-level overview of how data flows through my ecosystem: ingestion, storage, notification, and display—covering both infrastructure and design principles.

## 🔗 Related Repositories
- microservices : Collection of Python containers that fetch and publish live AQI, Weather, Moon, Family Event, Google Calendar, GitHub, MLB, and NFL data.
- APIServer : Acts as the central API hub and Redis event listener.
- nodewebdisplay : Front-end visual dashboard, now SSE-enabled for real-time updates.

## 📡 Real-Time Pipeline

Data Flow (Blue links are one time at start-up only):
```mermaid
flowchart LR
  subgraph Kubernetes
    Microservice -- PUB update --> Redis
    Redis -- SUB update --> KV-Updater
    KV-Updater -- WRITE KV --> Redis
    Redis -- SUB update --> APIServer
    APIServer -- READ KV --> Redis
  end
  Client -- READ API --> APIServer
  APIServer -- SSE update --> Client
style Microservice fill:#08f,color:#fff
style Redis fill:#e22,color:#fff
style KV-Updater fill:#eea,color:#000
style APIServer fill:#3d3,color:#fff
style Client fill:#fe1,color:#000
style Kubernetes fill:#fff,stroke:eea,stroke-width:1px,color:#444
linkStyle 4,5 stroke:#00F,color:blue
```

![Future Pipeline](https://github.com/dekeyrej/ecosystem-map/blob/main/diagrams/to-be_data_flow.svg)

Sequence Diagram:
```mermaid
sequenceDiagram
    participant Microservice
    participant Redis  as Redis 🧠
    participant Redis Snapshot as ⬆️ Redis Snapshot
    participant KV Updater as 🔁 KV Updater
    participant APIserver as 🖥️ APIserver
    participant Web/Matrix Client as 🌐 Web/Matrix Client
    Redis Snapshot->>+Redis: Load Snapshot
    APIserver->>+Redis: Read KV state (startup only)
    KV Updater->>+Redis: SUBSCRIBE 'update:{rich}'
    APIserver->>+Redis: SUBSCRIBE 'update:{rich}'
    APIserver->>+Web/Matrix Client: READ State
    Web/Matrix Client->>+APIserver: REQUEST SSE
    Microservice->>+Redis: PUBLISH 'update:{rich}'
    Redis->>+KV Updater: REPUBLISH 'update:{rich}'
    note over APIserver,Web/Matrix Client: SSE streams until disconnect
    KV Updater->>+Redis: WRITE KV Update
    Redis->>+Redis Snapshot: WRITE Snapshot
    Redis->>+APIserver: REPUBLISH 'update:{rich}'
    APIserver->>+Web/Matrix Client: SEND SSE
    note over Redis, Redis Snapshot: Internal to Redis
```

## 🧩 Tech Stack Highlights
- React + Bootstrap + Custom modules
- Redis pub/sub messaging for push efficiency
- Server-Sent Events (SSE) for display sync
- Kubernetes-deployed services, each containerized
- GitHub Actions CI/CD with automated image builds

## 🚀 Design Goals
- 🔒 Security-first: internal state (Redis) only accessed from inside the cluster
- 🔔 Decoupled updates: Redis notifies without blocking
- ♻️ Resilient render: display updates gracefully if data is delayed or unavailable
- 🎨 Expression-ready: dashboard supports curated, modular content including Moon phases, AQI, game stats, and more

## Project Plan:
```mermaid
---
config:
  kanban:
---
kanban
  [Todo]
    id10[WebDisplay: Swicth to a shared eventSource for SSE]@{priority: "High"}
    id11[WebDisplay: Process updates from SSE]@{priority: "High"}
  [In progress]
    id12[MatrixClient: Process Startup from NodeAPI]@{priority: "High"}
    id13[MatrixClient: Subscribe to SSE/Process Updates via SSE]@{priority: "High"}
    id14[MatrixClient: Remove DataSource]@{priority: "Low"}
    id15[MatrixClient: Remove Redis connection]@{priority: "Low"}
  [Ready for unit test]
    id6[NodeAPI: Read State from KV]@{priority: "High"}
    id7[NodeAPI: Read full message, update internal state]@{priority: "High"}
    id8[NodeAPI: Send full message via SSE]@{priority: "High"}
    id9[NodeAPI: Remove PostgreSQL handler]@{priority: "Low"}
  [Test cluster deployment]
    id1[ServerPage: Publish full message via Redis]@{priority: "High"}
    id2[ServerPage: Remove DataSource]@{priority: "Medium"}
    id3[ServerPage: Read update period from YAML deployment environment]@{priority: "Low"}
    id4[ServerPage: Read Health Check port number from secrets]@{priority: "Low"}
    id5[KV Updater: Create new app to subscribe to updates, and post to KV]@{priority: "High"}
    id16[DisplayPage: Remove DataSource]@{priority: "Low"}
  [Done]
    id0[Prototype Pub Full message, Receive Full message, write KV, read KV]@{priority: "High"}
```

*Note:* kanban _state_ is for illustrative purposes.  *All tasks* are actually complete.