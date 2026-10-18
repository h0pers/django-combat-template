# About scaling

A generated project runs on one server. This page explains how it grows past that server: which parts the template already prepares, and which decisions it leaves to you.

## Scale up first

A bigger VPS is the cheapest way to get more capacity. Gunicorn starts `(2 × CPU cores) + 1` workers by default, so a server with more cores runs more workers without any change. Adding servers brings a load balancer, shared storage and more ways to fail. It pays off when one server can't keep up, or when you need the app to survive losing a server.

## What makes the app ready for more servers

Requests can go to any backend container on any server only when no container keeps state of its own. The template keeps state out of the containers.

Sessions
: Sessions use the `cached_db` backend. They're read from Redis and written through to PostgreSQL, so every container sees the same sessions, and a Redis restart doesn't log users out.

Files
: By default, uploaded media and static files live in Docker volumes on the server. A second server can't see them. With a bucket configured, both go to S3-compatible storage instead, as in {doc}`../how-to/store-files-in-s3`.

One-off tasks
: Migrations, `collectstatic` and creating the first user run once per deploy in `docker-release.sh`, not in each container. {doc}`deploy-pipeline` explains why.

Database connections
: Each Gunicorn worker keeps a small pool of PostgreSQL connections, using the pool built into Django 5.2 and psycopg. Reusing connections saves the cost of opening one per request. The pool size caps how many connections each worker can hold, so the total is predictable: `workers × DJANGO_DB_POOL_MAX_SIZE × servers` has to stay below PostgreSQL's `max_connections`.

Health checks
: The project has two endpoints with different jobs. `/api/health/` answers as long as the app runs, and it's the container health check. `/api/health/ready/` also checks PostgreSQL and Redis, and returns `503` when one of them is down, so a load balancer can stop sending traffic to that server.

## Why the container health check ignores the database

Docker and orchestrators such as Docker Swarm restart containers that fail their health check. If the container health check included the database, a short database outage would mark every backend container unhealthy at once, and the orchestrator would restart all of them. Restarting doesn't fix the database, and the restarts add load just as it comes back. A health check that only covers the process itself restarts a container only when that container is broken.

The readiness endpoint answers a different question: can this server handle a request right now? Load balancers and uptime monitors ask that question, so they use `/api/health/ready/`. Its response says only `ok` or `error`. The failed check goes to the logs, not to whoever calls the endpoint.

## What the template leaves to you

Running on several servers needs choices that depend on your hosting, so the template doesn't make them.

- **Routing traffic.** Something has to spread requests across servers and replace failed containers: Docker Swarm, Kamal, Kubernetes or a managed load balancer.
- **Moving PostgreSQL and Redis.** Both run next to the app on the first server. With more servers, they move to a server of their own or to a managed service. `postgres` and `postgres-backup` share a volume, so they stay on the same server.
- **PgBouncer.** When the connection budget gets tight, PgBouncer in transaction mode lets many workers share a few database connections. It needs the built-in pool turned off with `DJANGO_DB_POOL=false`, and `DISABLE_SERVER_SIDE_CURSORS` set in the database settings, because transaction mode doesn't support server-side cursors.

## Related

- {doc}`production-stack`
- {doc}`../how-to/tune-gunicorn`
- {doc}`../reference/environment`
