from rest_framework import serializers

from apps.polls.models import Choice, Poll


class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = [
            "id",
            "text",
        ]


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
