# Drift Monitoring

A simple to use library to monitor drift detection jobs.

## TODO list

- [ ] Add gitlab/github actions, depends on final repository location.
- [ ] Add frontend to the integration tests and reverse proxy deps.
- [ ] Add database backup and restore services to compose.
- [ ] Add extra utilities to the compose services (Graphana, etc.).

## Drift Monitoring client

A simple to use library to monitor drift detection jobs. Simply create a
context in your script and use the `monitor` function to synchronize the
job status with the monitoring server.

```python
from drift_monitoring import DriftMonitoring

with DriftMonitor(experiment_name, "model_1") as monitor:
    detected, detection_parameters = your_concept_detector()
    monitor.concept(detected, detection_parameters)
    detected, detection_parameters = your_data_detector()
    monitor.data(detected, detection_parameters)
```

### Installation

To install the client, you can use the following command:

```bash
pip install drift-monitor
```

### MyToken

MyToken are special access token that can last for a long time. They are
used to authenticate the client with the server. To create a MyToken, you
can visit [mytoken.data.kit.edu](https://mytoken.data.kit.edu/home#mt).

> We recommend that you create a MyToken that only has access to the
> drift monitoring server.

## Drift Monitoring server

A server that stores drift detection to simplify and monitor jobs.
Provides a dashboard to visualize the results.
The server is composed of multiple components:

- A Mongo database to store the drift detection jobs and data.
- A backend to handle authentication and database interface.
- A frontend to visualize the drift detection jobs.
- A reverse proxy to handle https and expose the API.

### Run in Production

Before starting the server, you need to generate the following secrets
on `/secrets` folder:

- app_database_password: Mongo database password.

Once the secrets are generated, you also need to create and configure the
`.env` file with the required variables. You can use the `.env.sample` file
as a template.

Once all the environment variables and secrets are set, you can start the
server by running:

```bash
docker compose -f compose.yml -f compose.prod.yml up --build
```

This command will start, all containers. Database is stored in a docker
volume, so it will persist between restarts. For the first time, a new
certificate will be generated and stored in `/letsencrypt`, do not share
this folder. Renewal of the certificate is done automatically.

> Due to security issues, it is not possible to run in production mode as
> "localhost". You need to set the `APP_DOMAIN_NAME` to a valid domain name.
> See [edudns](https://edudns.services.fedcloud.eu/) as an example of an
> university domain name.

To stop the server, you can run:

```bash
docker compose down
```

### Run in Development

Secrets are not required for development, the folder `/sandbox` contains
a set of secrets and database items that are automatically loaded when
using `compose.override.yml`. However, it is still required to create
the `.env` file with the required variables and use a valid domain name.

To start the server in development mode, you can run:

```bash
docker compose up --build
```

Certificates are generated automatically, from letsencrypt staging server
to avoid rate limiting. The certificates are NOT mounted and stored in
only in the reverse proxy container.

After the containers are running, you can access when running in development
mode, you need to attache a debugger to the backend and frontend services
to start the python execution.

To stop the server, you can run:

```bash
docker compose down
```

### Integration tests

To test a component you can run compose with the test file, for example:

```bash
docker compose -f compose.yml -f compose.test.yml run --build --rm testing
```

It will run the tests on tests folder with services running as close to
production as possible (except for using a staging certificate). Note that
after testing is complete, the remove step does not stop the rest of services,
to stop all services you can run:

```bash
docker compose down
```
