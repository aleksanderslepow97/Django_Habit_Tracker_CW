from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from users.models import User


class UserTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email="test1@test1.ru",)
        self.client.force_authenticate(user=self.user)

    def test_user_list(self):
        url = reverse("users:user-list")
        response = self.client.get(url)
        data = response.json()
        result = [{"id": self.user.pk, "email": "test1@test1.ru"}]

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, result)

    def test_user_retrieve(self):
        url = reverse("users:user-detail", args=(self.user.pk,))
        response = self.client.get(url)
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("email"), self.user.email)

    def test_user_create(self):
        url = reverse("users:user-list")
        data = {"email": "test2@test2.ru", "password": "123qwe456rty"}
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.all().count(), 2)

    def test_user_update(self):
        url = reverse("users:user-detail", args=(self.user.pk,))
        data = {"tg_chat_id": 123, "password": "123"}
        response = self.client.patch(url, data)
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("tg_chat_id"), "123")

    def test_lesson_delete(self):
        url = reverse("users:user-detail", args=(self.user.pk,))
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(User.objects.all().count(), 0)
