---
paths:
  - "website/apps/**/api/**"
  - "website/website/api.py"
---

# API layer (DRF)

- `api/vN/` holds `views.py`, `serializers.py`, `urls.py`, `schema.py` and `docstring.py`. Nothing in `api/` queries the ORM: views call the app's service.
- Serializers live in `serializers.py`, never nested inside views. `ModelSerializer` with an explicit `fields` list, one field per line, never `"__all__"`. Input fields that aren't model fields (e.g. a `ListField` of strings) are declared on the serializer with their own validation.
- Validation happens here, in the serializer: `min_length`, `max_length`, `validate_<field>()`, `validate()`.
- One DRF generic view per URL: `ListCreateAPIView` for `items/`, `RetrieveUpdateDestroyAPIView` for `items/<id>/`. Name it after the generic with the entity prefix and an `API` suffix (`PollListCreateAPI`, `PollRetrieveUpdateDestroyAPI`).
- Route every database access through the service by overriding:
  - `get_queryset()` → the service's read method. Detail views set `lookup_url_kwarg` (e.g. `"poll_id"`) and let DRF's `get_object()` filter that queryset and check object permissions; don't override `get_object()`.
  - `create()` / `update()` → `serializer.is_valid(raise_exception=True)`, then the service with `**serializer.validated_data`, then render with the output serializer
  - `perform_destroy()` → the service's delete method
- Never call `serializer.save()` and never rely on the default `perform_create()` / `perform_update()`.
- `get_serializer_class()` returns the input serializer for writes and the output serializer for reads.
- `@api_view` only for trivial endpoints without models (e.g. `health`).
- OpenAPI: add an `extend_schema(...)` object to `schema.py` (summary, `description=docstring.X`, `tags`, and `responses` when the output serializer differs from the input one), put the text in `docstring.py`, attach with `@extend_schema_view(get=..., post=...)`.
- Register URLs in `api/vN/urls.py` (`app_name = "vN"`); a new app also needs `api/urls.py` (`app_name = "<app>"`) included in `website/website/api.py`. Reverse as `api:<app>:vN:<name>`.
- Errors: raise app errors in services; the exception handler renders `{"message": ..., "extra": {...}}`. Don't build error responses by hand.
- Every endpoint gets tests in `tests/test_api.py`.

Reference: `website/apps/polls/api/v1/` and the "API" section of `docs/architecture.md`. Use the `add-endpoint` skill for a new endpoint.
