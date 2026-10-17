from django.db import transaction
from django.db.models import QuerySet

from apps.polls.models import Choice, Poll


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
