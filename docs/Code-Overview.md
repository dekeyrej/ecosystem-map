# The 'Big Picture'

## Code Structure

### Python

1. Libraries:
   1. [Pages](https://github.com/dekeyrej/plain_pages) - provides the base classes for the microservices and the client displays. Depends on SecretManager and DataSourceLib
      1. **ServerPage**: Base class for the microservices
         Handles: 
         - Secret acquisition (via SecretManager, `secretcfg` and `secretdef`)
         - PostgreSQL connection (via DataSourceLib)
         - Redis Connection
         - Health check endpoint (when `prod=True`)
         - Main run loop (`Update()` called at `period` interval)
       2. **DisplayPage**:  Base class for RGB LED display clients.
          Handles:
          - Image rendering (128×64)
          - Posting to hardware
          - Local state management per display type

   2. [SecretManager](https://github.com/dekeyrej/secretmanager) - connects to secret source based on `secretcfg` (dictionary describing secret source type and configuration), and retrieves secrets based on `secretdef` (dictionary describing specific secret location). Supports several different source types. Common usage would be KubeVault for production, and File for local development.
      - File - JSON or YAML
      - Environment - reads environment values (in-place, .env, or somefile.env), returns values requested based on a map (dictionary), as opposed to the entire environment
      - Kubernetes - Secrets or ConfigMaps
      - KubeVault - _AES-256 encrypted_ secrets are stored as Kubernetes Secrets. Using HashiCorp Vault Kubernetes-authorization, Vault Transit Decryption-as-a-Service is applied to the ciphertext to return the secrets
   3. [DataSourceLib](https://github.com/dekeyrej/datasource) - Originally intended to provide consistent microservice behavior across various database types - PostgreSQL, MongoDB, and SQLite (now really just focused on PostgreSQL). Encapsulates connection, reading and writing records structured for the ecosystem.
3. [Microservices](https://github.com/dekeyrej/microservicematrix) - each is a subclass of serverpage, providing (bool) prod, (int) period, (dict) secretcfg, and (dict) secretdef on initialization. ServerPage handles the common plumbing, leaving the microservice subclass responsible for overriding the 'Update' method with the API URL to EXTRACT data from its datasource, and the specific TRANSFORM logic, and then handing the LOAD function back to the base class (which also handles publishing notifications on the Redis 'update' channel.
4. [Matrix Client](https://github.com/dekeyrej/matrixclient) - as the consumer of the microservice data, the client establishes the connections to the database and Redis. The database connection is shared by the instances of DisplayPage (one for each display type). On initialization, each displaypage instance fetches its associated data from the datasource connection updating its internal state. At this point the MatrixClient reads the display configuration from the datasource, writes a 'startup' record to the datasource, and begins cycling through the display types (as defined in the display config).  To keep the data refreshed, the client subscribes to the Redis 'update' channel, and calls each displaypage instance when new data is posted for its data type.
   ```
   [Microservice] → [Postgres]
              ↘︎      ↘︎
            Redis → MatrixClient
                      ↘︎
                 DisplayPage.render()
   ```

### JavaScript

1. [NodeAPIServer](https://github.com/dekeyrej/nodeapiserver) - on startup, the API server reads data from the PostgreSQL database to initialize its internal state. Subscribing to the Redis 'update' channel, it fetches updated data from the database when notified that new data is available. It services API calls based on its internal state. It also provides a downstream Server-Side Event (SSE) endpoint to notify API consumers when updates occur.
2. [Web Display](https://github.com/dekeyrej/nodewebdisplay) - a REACT 'App' that displays data gathered from the API Server, currently:
   - Environment (Air Quality, Current Conditions, Hourly Forecast and Daily Forecast
   - MLB shows scheduled, in-progress, and completed games for the day
   - NFL  shows scheduled, in-progress, and completed games for the week
   
     WebDisplay is SSE-enabled and supports live updates by data type.

   ### GitHub Integration

   All services are containerized and built via GitHub Actions. Initial provisioning of virtual hosts and containers on Proxmox-VE, as well as initial Kubernetes node and vault container configuration handled in [Ansible](https://github.com/dekeyrej/ansible). Production deployments are managed in Kubernetes, with local dev workflows supported via WSL.

[Data Architecture Overview](https://github.com/dekeyrej/ecosystem-map/wiki/Data-Architecture-Overview)