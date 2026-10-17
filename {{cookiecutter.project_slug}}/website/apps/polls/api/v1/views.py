from drf_spectacular.utils import extend_schema_view
from rest_framework import generics, status
from rest_framework.request import Request
from rest_framework.response import Response

from apps.polls.api.v1.schema import create_poll_schema, list_polls_schema
from apps.polls.api.v1.serializers import PollCreateSerializer, PollSerializer
from apps.polls.services import PollService


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
