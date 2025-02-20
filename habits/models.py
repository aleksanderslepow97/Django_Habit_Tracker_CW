from django.db import models

from config.settings import NULLABLE
from habits.validators import (validate_duration, validate_habit_execution,
                               validate_periodicity, validate_pleasant_habit,
                               validate_related_habit_pleasant,
                               validate_reward_and_related_habit)
from users.models import User


class Habit(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="user",
        verbose_name="Создатель",
        help_text="Укажите создателя привычки",
    )
    action = models.CharField(
        max_length=255, verbose_name="Действие", help_text="Укажите действие"
    )
    time = models.TimeField(verbose_name="Время", help_text="Укажите время")
    place = models.CharField(
        max_length=255, verbose_name="Место", help_text="Укажите место"
    )
    reward = models.CharField(
        max_length=255,
        **NULLABLE,
        verbose_name="Награда",
        help_text="Укажите вознаграждение"
    )
    pleasant_habit = models.BooleanField(
        default=False,
        verbose_name="Приятная привычка",
        help_text="Признак приятной привычки",
    )
    related_habit = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        **NULLABLE,
        related_name="related_habits",
        verbose_name="Связанная привычка",
        help_text="Укажите связанную привычку"
    )
    periodicity = models.PositiveIntegerField(
        default=1, verbose_name="Периодичность", help_text="Укажите период повторения"
    )
    duration = models.PositiveIntegerField(
        null=False,
        verbose_name="Продолжительность",
        help_text="Укажите продолжительность",
    )
    is_public = models.BooleanField(
        default=False, verbose_name="Публичность", help_text="Признак публичности"
    )

    def __str__(self):
        return self.action

    class Meta:
        verbose_name = "Привычка"
        verbose_name_plural = "Привычки"

    def clean(self):
        validate_reward_and_related_habit(self)
        validate_duration(self)
        validate_related_habit_pleasant(self)
        validate_pleasant_habit(self)
        validate_periodicity(self)
        validate_habit_execution(self)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
