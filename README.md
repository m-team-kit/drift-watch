# Drift Detection

- [ ] Add gitlab/github actions, depends on final repository location.

# Detector container

A container to run a script that runs drift detection on a given dataset.
The script is a placeholder for the drift detection framework.

- [ ] Is the drift detection framework agnostic to the model type?
- [ ] Implement drift detection to use in "demo-advanced" project:
- [ ] Should the container just run the script? Create template for script?
- [ ] Access real data by accessing the database.

# Monitoring server

A server that monitors drift detection jobs and provides a dashboard
to visualize the results.

Before starting the server, you need to generate the following secrets
on `/secrets` folder:

- app_database_password: Mongo database password.

Once the secrets are generated, you can start the server by running:

```bash
docker compose -f compose.yml -f compose.prod.yml up --build
```

To stop the server, you can run:

```bash
docker compose -f compose.yml -f compose.prod.yml down
```

To test a component you can run compose with the test file, for example:

```bash
docker compose -f compose.yml -f compose.test.yml run --build --rm backend
```

Note that this step does not remove the database, use the stop commands
to remove the database container to clean the persistent volumes.

# Development

## Frontend

A Streamlit dashboard for visualizing feature drift, concept drift, and no drift.
Fetches data from the Flask API using various endpoints.

- [ ] Complete dashboard with all the required features.
- [ ] Add here the features

## Backend

A Flask API that handles drift run data and job status.
Contains swagger documentation (openapi 3.1) for above APIs.
Saves drift run data to a MongoDB database.
Provides endpoints for saving job status and get data with multiple filters.

- [ ] Add pagination to the endpoints to avoid overloading the server.
- [ ] Test in production (call the API from the browser).
- [ ] Test in development (run debugger attached to the container).
- [ ] Add reverse proxy for https and expose API doc.

Create a conda environment, make sure conda is installed
(https://conda.io/docs/user-guide/install/):

```bash
$ conda create --name drift-run python=3.11
$ conda activate drift-run
$ pip install -r backend/requirements.txt
$ pip install -r requirements-dev.txt
$ pip install -r requirements-test.txt
```

To run and debug the backend in local, you can use the following command:

```bash
export FLASK_APP=backend/autoapp:app
python -m flask run <args>
```

You will need to export to the environment the application required variables,
see the file `.env.sample` for the required variables. Additionally you can create
your `.env` file and launch the application using the vscode debugger
configuration at `.vscode/launch.json`.

For testing you need a database running to run the tests, you can use the following
commands to run bring up the database and then run the tests:

```bash
$ docker compose up -d database
$ python -m pytest -x -n=auto tests
```

The repository is configure so vscode can locate the tests and run them using
the debugger. To obtain the test plan you can use the following command:

```bash
python -m pytest --setup-plan tests
```

## Reverse proxy

The application is served using a reverse proxy. Both production and
development environments use https. As ACME/letsencrypt does not support
localhost certificates, on development, self-signed certificates are
required. However, such certificates should not be added to the repository
as they might generate security issues:

https://letsencrypt.org/docs/certificates-for-localhost/#for-native-apps-talking-to-web-apps

The best option is to generate the certificates before running the
application. You can use the following command to generate the certificates:

```bash
$ ./sandbox/generate-certs.sh
```

More information on how to generate self-signed certificates can be found:

https://letsencrypt.org/docs/certificates-for-localhost/#making-and-trusting-your-own-certificates
