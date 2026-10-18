# Tune Gunicorn

This guide shows you how to change the number of Gunicorn workers and the request timeout on one server. These settings depend on the server's CPU and memory, so CI doesn't deploy them.

Without any change, Gunicorn starts `(2 × CPU cores) + 1` workers, counting the cores the container can see, with a 60-second timeout. Lower the worker count on servers with little memory, or when the container is limited to fewer CPUs than the host has.

1. On the server, in the app directory, create `docker-compose.override.yml`:

   ```yaml
   services:
     backend:
       environment:
         - "GUNICORN_WORKERS=5"
         - "GUNICORN_TIMEOUT=60"
   ```

2. Check the database connection budget. Each worker keeps its own pool of up to `DJANGO_DB_POOL_MAX_SIZE` connections, `4` by default. Keep this number below PostgreSQL's `max_connections`, which is `100` by default:

   ```text
   workers × DJANGO_DB_POOL_MAX_SIZE × servers
   ```

   For example, 5 workers on one server use up to 20 connections.

3. Apply the change without downtime:

   ```bash
   docker rollout backend
   ```

4. Check the processes in the backend container:

   ```bash
   docker compose top backend
   ```

   The list shows one Gunicorn master process and one process for each worker.

Docker Compose merges the override file automatically, and deploys never overwrite it.
