This page documents the structure and philosophy behind the Ansible roles used to provision, deploy, and manage services across the environment—from local test clusters to full production in Lothlórien.

## 🎯 Philosophy
Everything is declarative, composable, and target-agnostic. Whether deploying to:
- ⚙️ Bare metal
- 💻 Multipass VM
- 📦 Proxmox VM
- 📦 Proxmox LXC container

After provisioning, the same roles apply. Inventory determines the what, playbooks coordinate the how.

## 📁 Role Structure
| Role | Purpose | 
|---|---|
| multipass | Launch and configure Multipass VMs (e.g., for local test clusters in WSL) | 
| proxmox-vm / proxmox-ct | Provision and configure Proxmox VMs and containers on Iluvatar | 
| microk8s | Bootstrap a single-node or multi-node K8s cluster (w/ optional MicroCeph) | 
| postgres / redis | Deploy core backing services | 
| mtig-stack | Deploy all web-facing microservices, including nodeapi, webdisplay, and MTIG | 
| cluster-init | High-level orchestration across roles, often gated by inventory groups or tags | 

All roles are idempotent and support testing in either Mirkwood (staging) or Lothlórien (production).

## 🌍 Current Topology
| Node Pool | Description | 
|---|---|
| Lothlórien | Production workloads—deployed via Ansible; stable, persistent | 
| Mirkwood | Development and testing—cluster spins up via the same playbooks | 
| Multipass (WSL) | Formerly used for local K8s testing in WSL with MicroK8s; may return when RAM allows | 



## 🧪 Testing Workflows
You used to spin up clusters under [WSL using multipass + microk8s](https://github.com/dekeyrej/ecosystem-map/wiki/%F0%9F%A7%AA-WSL-Development) for quick dev/test loops. Now with Iluvatar's Proxmox resources available, Mirkwood acts as the live playground.
All Ansible playbooks work seamlessly against any of:
- WSL (via localhost transport)
- Multipass VMs (via SSH)
- Proxmox VMs/CTs (via standard inventory)

## 🔐 Secrets & Bootstrapping
Secrets are handled by the secretmanager project, which pulls Vault-encrypted secrets into services via ephemeral authentication. These roles [inject secrets](https://github.com/dekeyrej/ecosystem-map/wiki/Secrets-&-Config) as part of application provisioning and config generation.
See: [🔐 Secrets & Config](https://github.com/dekeyrej/ecosystem-map/wiki/Secrets-&-Config)

## 🏗 Example Playbook
Here’s a condensed view of a production deploy flow:
```yaml
- hosts: cluster_nodes
  become: true
  roles:
    - microk8s
    - microceph   # optional
    - postgres
    - redis
    - nodeapi
    - webdisplay
    - mtig-stack
```

With just a tweak to inventory and vars, the same flow can target staging or multipass.

## 🧬 Deployed Services via Ansible

Roles manage deployment for a host of services, including:

Stack | Components | Purpose
--- | --- | ---
MTIG | Mosquitto, Telegraf, InfluxDB, Grafana | Metrics ingestion, visualization, and MQTT-based data transport
nodeapi | Custom service endpoints | Provides API data streams to webdisplay and SSE consumers
webdisplay | Frontend components | Real-time environmental dashboard & visualizers
Postgres/Redis | Backing data stores | Persistent state and message brokering

These get rolled out identically to either staging or production depending on inventory targeting—and tie into your SecretManager flow for secure config

## 📡 MTIG: Metrics & Messaging Stack
MTIG stands for <strong>Mosquitto–Telegraf–InfluxDB–Grafana</strong>, a telemetry powerhouse delivering real-time observability and visualization across the stack. Deployed via Ansible with the same flexibility as the rest of the system, it connects your environment's sensors, stats, and stories.

Component | Role
|--- | ---|
Mosquitto | Lightweight MQTT broker for sensor/event ingest
Telegraf | Agent for gathering & transforming data from MQTT, system metrics, and external APIs
InfluxDB | Time-series database for fast, durable metric storage
Grafana | Dashboard layer—visualizes everything from AQI to system perf

All of these can run on metal, VM, or containerized infrastructure, provisioned by the same playbooks used throughout Lothlórien and Mirkwood. They're loosely coupled and easily extended (e.g. add <code>Prometheus</code> or Grafana Loki for log streams).

Future ideas:
- 📈 Sensor → MQTT → Telegraf → Influx → Live Grafana dashboard loop
- 🧪 Run shadow MTIG instance in Mirkwood with mocked inputs for validation
- 🔒 Bind secret-sourced credentials and retention configs with `secretmanager`