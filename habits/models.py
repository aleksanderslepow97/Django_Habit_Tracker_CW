from django.db import models
from config.settings import AUTH_USER_MODEL


class Habit(models.Model):
    """Модель привычки"""

    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True,
                             verbose_name="Пользователь")
    location = models.CharField(max_length=50, default="Где угодно", verbose_name="Место")
    time = models.TimeField(verbose_name="Время")
    action = models.CharField(max_length=50, verbose_name="Действие")
    is_pleasant_habit = models.BooleanField(default=False, verbose_name="Признак приятной привычки")
    related_habit = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True,
                                      verbose_name="Связанная привычка")
    periodicity = models.PositiveIntegerField(default=1, verbose_name="Периодичность в днях")
    award = models.CharField(max_length=50, null=True, blank=True, verbose_name="Вознаграждение")
    execution_time = models.PositiveIntegerField(default=0, verbose_name="Время выполнения (в секундах)")
    is_public = models.BooleanField(default=False, verbose_name="Признак публичности")

    def __str__(self):
        return f"{self.user} - {self.action}"

    class Meta:
        verbose_name = "Привычка"
        verbose_name_plural = "Привычки"
        ordering = ["pk"]
