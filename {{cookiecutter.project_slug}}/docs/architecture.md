# Architecture

How the code is layered, what goes where, and why. `AGENTS.md` has the short rules; this file explains them.

## Layers

```
request
  │
  ▼
{%- if cookiecutter.use_drf == "y" %}
api/vN/views.py      presentation: validate input with serializers, call a service, shape the output
{%- else %}
views.py             presentation: validate input, call a service, render the response
{%- endif %}
  │  validated data
  ▼
services.py          <Entity>Service: every database read and write, transactions
  │
  ▼
models.py            schema, Meta, simple properties
```

Dependencies point down only: views import services, services import models. Models never import services, and services never import views{% if cookiecutter.use_drf == "y" %}, anything from `api/` or DRF{% endif %}. Admin actions, management commands{% if cookiecutter.use_wagtail == "y" %}, Wagtail page code{% endif %} and future background tasks call the same services as the views.

## Why views don't touch the database

- **One implementation per operation.** "Create a poll" is needed by the API, the admin, a management command and later a background task. If the logic lives in a view, each caller copies it and the copies drift apart.
{%- if cookiecutter.use_drf == "y" %}
- **API versions stay presentation-only.** `api/v1/` and `api/v2/` differ in serializers, URLs and views. Both call the same services, so a v2 never forks the business logic.
{%- endif %}
- **Logic is testable without HTTP.** Service tests call `PollService.create(...)` directly. No client, no URL routing, no auth setup.
- **One transaction boundary.** A multi-step write is wrapped in `@transaction.atomic` in the service, so it is all-or-nothing whoever calls it.
- **Query performance lives in one place.** The service returns querysets with `select_related` / `prefetch_related` applied. A view can't introduce an N+1 query by reaching through relations it didn't load.
- **Everyone knows where to look.** Reviewers and agents find all database access for an entity in one file.

## Services

```python
class PollService:
    @staticmethod
    def get_all() -> QuerySet[Poll]:
        return Poll.objects.prefetch_related("choices")

    @staticmethod
    @transaction.atomic
    def create(*, question: str, choices: list[str]) -> Poll:
        poll = Poll.objects.create(question=question)
        Choice.objects.bulk_create([Choice(poll=poll, text=text) for text in choices])
        return poll
```

- One `<Entity>Service` class per entity in `apps/<app>/services.py`, made of `@staticmethod` / `@classmethod` methods. Services hold no state, so they are never instantiated.
- Arguments are keyword-only (`*`) and type-hinted, so call sites read `PollService.create(question=..., choices=...)`.
- Services do database work only. Input is already validated by the time it arrives, so there is no `full_clean()` and no re-checking of field rules.
- Services don't know about HTTP: no `request`, no status codes, no `Response`{% if cookiecutter.use_drf == "y" %}, no DRF imports{% endif %}. They must work the same from a view, a shell or a test.
- Reads return querysets with related objects already loaded; callers can still filter or paginate them.

## Validation

Input is validated at the edge, in the view, before a service is called.
{%- if cookiecutter.use_drf == "y" %} For the API that means the serializer: `ModelSerializer` takes field rules (`max_length`, `null`, `choices`) from the model, and extra input fields declare their own rules:

```python
class PollCreateSerializer(serializers.ModelSerializer):
    choices = serializers.ListField(
        child=serializers.CharField(max_length=200),
        min_length=2,
    )

    class Meta:
        model = Poll
        fields = [
            "question",
            "choices",
        ]
```
{%- else %} Use a Django form or explicit checks in the view, then pass clean values to the service.
{%- endif %}

## Errors

Business-rule failures use one exception hierarchy:

```
ApplicationError            apps/core/exceptions.py
└── PollsError              apps/polls/exceptions.py: base for one app
    └── PollsClosedError    one specific rule, named with the app prefix
```

```python
class PollsClosedError(PollsError):
    def __init__(self, *, poll_id: int) -> None:
        super().__init__("This poll is closed.", extra={"poll_id": poll_id})
```

- Every app gets an `<App>Error` base in its `exceptions.py`; specific errors subclass it and carry the app prefix, so imports from other apps stay unambiguous.
- Raise them from services only for rules that depend on database state (voting on a closed poll, a choice that belongs to another poll). Field-level input problems are validation errors and belong in the view.
- Callers can catch a specific error, the app base, or `ApplicationError`.
{%- if cookiecutter.use_drf == "y" %}

The API exception handler (`apps/core/api/exception_handler.py`) gives every error the same shape:

| Raised | Status | Body |
|---|---|---|
| `ApplicationError` and subclasses | 400 | `{"message": "This poll is closed.", "extra": {"poll_id": 1}}` |
| DRF or Django `ValidationError` | 400 | `{"message": "Validation error", "extra": {"fields": {"question": ["..."]}}}` |
| `Http404`, `PermissionDenied`, other DRF errors | their status | `{"message": "Not found.", "extra": {}}` |

Services raise Django's `Http404` (for example via `get_object_or_404`), never DRF's `NotFound`, because they don't import DRF.

## API

```python
@extend_schema_view(get=list_polls_schema, post=create_poll_schema)
class PollListCreateAPI(generics.ListCreateAPIView):
    def get_serializer_class(self):
        if self.request.method == "POST":
            return PollCreateSerializer
        return PollSerializer

    def get_queryset(self):
        return PollService.get_all()

    def create(self, request: Request, *args, **kwargs) -> Response:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        poll = PollService.create(**serializer.validated_data)

        return Response(PollSerializer(poll).data, status=status.HTTP_201_CREATED)
```

- One generic view per URL: `ListCreateAPIView` for `polls/`, `RetrieveUpdateDestroyAPIView` for `polls/<id>/`. Names end in `API`.
- DRF generics give pagination, permissions and schema detection for free. The overridden methods route all database access through the service:
  - `get_queryset()` → the service's read method
  - `create()` / `update()` / `destroy()` → validate with the serializer, then call the service with `validated_data`
- Never rely on the default `perform_create()` / `serializer.save()`: they write to the database directly and skip the service.
- `get_serializer_class()` picks the input serializer for writes and the output serializer for reads. When they differ, render the response with the output serializer explicitly, as above.
- Plain `@api_view` functions are fine for trivial endpoints with no models, like `health`.
- Each `api/vN/` package holds `views.py`, `serializers.py`, `urls.py`, `schema.py` (`extend_schema` objects) and `docstring.py` (description text).
- Start a `v2` only for breaking changes to request or response shapes. A v2 reuses the models and services and only adds new serializers, views and URLs.
{%- endif %}

## Models

- Fields, `Meta` (always set `ordering` when the order matters) and `__str__`.
- Properties are fine for simple values derived from the model's own fields. Anything that queries other tables or writes belongs in a service.
- No business logic in `save()` or signals. They run implicitly, are easy to bypass (`bulk_create`, `update()`) and hide behaviour from the caller. Keep signals for decoupled side effects such as cache invalidation.
- Refer to users with `settings.AUTH_USER_MODEL` in foreign keys and `get_user_model()` in code.

## Where code goes

| Code | Place |
|---|---|
| A new domain (its own models) | a new app in `website/apps/<app>/` |
| Database reads and writes | `apps/<app>/services.py` |
| Business-rule errors | `apps/<app>/exceptions.py` |
{%- if cookiecutter.use_drf == "y" %}
| Request/response shapes | `apps/<app>/api/vN/serializers.py` |
{%- endif %}
| Shared infrastructure (base errors, middleware, health check) | `apps/core/` |
| Pure helpers with no models or app imports | `website/utils/` |
| A setting topic | `website/website/settings/components/<topic>.py`, registered in `settings/__init__.py` |
| One-off deploy steps (migrations, static files, bootstrap data) | `docker-release.sh`, run once per deploy |
| Production server tuning | `website/gunicorn.conf.py` |

## Tests

- Tests live in `apps/<app>/tests/` and mirror the code: `test_services.py`{% if cookiecutter.use_drf == "y" %}, `test_api.py`{% endif %}.
- Service tests are the main ones: call the service, assert on the database. Mark them `@pytest.mark.django_db`.
{%- if cookiecutter.use_drf == "y" %}
- API tests use `APIClient` and check status codes, response shape and that the service ran. They don't re-test business logic.
{%- endif %}
- Guard query counts on reads with pytest-django's `django_assert_num_queries` fixture.
