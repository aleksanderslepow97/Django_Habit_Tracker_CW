from rest_framework import serializers

from .models import CustomsUser


class CustomsUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomsUser
        fields = "__all__"
