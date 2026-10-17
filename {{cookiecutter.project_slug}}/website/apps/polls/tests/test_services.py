import pytest

from apps.polls.models import Poll
from apps.polls.services import PollService


@pytest.mark.django_db
def test_create_saves_poll_with_choices():
    poll = PollService.create(question="Favourite colour?", choices=["Red", "Blue"])

    assert Poll.objects.get() == poll
    assert list(poll.choices.values_list("text", flat=True)) == ["Red", "Blue"]


@pytest.mark.django_db
def test_get_all_prefetches_choices(django_assert_num_queries):
    PollService.create(question="Favourite colour?", choices=["Red", "Blue"])
    PollService.create(question="Favourite food?", choices=["Pizza", "Sushi"])

    with django_assert_num_queries(2):
        texts = [
            choice.text
            for poll in PollService.get_all()
            for choice in poll.choices.all()
        ]

    assert len(texts) == 4
