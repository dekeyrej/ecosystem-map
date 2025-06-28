# The 'Big Picture'

## Code Structure

### Python

1. Libraries:
   1. [Pages](https://github.com/dekeyrej/plain_pages) - provides the base classes for the microservices and the client displays. Depends on SecretManager and DataSourceLib
      1. ServerPage - Base class for the microservices - encapsulates most of the required plumbing
         - Acquire the necessary 'secrets' - Depends on SecretManager. secretcfg and secretdef dictionaries on initialization.
         - Connects to the database - Depends on DataSourceLib
         - Connects to redis
         - When running in Production (inside the Kubernetes cluster) establishes/monitors the health port. 'prod' value on initilization.
         - Provides the main run loop which calls the 'Update' function as overridden by the specific microservice. Update 'period' value on initialization.
       2. DisplayPage - Base class for each of the individual RGB LED displays.  It provides the plumbing and 'fittings' necessary to render information as a 128x64 image, and post it to the physical hardware. It also holds the current state data for its initialized display type.
   2. [SecretManager](https://github.com/dekeyrej/secretmanager) - 'connects' to secret source based on 'secretcfg' dictionary, and retrieves secrets based on 'secretdef' dictionary. Supports several different source types. Common usage would be KubeVault for production, and File for local development. The source type and the specific secret source are provided in 2 dictionaries - secretcfg (secret source type and configuration), and secretdef (specific secret location)
      - File - JSON or YAML
      - Environment - reads environment values (in-place, .env, or <somefile>.env), returns values requested based on a map (dictionary), as opposed to the entire environment
      - Kuberenetes - Secrets or ConfigMaps
      - KubeVault - _ASE-256 encrypted_ secrets are stored as Kubernetes Secrets. Using Hasicorp Vault Kubernetes-authorization, Vault Transit Decryption-as-a-Service is applied to the ciphertext to return the secrets
   3. [DataSourceLib](https://github.com/dekeyrej/datasource) - Originally intended to provide consistent microservice behavior across various database types - PostgreSQL, MongoDB, and SQLite (now really just focused on PostgreSQL). Encapsulates connection, reading and writing records structured for the ecosystem.
3. [Microservices](https://github.com/dekeyrej/microservicematrix) - each is a subclass of serverpage, providing (bool) prod, (int) period, (dict) secretcfg, and (dict) secretdef on initialization. ServerPage handles the common plumbing, leaving the microservice subclass responsible for overriding the 'Update' method with the API URL to EXTRACT data from its datasource, and the specific TRANSFORM logic, and then handing the LOAD function back to the base class (which also handles publishing notifications on the redis 'update' channel.
4. [Matrix Client](https://github.com/dekeyrej/matrixclient) - as the consumer of the microservice data, the client establishes the connections to the database and redis. The database connection is shared by the instances of DisplayPage (one for each display type). On initialization, each displaypage instance fetched its associated data from the datasource connection updating its internal state. At this point the MatrixClient reads the display configuration from the datasource, writes a 'startup' record to the datasource, and begins cycling through the display types (as defined in the display config).  To keep the data refreshed, the client subscribes to the redis 'update' channel, and calls each displaypage instance when new data is posted for its data type.

### JavaScript

1. [NodeAPIServer](https://github.com/dekeyrej/nodeapiserver) - on startup, the API server reads data from the PostgreSQL database to initialize its internal state. Subscribing to the redis 'update' channel, it fetches updated data from the database when notified tha new data is available. It services API calls based on its internal state. It also provides a downstream Server-Side Event (SSE) endpoint to notify API consumers when updates occur.
2. [Web Display](https://github.com/dekeyrej/nodewebdisplay) - a REACT 'App' that displays one of its views of data gathered from the API Server, currently:
   - Environment (Air Quality, Current Conditions, Hourly Forecast and Daily Forecast
   - MLB shows scheduled, in-progress, and completed games for the day
   - NFL  shows scheduled, in-progress, and completed games for the week
   
   The Webdisplay subscribes to the SSE endpoint provided by the API server, and dynamically updates the display currently in view

   ### GitHub Integration

   All services are containerized and built via GitHub Actions. Initial provisioning of virtual hosts and containers on Proxmox, as well as initial kubenetes node and vault configuration handled in Ansible. Production deployments are managed in Kubernetes, with local dev workflows supported via WSL.
