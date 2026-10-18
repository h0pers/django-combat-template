# About the code layers

A generated project splits each app into three layers, and dependencies only point down.

```text
views.py / api/vN/views.py   validate input, call a service, shape the output
        │  validated data
        ▼
services.py                  <Entity>Service: every database read and write
        │
        ▼
models.py                    schema, Meta, simple properties
```

Views import services, and services import models. Models never import services. Services never import views, anything from `api/`, or DRF.

## Why views don't touch the database

Django's own tutorial puts queries in views, and many projects put logic in model methods ("fat models"). Both work in small projects. They get harder as more code needs the same operation.

One implementation per operation
: "Create a poll" is needed by the API, the admin, a management command and later a background task. When the logic lives in a view, each caller copies it, and the copies drift apart. A service is the one place all of them call.

API versions stay thin
: `api/v1/` and `api/v2/` differ in serializers, URLs and views. Both call the same services, so a new version never forks the business logic.

Logic is testable without HTTP
: Service tests call `PollService.create(...)` directly, with no client, URL routing or authentication setup.

One transaction boundary
: A multi-step write is wrapped in `@transaction.atomic` inside the service, so it's all or nothing whoever calls it.

Query performance lives in one place
: Read methods return querysets with `select_related` and `prefetch_related` already applied. A view can't add an N+1 query by reaching through relations the service didn't load.

The cost is more files and an extra call for simple operations. The template accepts that cost because the alternative gets more expensive as the project grows.

## What a service looks like

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

Services hold no state, so they're classes of static and class methods that you never instantiate. Arguments are keyword-only, so call sites read clearly. A service knows nothing about HTTP. It works the same from a view, a shell or a test.

## Where validation happens

Input is validated at the edge, before it reaches a service. With DRF, that's the serializer: a `ModelSerializer` takes field rules such as `max_length` from the model, and extra fields declare their own rules. Without DRF, it's a form or explicit checks in the view.

Services trust their input. They don't call `full_clean()` or repeat field checks. They raise errors only for rules that depend on the database, such as voting in a poll that's already closed.

## Why one error hierarchy

```text
ApplicationError            apps/core/exceptions.py
└── PollsError              apps/polls/exceptions.py
    └── PollsClosedError    one specific rule (a hypothetical example)
```

Every business-rule error inherits from `ApplicationError`, so callers can catch one specific error, everything from one app, or everything at once. The app prefix in each name keeps imports from different apps unambiguous.

With DRF, one exception handler turns these errors, validation errors and Django's `Http404` and `PermissionDenied` into the same `{"message": ..., "extra": {...}}` body. Clients parse one error shape for every endpoint. The {doc}`../reference/endpoints` page lists the shapes.

Services raise Django's `Http404` rather than DRF's `NotFound`, because services don't import DRF.

## Why no logic in `save()` or signals

`save()` overrides and signals run implicitly. They're skipped by `bulk_create()` and `QuerySet.update()`, and a reader can't see them at the call site. The template keeps business logic in services, where it's explicit. Signals are still fine for decoupled side effects such as clearing a cache.

## Related

- {doc}`../how-to/add-an-app`
- `docs/architecture.md` and `AGENTS.md` in a generated project apply these rules to the options you picked.
