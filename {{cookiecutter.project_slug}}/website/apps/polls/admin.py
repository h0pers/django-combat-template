from django.contrib import admin

from apps.polls.models import Choice, Poll


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 2


@admin.register(Poll)
class PollAdmin(admin.ModelAdmin):
    list_display = [
        "question",
        "created_at",
    ]
    inlines = [
        ChoiceInline,
    ]
