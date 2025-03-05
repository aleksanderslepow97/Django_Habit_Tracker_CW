from django.core.management import call_command
from django.core.management.base import BaseCommand
from habits.models import Habit
from users.models import User


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        # Удаляем существующие записи
        Habit.objects.all().delete()
        User.objects.all().delete()

        # Добавляем данные из фикстур
        call_command("loaddata", "user_fixture.json", format="json")
        self.stdout.write(self.style.SUCCESS("Пользователи загружены из фикстур успешно"))
        call_command("loaddata", "habit_fixture.json", format="json")
        self.stdout.write(self.style.SUCCESS("Привычки загружены из фикстур успешно"))
