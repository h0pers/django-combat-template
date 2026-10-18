# Build and run your first project

In this tutorial, you generate a project from the template, start it on your machine, create a poll through its REST API, look at it in the Django admin and run the test suite. At the end, you have a working project to build on.

## Before you begin

You need:

- [uv](https://docs.astral.sh/uv/getting-started/installation/)
- [Docker](https://docs.docker.com/get-docker/) with Compose v2. Docker Desktop, Colima and OrbStack all work.
- git
- Nothing listening on port 80 on your machine

This tutorial uses the default options, which include Django REST Framework.

## Generate the project

1. Run Cookiecutter against the template:

   ```bash
   uvx cookiecutter gh:h0pers/django-combat-template
   ```

2. Press **Enter** at every prompt to accept the defaults.

   Cookiecutter creates a `my-django-project` directory, locks the dependencies with uv and makes the first git commit. The last lines of the output list the files in that commit:

   ```text
    create mode 100644 website/website/urls.py
    create mode 100644 website/website/wsgi.py
   ```

3. Go into the project and create its environment file from the example:

   ```bash
   cd my-django-project
   cp .env.example .env
   ```

## Start the stack

1. Build and start the development stack:

   ```bash
   docker compose -f docker-compose.debug.yml up --build
   ```

   The first build takes a few minutes. The stack keeps running in this terminal and prints its logs here.

   On start, the backend creates the database tables, collects the static files and creates an admin user from the `DJANGO_SUPERUSER_*` values in `.env`. Wait until the logs show:

   ```text
   backend-1  | Superuser created successfully.
   backend-1  | Watching for file changes with StatReloader
   ```

2. Open a second terminal in `my-django-project` and check that the backend responds:

   ```bash
   curl http://localhost/api/health/
   ```

   ```json
   {"status":"ok"}
   ```

## Create a poll through the API

1. Send a poll with two choices:

   ```bash
   curl -X POST http://localhost/api/v1/polls/ \
     -H "Content-Type: application/json" \
     -d '{"question": "Tabs or spaces?", "choices": ["Tabs", "Spaces"]}'
   ```

   The API returns the new poll. Your `created_at` value differs:

   ```json
   {"id":1,"question":"Tabs or spaces?","created_at":"2026-10-17T18:53:09.336581Z","choices":[{"id":1,"text":"Tabs"},{"id":2,"text":"Spaces"}]}
   ```

2. Send a poll with only one choice:

   ```bash
   curl -X POST http://localhost/api/v1/polls/ \
     -H "Content-Type: application/json" \
     -d '{"question": "Only one?", "choices": ["Yes"]}'
   ```

   The API rejects it with status 400:

   ```json
   {"message":"Validation error","extra":{"fields":{"choices":["Ensure this field has at least 2 elements."]}}}
   ```

   Every error from the API has this `message` and `extra` shape. {doc}`explanation/code-layers` explains where it comes from.

3. Open <http://localhost/api/docs/> in your browser. Swagger UI lists the `polls` endpoints, and you can send requests from there.

## Look at the poll in the admin

1. Open <http://localhost/admin/>.
2. Log in with username `admin` and password `admin`.
3. Click **Polls**. The poll "Tabs or spaces?" is in the list.

## Run the tests

1. Run the test suite:

   ```bash
   make test
   ```

   The first run builds a test image. The output ends with:

   ```text
   ============================== 19 passed in 0.52s ==============================
   ```

   If the output shows `ModuleNotFoundError` instead, an older `backend:test` image from another project is in the way. Run `make test-image`, then `make test` again.

2. Stop the test database and cache:

   ```bash
   make test-down
   ```

## Stop the stack

1. In the first terminal, press **Ctrl+C**.
2. Remove the containers:

   ```bash
   docker compose -f docker-compose.debug.yml down
   ```

   Your database is kept in a Docker volume, so the poll is still there the next time you start the stack. On later starts, the backend skips migrations that are already applied and doesn't create another admin user.

## What you've done

You generated a project, ran it with hot reload, created data through its API, saw how it reports errors, and ran its tests.

Next:

- To put the project online, follow {doc}`how-to/deploy-to-a-vps`.
- To add your own models, follow {doc}`how-to/add-an-app`.
- To understand how the code is organized, read {doc}`explanation/code-layers`.
