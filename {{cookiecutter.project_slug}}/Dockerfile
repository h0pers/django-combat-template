FROM ghcr.io/astral-sh/uv:python3.14-alpine AS base

ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_PROJECT_ENVIRONMENT=/opt/venv \
    VIRTUAL_ENV=/opt/venv \
    PATH="/opt/venv/bin:$PATH"

FROM base AS deps-base

RUN apk --no-cache add python3-dev libpq-dev

COPY pyproject.toml uv.lock ./

FROM deps-base AS deps

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-install-project --no-default-groups

FROM deps-base AS deps-test

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-install-project --no-default-groups --group test

FROM deps-base AS deps-dev

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-install-project --group dev

FROM base AS runtime

ENV USER=user \
    USER_UID=1001 \
    PROJECT_NAME=website \
    DJANGO_BASE_DIR=/usr/src/website \
    GUNICORN_PORT=8000 \
    GUNICORN_LOG_LEVEL=info \
    DJANGO_STATIC_ROOT=/var/www/static \
    DJANGO_MEDIA_ROOT=/var/www/media

RUN apk add --no-cache su-exec libpq-dev && \
    adduser -s /bin/sh -D -u $USER_UID $USER

WORKDIR $DJANGO_BASE_DIR

COPY docker-cmd.sh docker-release.sh /
COPY $PROJECT_NAME $DJANGO_BASE_DIR

RUN chmod +x /docker-cmd.sh /docker-release.sh && \
    mkdir -p $DJANGO_STATIC_ROOT $DJANGO_MEDIA_ROOT && \
    chown -R $USER:$USER $DJANGO_BASE_DIR $DJANGO_STATIC_ROOT $DJANGO_MEDIA_ROOT

CMD ["/docker-cmd.sh"]

EXPOSE $GUNICORN_PORT

FROM runtime AS development

COPY --from=deps-dev /opt/venv /opt/venv

FROM runtime AS test

COPY --from=deps-test /opt/venv /opt/venv
{%- if cookiecutter.use_vue == "y" %}

FROM node:22-alpine AS frontend-build
WORKDIR /app/frontend
COPY frontend/package.json frontend/package-lock.json ./
RUN npm ci
COPY frontend/ /app/frontend/
COPY website/apps/ /app/website/apps/
COPY website/templates/ /app/website/templates/
RUN npm run build
{%- endif %}

FROM runtime AS production

COPY --from=deps /opt/venv /opt/venv
{%- if cookiecutter.use_vue == "y" %}
COPY --chown=$USER:$USER --from=frontend-build /app/website/static/dist $DJANGO_BASE_DIR/static/dist/
{%- endif %}
