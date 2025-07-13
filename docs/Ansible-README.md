![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)
![Last Commit](https://img.shields.io/github/last-commit/dekeyrej/ansible)
![Repo Size](https://img.shields.io/github/repo-size/dekeyrej/ansible)
![Ansible Lint](https://img.shields.io/badge/lint-passing-brightgreen) <!-- Update dynamically if you add CI -->


# 📘 Project: Proxmox to Vault-Hardened MicroK8s Cluster Homelab Automation
A fully automated system for provisioning Kubernetes-ready nodes via Proxmox, configuring secure Vault-based secrets delivery, orchestrating microceph and microk8s clusters, and deploying services and applications—all with Ansible.

## 📁 Repository Structure

- `playbooks/`: Entry points for specific automation tasks.
- `roles/`: Modular roles for provisioning, configuration, and updates.
- `inventory/`: Host definitions for targeting your infrastructure.
- `collections/`: External dependencies (e.g., community modules).
- `ansible.cfg`: Configuration for Ansible execution.

## 🚀 Getting Started

Install required collections:

```bash
ansible-galaxy install -r collections/requirements.yml
```

## 🛠️ Features
- Proxmox VM & LXC container automation via community.general.proxmox
- Cloud-init bootstrapping and cloud-capable templating
- Self-signed RFC-compliant CA and TLS cert generation
- Vault installation, configuration, auto-unseal with GCP KMS
- MicroK8s and MicroCeph clustering with node prep
- Secrets provisioning for K8s workloads using 
- Turnkey deployment of microservices & supporting infrastructure

## 📁 Repo Structure

- `playbooks/`: Entry points for specific automation tasks.
- `roles/`: Modular roles for provisioning, configuration, and updates.
- `inventory/`: Host definitions for targeting your infrastructure.
- `collections/`: External dependencies (e.g., community modules).
- `ansible.cfg`: Configuration for Ansible execution.

Run a playbook:
```bash
ansible-playbook -i inventory/hosts.ini playbooks/88_proxmox_provision.yaml
```

## 🧱 Key Roles
| Role | Description | 
|---|---|
| proxmox-fetch-container-image | Downloads latest Ubuntu Noble LXC image | 
| vault-install | Installs and configures HashiCorp Vault | 
| microk8s-assemble-cluster | Builds a MicroK8s cluster across nodes | 
| redis | Sets up Redis for real-time data flow | 
| deploy-microservices | Deploys Redis-first microservices | 
| magic-mirror | Configures MagicMirror display system | 


## 🧪 Testing & Development
Use roletesting.yaml or testbook.yaml for isolated role testing.

## 🧠 Philosophy
- Declarative: Minimal imperative logic.
- Composable: Roles can be reused across playbooks.
- Transparent: Clear logs and traceable actions.

## 📜 License
MIT

## 🧩 Related Projects
- [MicroServiceMatrix](https://github.com/dekeyrej/microservicematrix) Modular microservices for real-time updates
- [MatrixClient](https://github.com/dekeyrej/matrixclient) SSE-driven client for Redis-first architecture



## 🌱 Extras
- MagicMirror2 container bootstrapped with Ansible
- Future support for deploy_mtig_stack, open-webui, and other microservices

## 🔭 Roadmap
- Improve cloud-init templating of base images
- Replace cert patching once MicroK8s supports modern key usages
- Add validation role to verify cluster and secrets bootstrapping
