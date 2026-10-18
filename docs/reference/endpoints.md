# Endpoints

URLs served by a generated project.

| Path | Option | Description |
|---|---|---|
| `/admin/` | Always | Django admin. |
| `/api/health/` | Always | Liveness check. `GET` returns `{"status":"ok"}` with status 200 while the app runs. Doesn't check the database or Redis. Used by the container health check. |
| `/api/health/ready/` | Always | Readiness check. `GET` checks PostgreSQL and Redis. Returns `{"status":"ok"}` with status 200, or `{"status":"error"}` with status 503 if one of them is down. The failed check is logged, not returned. For load balancers and uptime monitors. |
| `/api/v1/polls/` | `use_drf=y` | Example API. See [Polls API](#polls-api). |
| `/api/schema/` | `use_drf=y` | OpenAPI schema. Only when `DEBUG` is on. |
| `/api/docs/` | `use_drf=y` | Swagger UI. Only when `DEBUG` is on. |
| `/app/` | `use_vue=y` | Vue single-page app. `/` redirects here. |
| `/cms/` | `use_wagtail=y` | Wagtail admin. |
| `/documents/` | `use_wagtail=y` | Wagtail documents. |
| `/` | `use_wagtail=y` | Wagtail pages. With `use_vue=y` as well, `/` redirects to `/app/` and Wagtail serves the other paths. |
| `/static/` | Always | Static files. Served by Nginx in production, unless files are stored in S3. |
| `/media/` | Always | Uploaded files. Served by Nginx in production, unless files are stored in S3. |

## Polls API

`GET /api/v1/polls/`
: Lists polls, newest first, 100 per page. Use `?page=<n>` for the next page.

  ```json
  {"count":1,"next":null,"previous":null,"results":[{"id":1,"question":"Tabs or spaces?","created_at":"2026-10-17T18:53:09.336581Z","choices":[{"id":1,"text":"Tabs"},{"id":2,"text":"Spaces"}]}]}
  ```

`POST /api/v1/polls/`
: Creates a poll. `question` is up to 200 characters. `choices` is a list of at least 2 strings, each up to 200 characters. Returns the poll with status 201.

  ```json
  {"question": "Tabs or spaces?", "choices": ["Tabs", "Spaces"]}
  ```

The polls API allows anonymous access. Change `DEFAULT_PERMISSION_CLASSES` in `website/website/settings/components/rest_framework.py` before you use it for real data.

## Error responses

With `use_drf=y`, every API error has the same shape.

| Cause | Status | Body |
|---|---|---|
| `ApplicationError` or a subclass | 400 | `{"message": "<error message>", "extra": {...}}` |
| Validation error | 400 | `{"message": "Validation error", "extra": {"fields": {"<field>": ["<error>"]}}}` |
| `Http404`, `PermissionDenied` and other DRF errors | The error's status | `{"message": "<detail>", "extra": {}}` |
