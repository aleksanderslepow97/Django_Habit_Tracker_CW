from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from users.models import User


class UserTestCase(APITestCase):
    def setUp(self):
        """Данные для теста(фикстура для теста)."""
        self.user = User.objects.create(
            email="test@test.com",
        )
        self.client.force_authenticate(user=self.user)

    def test_user_retrieve(self):
        """Тестирование деталей пользователя."""
        url = reverse("users:user-detail", args=(self.user.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("email"), self.user.email)

    def test_user_list(self):
        """Тестирование списка пользователей."""
        url = reverse("users:user-list")
        response = self.client.get(url)
        data = response.json()
        result = [
            {"id": self.user.pk, "email": "test@test.com", "tg_chat_id": None},
        ]
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, result)

    def test_user_create(self):
        """Тестирование создания пользователя."""
        url = reverse("users:user-list")
        data = {"email": "test1@test1.com", "password": "123456"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.all().count(), 2)

    def test_user_update(self):
        """Тестирование изменения пользователя."""
        url = reverse("users:user-detail", args=(self.user.pk,))
        data = {"tg_chat_id": "508906"}
        response = self.client.patch(url, data)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("tg_chat_id"), "508906")

    def test_user_delete(self):
        """Тестирование удаления пользователя."""
        url = reverse("users:user-detail", args=(self.user.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(User.objects.all().count(), 0)
