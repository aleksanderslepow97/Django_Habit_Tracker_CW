from django.contrib import admin

from habits.models import Habit


@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "action",
        "time",
        "place",
        "reward",
        "pleasant_habit",
        "related_habit",
        "periodicity",
        "duration",
        "is_public",
    )
    list_filter = ("action",)
    search_fields = ("action",)
