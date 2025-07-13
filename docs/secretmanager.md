# 🔐 SecretManager: Vault-Backed Secrets for Microservices

This document describes how microservices in the homelab retrieve secrets securely from HashiCorp Vault using the `KUBEVAULT` pattern. The implementation is powered by [`secretmanager.py`](https://github.com/dekeyrej/secretmanager/blob/main/secretmanager/secretmanager.py), and demonstrated in [`kubevault_example.py`](https://github.com/dekeyrej/secretmanager/blob/main/examples/kubevault_example.py).

---

## 🧠 The KUBEVAULT Pattern

Microservices authenticate to Vault using their Kubernetes service account. Vault is configured to recognize these identities and issue short-lived tokens that allow access to secrets or encryption services.

### 🔗 Flow Summary

1. **Service Account**: Microservice runs in Kubernetes with a bound service account.
2. **Vault Auth**: Vault is configured to trust the Kubernetes API and validate JWTs.
3. **Token Exchange**: Microservice uses its service account token to get a Vault token.
4. **Secret Access**: Vault token is used to `transit` decrypted ciphertext-version of secrets stored in a Kubernetes secret

---

## 🧪 Example: `kubevault_example.py`

This script demonstrates:

- Automatic Vault token acquisition via Kubernetes service account
- Retrieval of secrets from Kubernetes
- Use of Vault’s Transit engine for decryption

```python
from secretmanager import SecretManager

secretcfg = {
    "SOURCE": "KUBEVAULT",
    "kube_config": None,
    "service_account": "default",
    "namespace" : "default",
    "vault_url": "https://192.168.86.9:8200",
    "role": "demo",
    "ca_cert": True
}

sm = SecretManager(secretcfg)

# Fetch ciphertext version of a JSON-serialized Python dictionary containing secrets from a Kubernetes secret, and 
# decrypt/deserialize using Vault Transit decryption - return a Python dictionary
secrets = sm.read_secrets("matrix-secrets", "default", "SECRET", "secrets.json", "aes256-key")
```
---

## 🔐 Vault Configuration Requirements

Vault must be configured with:

- Kubernetes Auth Method:
- Bound to the correct service account and namespace
- JWT validation enabled

- Transit Secrets Engine:
- Key created (e.g., `my-key`)
- Permissions granted to the Vault role


This is handled by the `vault-configure-for-kubevault` role in the ansible repository.

---

## 🧱 SecretManager Capabilities

Method Description (for methods used in the example):
- `__init__()` uses secretcfg to configure the library for a particular _type_ of secret retrieval
- `connect_to_k8s()` connects to the kubenetes cluster's API service
- `get_k8s_service_account_token()` requests an ephermeral JWT (10m TTL)
- `connect_to_vault()` connects to the Vault authenitcated with the JWT (**10s** TTL)
- `read_encrypted_secrets()` wrapper for "KUBEVAULT" pattern
    -  `read_k8s_secret()` reads ciphertext from named kubernetes secret
    -  `decrypt_data_with_vault()` decrypts ciphertext using vault Transit service
    -  `load_json_secrets()` deserializes and returns decrypted text into Python dictionary

---

## 🔭 Roadmap

- Add support for token renewal and caching
- Extend to support AppRole and GCP IAM auth modes
- Integrate with Redis-first microservices for real-time secret updates

---

## 📎 Related Repositories

- `ansible`: Infrastructure automation for Vault and Kubernetes
- `microservicematrix`: Microservices consuming secrets via SecretManager

---

### In `vault.md`
Vault is provisioned via Ansible and integrated with MicroK8s for Kubernetes-based authentication. See microk8s.md for cluster setup and secretmanager.md for secrets templating and consumption.

### In `microk8s.md`
This role configures MicroK8s to authenticate with Vault and enables secrets encryption via Vault Transit. See vault.md for Vault provisioning and secretmanager.md for secrets usage patterns.

### In `secretmanager.md`
Secrets are encrypted using Vault Transit and consumed by microservices deployed in MicroK8s. See vault.md for encryption setup and microk8s.md for cluster integration.
