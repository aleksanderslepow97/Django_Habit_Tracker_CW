from django.core.management import BaseCommand
from users.models import CustomsUser


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        user = CustomsUser.objects.create(email="admin@mail.ru")
        user.is_staff = True
        user.is_active = True
        user.is_superuser = True
        user.set_password("852123654")
        user.save()
