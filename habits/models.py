from datetime import timedelta

from django.conf import settings
from django.db import models


class Habit(models.Model):
    """Модель Привычка."""

    habit = models.CharField(
        max_length=250,
        verbose_name="Название привычки.",
        help_text="Укажите название привычки.",
    )
    location = models.CharField(
        max_length=250,
        blank=True,
        null=True,
        verbose_name="Место, в котором необходимо выполнять привычку.",
        help_text="Укажите место, в котором необходимо выполнять привычку.",
    )
    time_habit = models.TimeField(
        blank=True,
        null=True,
        verbose_name="Время, когда необходимо выполнять привычку.",
        help_text="Укажите время, когда необходимо выполнять привычку.",
    )
    action = models.CharField(
        max_length=250,
        blank=True,
        null=True,
        verbose_name="Действие, которое представляет собой привычка.",
        help_text="Укажите действие, которое представляет собой привычка.",
    )
    pleasant_habit = models.BooleanField(
        default=False,
        blank=True,
        null=True,
        verbose_name="Привычка, которую можно привязать к выполнению полезной привычки.",
        help_text="Укажите привычку, которую можно привязать к выполнению полезной привычки.",
    )
    related_habit = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="Привычка, которая связана с другой привычкой.",
        help_text="Укажите привычку, которая связана с другой привычкой.",
        related_name="related_habits",  # Уникальное имя для обратного запроса
    )
    periodicity = models.PositiveSmallIntegerField(
        default=1,
        blank=True,
        null=True,
        verbose_name="Периодичность выполнения привычки для напоминания в днях.",
        help_text="Укажите периодичность выполнения привычки для напоминания в днях.",
    )
    award = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        verbose_name="Вознаграждение.",
        help_text="Укажите чем Вы себя вознаградите после выполнения привычки.",
    )
    time_to_complete = models.DurationField(
        default=timedelta(seconds=120),
        blank=True,
        null=True,
        verbose_name="Время, которое предположительно Вы потратите на выполнение привычки.",
        help_text="Укажите время, которое предположительно Вы потратите на выполнение привычки.",
    )
    STATUS_PUBLICITY = [
        ("Опубликована", "Опубликована"),
        ("Не опубликована", "Не опубликована"),
    ]
    publicity = models.CharField(
        max_length=20,
        choices=STATUS_PUBLICITY,
        default="Не опубликована",
        verbose_name="Статус опубликования привычки",
        help_text="Укажите хотите ли Вы, чтобы другие пользователи видели Ваши привычки.",
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True
    )

    class Meta:
        verbose_name = "Привычка"
        verbose_name_plural = "Привычки"

    def __str__(self):
        return self.habit
