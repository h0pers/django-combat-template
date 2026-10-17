---
name: add-service
description: Add a model and/or service methods to an existing app the project's way - model with migration, <Entity>Service class doing all database reads and writes, app errors, admin registration and service tests. Use when the user asks to store new data, add business logic, or add a read/write operation.
argument-hint: "<app> <Entity>"
---

# Add a model and its service

Arguments: `$ARGUMENTS` (app, then entity, e.g. `polls Vote`). The app must exist; if not, run the `new-app` skill first.

Read `website/apps/<app>/models.py`, `services.py` and `exceptions.py` before changing them, and copy the style of `website/apps/polls/` when it exists.

## 1. Model (skip if the model exists)

In `website/apps/<app>/models.py`:

```python
from django.db import models


class Vote(models.Model):
    choice = models.ForeignKey("polls.Choice", on_delete=models.CASCADE, related_name="votes")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"Vote for {self.choice_id}"
```

- `related_name` on every relation; `settings.AUTH_USER_MODEL` for user foreign keys.
- No logic in `save()` or signals.

Then `make makemigrations ARGS=<app>`.

## 2. Service

In `website/apps/<app>/services.py`, one class per entity:

```python
from django.db import transaction
from django.db.models import QuerySet
from django.shortcuts import get_object_or_404

from apps.polls.models import Choice, Vote


class VoteService:
    @staticmethod
    def get_all() -> QuerySet[Vote]:
        return Vote.objects.select_related("choice")

    @staticmethod
    def get_by_id(*, vote_id: int) -> Vote:
        return get_object_or_404(Vote.objects.select_related("choice"), pk=vote_id)

    @staticmethod
    @transaction.atomic
    def create(*, choice: Choice) -> Vote:
        return Vote.objects.create(choice=choice)
```

- `@staticmethod` / `@classmethod` only, keyword-only arguments, type hints.
- Database work only: no input validation, no `full_clean()`, no request or HTTP concepts. Validation belongs in the view or serializer.
- `@transaction.atomic` around multi-step writes; `bulk_create` for many rows.
- Load what callers render with `select_related` / `prefetch_related`.

## 3. App errors (only for real database-state rules)

If an operation must be refused because of what's in the database (and the user asked for that rule), add an error to `website/apps/<app>/exceptions.py` and raise it from the service:

```python
class PollsClosedError(PollsError):
    def __init__(self, *, poll_id: int) -> None:
        super().__init__("This poll is closed.", extra={"poll_id": poll_id})
```

Name it `<App><Thing>Error`, subclass the app's `<App>Error`. Don't invent rules.

## 4. Admin

In `website/apps/<app>/admin.py`, register new models with `@admin.register(Model)`; write `list_display` and similar lists one item per line.

## 5. Tests

In `website/apps/<app>/tests/test_services.py`:

```python
import pytest

from apps.polls.services import PollService, VoteService


@pytest.mark.django_db
def test_create_vote():
    poll = PollService.create(question="Favourite colour?", choices=["Red", "Blue"])

    vote = VoteService.create(choice=poll.choices.first())

    assert vote.choice.text == "Red"


@pytest.mark.django_db
def test_get_all_loads_choice(django_assert_num_queries):
    poll = PollService.create(question="Favourite colour?", choices=["Red", "Blue"])
    VoteService.create(choice=poll.choices.first())

    with django_assert_num_queries(1):
        assert [vote.choice.text for vote in VoteService.get_all()] == ["Red"]
```

One test per service method, plus a query-count test for read methods.

## 6. Finish

`make format`, `make lint`, `make test ARGS=apps/<app>/tests/test_services.py`, `make test`, `make migrate-check`. If the data should be exposed over HTTP, continue with the `add-endpoint` skill.
