from django.contrib import admin
from users.models import CustomsUser


@admin.register(CustomsUser)
class CustomsUserAdmin(admin.ModelAdmin):
    list_filter = ("id", "email")
