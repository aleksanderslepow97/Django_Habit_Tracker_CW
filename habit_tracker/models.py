import datetime

from django.db import models
from users.models import CustomsUser


class Habit(models.Model):
    """Модель привычки."""

    OWNER_CHOICES = [
        ("every minutes", "каждую минуту"),  # тестовое значение
        ("every day", "каждый день"),
        ("every other day", "через день"),
        ("every three days", "раз в 3 дня"),
        ("every four days", "раз в 4 дня"),
        ("every five days", "раз в 5 дней"),
        ("every six days", "раз в 6 дней"),
        ("every week", "раз в неделю"),
    ]

    owner = models.ForeignKey(
        CustomsUser,
        related_name="habits",
        on_delete=models.CASCADE,
        verbose_name="Владелец",
        blank=True,
        null=True,
    )
    place = models.CharField(
        max_length=255,
        verbose_name="Место выполнения привычки",
        help_text="Укажите место выполнения привычки",
        blank=True,
        null=True,
    )
    time = models.DateTimeField(
        verbose_name="Время начала выполнения привычки",
        help_text="Выберете дату и время начала привычки",
        blank=True,
        null=True,
    )
    action = models.CharField(
        max_length=255,
        verbose_name="Действие привычки",
        help_text="Опишите действие вашей привычки",
    )
    is_pleasant = models.BooleanField(
        default=False,
        verbose_name="Признак приятной привычки",
        help_text="Привычка является приятной",
    )
    related_habit = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name="Связанная привычка",
        help_text="Выберете связанную приятную привычку",
    )
    periodicity = models.CharField(
        max_length=16,
        choices=OWNER_CHOICES,
        verbose_name="Периодичность выполнения",
        help_text="Выберите периодичность выполнения привычки",
        default="every day",
    )
    reward = models.CharField(
        max_length=255,
        verbose_name="Вознаграждение",
        help_text="Укажите вознаграждение",
        blank=True,
        null=True,
    )
    time_to_complete = models.IntegerField(
        default=1,
        verbose_name="Время выполнения",
        help_text="Укажите предположительное время выполнения привычки в минутах",
    )
    is_public = models.BooleanField(
        default=False,
        verbose_name="Общий доступ",
        help_text="Опубликовать для общего доступа",
    )

    def __str__(self):
        return f"{self.action} by {self.owner} at {self.place}"

    def get_periodicity_timedelta(self):
        if self.periodicity == "every minutes":
            return datetime.timedelta(minutes=1)
        elif self.periodicity == "every day":
            return datetime.timedelta(days=1)
        elif self.periodicity == "every other day":
            return datetime.timedelta(days=2)
        elif self.periodicity == "every three days":
            return datetime.timedelta(days=3)
        elif self.periodicity == "every four days":
            return datetime.timedelta(days=4)
        elif self.periodicity == "every five days":
            return datetime.timedelta(days=5)
        elif self.periodicity == "every six days":
            return datetime.timedelta(days=6)
        elif self.periodicity == "every week":
            return datetime.timedelta(weeks=1)
        else:
            return None
