🧭 Ecosystem Map Documentation Outline
🏰 1. Introduction / Index (README.md)
- Title: The Ecosystem Map: A Modular Infrastructure Chronicle
- Purpose: What this map represents (homelab, automation, display, secrets)
- Philosophy: Modular, ephemeral, thematic
- Legend: Glossary of thematic names (e.g. Manwë, Celebrimbor, Recryptonator)
- Navigation: Table linking to all service and subsystem docs

⚙️ 2. Core Infrastructure
infra.md
- Overview of physical and virtual infrastructure
- Proxmox nodes, LXCs, VMs
- Networking, storage (Ceph), DNS, ingress
kubernetes.md
- Cluster layout and orchestration strategy
- Namespaces, deployments, CronJobs
- Helm, manifests, readiness probes
vault.md
- Vault setup and roles
- Transit secrets, TTL strategy
- Integration with Kubernetes
secrets.md
- SecretManager lifecycle
- Ephemeral access pattern
- Supported sources (env, file, Vault)

🧠 3. Microservices
Each doc follows a consistent template:
weather.md, moon.md, aqi.md, etc.
- Overview: What it does and why
- Data Source: API or feed used
- Secrets: What’s needed and how it’s pulled
- Flow: Lifecycle from pod start to Redis publish
- Display: How it’s rendered (Tidbyt, BMP, SSE)
- Deployment: YAML, CronJob, container image
- Notes: Edge cases, polling logic, quirks

🎛️ 4. Display & Clients
matrix.md
- RGB LED matrix setup
- BMP generation and rendering
- Display targets and rotation logic
nodewebdisplay.md
- SSE frontend
- Redis subscription
- Web-based rendering
matrixclient.md
- CLI or daemon client
- BMP generation and archival

🧩 5. Supporting Systems
recryptonator.md
- Encryption flow
- AES-256, Vault Transit
- Used by bootstrap roles and secret provisioning
celebrimbor.md
- Builder node
- Role in provisioning and orchestration
manwe.md
- Central orchestrator
- Recovery and rebuild strategy

🧙‍♂️ 6. Thematic Layer
naming.md (optional)
- Why the names matter
- Mapping Tolkien references to roles
- Storytelling as infrastructure design

📜 7. Project Evolution
Could be a collapsible section in README.md or its own doc:
- V1: ESP32 + CircuitPython
- V2: Monolithic Pi
- V3: Split client/server
- V4: Docker + Kubernetes
- Current: Modular microservices + Redis + Vault
