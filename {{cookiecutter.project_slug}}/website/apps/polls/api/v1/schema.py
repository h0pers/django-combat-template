from drf_spectacular.utils import extend_schema
from rest_framework import status

from apps.polls.api.v1 import docstring
from apps.polls.api.v1.serializers import PollSerializer

list_polls_schema = extend_schema(
    summary="List Polls",
    description=docstring.LIST_POLLS_DOCS,
    tags=["Polls"],
)

create_poll_schema = extend_schema(
    summary="Create Poll",
    description=docstring.CREATE_POLL_DOCS,
    tags=["Polls"],
    responses={
        status.HTTP_201_CREATED: PollSerializer,
    },
)
