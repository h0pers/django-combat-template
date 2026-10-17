---
paths:
  - "website/apps/**/tests/**"
---

# Tests

- pytest + pytest-django, function-style tests (`def test_...`), plain `assert`. No `unittest.TestCase` classes.
- Files mirror the code: `test_services.py` for services, `test_api.py` for endpoints, `test_<module>.py` otherwise.
- Any test that touches the database needs `@pytest.mark.django_db`.
- Service tests are the main tests: call the service directly and assert on the database or the returned objects.
- Read methods: assert the query count with the `django_assert_num_queries` fixture so N+1 regressions fail.
- API tests: `rest_framework.test.APIClient`, `reverse("api:<app>:vN:<name>")`, `format="json"` for bodies. Check status codes and the response shape, including the error shape `{"message": ..., "extra": {...}}`. Don't re-test service logic through the API.
- Create test data through services (`PollService.create(...)`), not raw ORM calls, unless the service doesn't exist yet.
- Run one file with `make test ARGS=apps/<app>/tests/test_services.py` (paths relative to `website/`), everything with `make test`.

Reference: `website/apps/polls/tests/` (when present).
