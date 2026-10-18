# Deploy to a VPS

This guide shows you how to put a generated project on a Linux server, so that every push to `master` deploys it.

## Before you begin

You need:

- A generated project pushed to a GitHub repository
- A Linux VPS you can reach over SSH
- A domain name whose DNS records you can edit

## Prepare the server

The server needs Docker, the [`docker rollout`](https://github.com/wowu/docker-rollout) plugin, a shared Traefik instance and a deploy user.

- **If you want this done for you,** use [vps-infra](https://github.com/h0pers/vps-infra). It's an Ansible collection that sets up an Ubuntu 24.04 server for Django Combat and hardens it. Add your app as a deploy user in its inventory and run the playbook.
- **If you set up the server yourself,** do the following:
  1. Install Docker and the `docker rollout` plugin.
  2. Create an external Docker network named `traefik-public`.
  3. Run Traefik on that network with a `websecure` entrypoint and a Let's Encrypt certificate resolver named `le`.
  4. Create a non-root user in the `docker` group for deploys.

## Point your domain at the server

Create an `A` record for your domain and another for `www`, both pointing at the server's IP address. Traefik redirects `www` to the bare domain.

## Add the GitHub settings

1. In your repository on GitHub, go to **Settings** > **Environments** and create an environment named `production`.
2. In that environment, add the required secrets from {doc}`../reference/github-settings`: `VPS_HOST`, `VPS_USER`, `SSH_PRIVATE_KEY`, `DJANGO_SECRET_KEY`, `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_DB` and `PACKAGES_TOKEN`.
3. Add an environment variable named `MY_DOMAIN` with your domain, for example `example.com`.

## Register the systemd service

The deploy workflow doesn't create the service that starts the app when the server boots, so you register it once.

1. Connect to the server as the deploy user.
2. Run the following, replacing `my-django-project` with your repository name:

   ```bash
   REPO_NAME="my-django-project"
   APP_DIR="$HOME/$REPO_NAME"

   sudo tee /etc/systemd/system/$REPO_NAME.service <<SERVICE
   [Unit]
   Description=$REPO_NAME
   After=docker.service network-online.target
   Requires=docker.service

   [Service]
   Type=oneshot
   RemainAfterExit=yes
   WorkingDirectory=$APP_DIR
   ExecStart=/usr/bin/docker compose up -d
   ExecStop=/usr/bin/docker compose down
   TimeoutStartSec=300

   [Install]
   WantedBy=multi-user.target
   SERVICE

   sudo systemctl daemon-reload
   sudo systemctl enable $REPO_NAME.service
   ```

## Deploy

1. Push to `master`:

   ```bash
   git push origin master
   ```

2. In your repository, open the **Actions** tab. The **CI** workflow runs first. When it succeeds, the **Deploy** workflow starts.
3. When **Deploy** finishes, check the site:

   ```bash
   curl https://example.com/api/health/
   ```

   ```json
   {"status":"ok"}
   ```

From now on, every push to `master` that passes CI is deployed. {doc}`../explanation/deploy-pipeline` describes what happens during a deploy.

## Next steps

- {doc}`store-backups-in-s3`
- {doc}`store-files-in-s3`
- {doc}`tune-gunicorn`
- Point an uptime monitor at `https://example.com/api/health/ready/`. It returns `503` when PostgreSQL or Redis is down.
