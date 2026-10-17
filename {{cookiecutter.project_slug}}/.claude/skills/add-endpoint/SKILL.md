---
name: add-endpoint
description: Add a DRF API endpoint the project's way - ModelSerializers in serializers.py, one generic view per URL (ListCreateAPIView / RetrieveUpdateDestroyAPIView) that routes all database access through the app's service, OpenAPI schema, URL and API tests. Use when the user asks for a new endpoint, route, or to expose a model over the API.
argument-hint: "<app> <Entity>"
---

# Add an API endpoint

Arguments: `$ARGUMENTS` (app, then entity, e.g. `polls Poll`). The service methods must exist first; if not, run the `add-service` skill. Copy the style of `website/apps/polls/api/v1/` when it exists.

All files below are in `website/apps/<app>/api/v1/`.

## 1. Serializers (`serializers.py`)

```python
class PollSerializer(serializers.ModelSerializer):
    choices = ChoiceSerializer(many=True)

    class Meta:
        model = Poll
        fields = [
            "id",
            "question",
            "created_at",
            "choices",
        ]


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

- Output serializer for reads, input serializer for writes. Explicit `fields`, one per line, never `"__all__"`.
- All input validation goes here.

## 2. Views (`views.py`)

Collection URL (`polls/`):

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

Detail URL (`polls/<int:poll_id>/`):

```python
@extend_schema_view(
    get=retrieve_poll_schema,
    put=update_poll_schema,
    delete=destroy_poll_schema,
)
class PollRetrieveUpdateDestroyAPI(generics.RetrieveUpdateDestroyAPIView):
    lookup_url_kwarg = "poll_id"
    http_method_names = [
        "get",
        "put",
        "delete",
        "head",
        "options",
    ]

    def get_serializer_class(self):
        if self.request.method == "PUT":
            return PollUpdateSerializer
        return PollSerializer

    def get_queryset(self):
        return PollService.get_all()

    def update(self, request: Request, *args, **kwargs) -> Response:
        serializer = self.get_serializer(self.get_object(), data=request.data)
        serializer.is_valid(raise_exception=True)

        poll = PollService.update(poll=serializer.instance, **serializer.validated_data)

        return Response(PollSerializer(poll).data)

    def perform_destroy(self, instance: Poll) -> None:
        PollService.delete(poll=instance)
```

- One generic per URL, named `<Entity><Generic>API`.
- `get_queryset()` always comes from the service. DRF's `get_object()` filters it by `lookup_url_kwarg` and runs object permission checks, so don't override it.
- Writes go through `create()` / `update()` / `perform_destroy()` calling the service with `validated_data`. Never `serializer.save()`.
- Leave out `patch` unless the service supports partial updates (arguments with `None` defaults).
- Only include the generic's methods the user asked for; use `ListAPIView`, `RetrieveAPIView` etc. when fewer operations are needed.

## 3. Schema (`schema.py` and `docstring.py`)

```python
# docstring.py
RETRIEVE_POLL_DOCS = "Get one poll with its choices"

# schema.py
retrieve_poll_schema = extend_schema(
    summary="Retrieve Poll",
    description=docstring.RETRIEVE_POLL_DOCS,
    tags=["Polls"],
)

update_poll_schema = extend_schema(
    summary="Update Poll",
    description=docstring.UPDATE_POLL_DOCS,
    tags=["Polls"],
    responses={
        status.HTTP_200_OK: PollSerializer,
    },
)
```

Add `responses=` whenever the response uses a different serializer than the request.

## 4. URL (`urls.py`)

```python
urlpatterns = [
    path("polls/", PollListCreateAPI.as_view(), name="polls"),
    path("polls/<int:poll_id>/", PollRetrieveUpdateDestroyAPI.as_view(), name="poll"),
]
```

Reverse as `api:<app>:v1:<name>`. If the app has no `api/urls.py` yet, create it as in the `new-app` skill and include it in `website/website/api.py`.

## 5. Tests (`website/apps/<app>/tests/test_api.py`)

```python
@pytest.mark.django_db
def test_retrieve_poll(client):
    poll = PollService.create(question="Favourite colour?", choices=["Red", "Blue"])

    response = client.get(reverse("api:polls:v1:poll", kwargs={"poll_id": poll.id}))

    assert response.status_code == 200
    assert response.data["question"] == "Favourite colour?"


@pytest.mark.django_db
def test_retrieve_missing_poll(client):
    response = client.get(reverse("api:polls:v1:poll", kwargs={"poll_id": 999}))

    assert response.status_code == 404
    assert response.data == {"message": "No Poll matches the given query.", "extra": {}}
```

Cover each method: success status and shape, a validation error (`400`, `extra.fields`), not found (`404`) and app errors (`400`, `message` / `extra`). Use `APIClient` from `rest_framework.test` and `format="json"` for request bodies.

## 6. Finish

`make format`, `make lint`, `make test`. The OpenAPI docs at `/api/docs/` (debug stack) should show the new operations with the right request and response bodies.
