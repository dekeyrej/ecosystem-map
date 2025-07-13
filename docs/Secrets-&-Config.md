# 🛡️ Secrets & Config: Vault-Based Secret Management with SecretManager

Managing secrets is one of the most fundamental (and risky) parts of building a distributed system. This ecosystem embraces a **“Secret Zero”** philosophy, leveraging **HashiCorp Vault**, Kubernetes Secrets, and some carefully crafted Python tooling to keep secrets secure—from initial encryption to runtime access and automated key rotation.

This approach is built to be:
- Secure-by-default
- Practical for homelab and production alike
- Ephemeral and minimally exposed

---

## 🔑 Why This Matters: Embracing Secret Zero

Kubernetes provides a way to store secrets—but not necessarily to store them **securely**. Most traditional patterns leave the “first secret” exposed in:
- Environment variables
- Mounted files
- Static, long-lived credentials

This ecosystem avoids that pitfall by storing only **Vault-encrypted ciphertext** inside Kubernetes and retrieving secrets at runtime via ephemeral tokens that live for 10 seconds or less. AES-256 key material **never enters the cluster**. Tokens aren’t stored. There are no standing credentials.

---

## 🔒 Design Principles

- All secrets are AES-256–encrypted via [[Vault Transit](https://developer.hashicorp.com/vault/docs/secrets/transit)](https://developer.hashicorp.com/vault/docs/secrets/transit)
- Only ciphertext is stored in Kubernetes
- Secrets are decrypted at runtime, in memory, via ephemeral Vault-authenticated sessions
- Vault tokens are short-lived (10s or less), and Kubernetes ServiceAccount tokens used for login have a TTL of just 10 minutes
- AES keys **never live in Kubernetes**
- Key rotation is fully automated
- The application holds secrets only in memory, never writes to disk or env

---

## 🛠️ Components

| Tool               | Role                                                                                  | Usage                     |
|--------------------|----------------------------------------------------------------------------------------|----------------------------|
| **encryptonator.py**     | Encrypts a plaintext JSON secrets dictionary using Vault Transit AES-256         | `python encryptonator.py` |
| **kubevault_example.py** | Retrieves and decrypts ciphertext at service startup (ephemeral)                 | `python kubevault_example.py` |
| **recryptonator.py**     | Scheduled key rotator: decrypt → rotate key → re-encrypt → update secret         | `python recryptonator.py` |

Each tool is defined with connection config (`secretcfg`) and the exact secret metadata (`secretdef`). See examples in [[SecretManager](https://github.com/dekeyrej/secretmanager/tree/main/examples/)](https://github.com/dekeyrej/secretmanager/tree/main/examples/).

---

## 🧰 Configuration Example

Here’s the core pattern used in Python services to fetch secrets:

For production - 

```python
secretcfg = {
  'SOURCE': 'KUBEVAULT',
  'vault_url': 'https://vault.mydomain.net',
  'auth_role': 'microservice-reader',
  ...
}

secretdef = {
  'namespace': 'dataops',
  'secret': 'weather-api-keys',
  'transit_key': 'env-data-key',
  ...
}
```

or, for development -

```python
secretcfg = {
  'SOURCE': 'FILE'
}

secretdef = {
  'file_name': 'secrets.json',
  'file_type': 'JSON'
}
```

Once instantiated, the `SecretManager` fetches, decrypts, and returns the secrets as a dictionary. It’s used only at service startup and then the SecretManager instance and secrets are discarded.

---

## 🔁 Key Lifecycle Hygiene

The `recryptonator` handles key rotation automatically. Deployed as a Kubernetes CronJob (e.g. once per month at 3:00 AM), it:

1. Fetches the current ciphertext from Kubernetes
2. Decrypts it via Vault Transit
3. Rotates the transit key in Vault
4. Re-encrypts the secret with the new key
5. Pushes the updated ciphertext to the same Kubernetes secret

This prevents secrets from being coupled to a long-lived encryption key—a common failure point in traditional secret systems.

---

## 📚 Failing Forward: A Brief History

This approach evolved through several failed—but educational—attempts:

1. **Secrets in image**: insecure but good for initial development
2. **Bundled encrypted SecureDicts**: no plaintext secrets, but bundled keys
3. **Single unified secret in K8s**: fast, but leaky
4. **Env-based YAML config**: simple, not secure
5. **This**: Vault Transit + K8s + short-lived auth + auto key rotation = ✨ peace of mind

---

## 🔗 Related Resources

- [[SecretManager GitHub Repo](https://github.com/dekeyrej/secretmanager)](https://github.com/dekeyrej/secretmanager)
- [[Encryptionator](https://github.com/dekeyrej/secretmanager/tree/main/examples/encryptonator)](https://github.com/dekeyrej/secretmanager/tree/main/examples/encryptonator)
- [[KubeVault Example](https://github.com/dekeyrej/secretmanager/tree/main/examples/kubevault-example.py)](https://github.com/dekeyrej/secretmanager/tree/main/examples/kubevault-example.py)
- [[Recryptonator](https://github.com/dekeyrej/secretmanager/tree/main/examples/recryptonator)](https://github.com/dekeyrej/secretmanager/tree/main/examples/recryptonator)
