import json
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django_celery_beat.models import ClockedSchedule, PeriodicTask
from .models import Habit


@receiver(post_save, sender=Habit)
def schedule_habit_reminder(sender, instance, created, **kwargs):
    """Планирование задачи с учётом времени выполнения привычки"""
    task_name = f'Напоминание о привычке {instance.pk}'

    # удаляем старую задачу
    if not created:
        try:
            task = PeriodicTask.objects.get(name=task_name)
            task.delete()
        except PeriodicTask.DoesNotExist:
            pass

    now = timezone.now()
    habit_time = timezone.datetime.combine(now.date(), instance.time)

    # переводим в осведомлённое если оно наивное
    if timezone.is_naive(habit_time):
        habit_time = timezone.make_aware(habit_time)

    # следующий день
    if habit_time < now:
        habit_time += timezone.timedelta(days=instance.periodicity)

    clocked_schedule, _ = ClockedSchedule.objects.get_or_create(clocked_time=habit_time)

    PeriodicTask.objects.create(
        clocked=clocked_schedule,
        name=task_name,
        task='habits.tasks.send_habit_reminder',
        args=json.dumps([instance.pk]),
        one_off=True,)


# @receiver(post_delete, sender=Habit)
# def delete_habit_reminders(sender, instance, **kwargs):
# """Удаление задач при удалении привычки (типо CASCADE)"""
# tasks = PeriodicTask.objects.filter(name__starswith=f'Напоминание о привычке {instance.pk}')
# tasks.delete()

# P.S(не успел реализовать delete_habit_reminders как хотел через сигналы, времени не хватило()
