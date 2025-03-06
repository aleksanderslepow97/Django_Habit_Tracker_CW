from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from habit.models import Habit
from users.models import User


class HabitTestCase(APITestCase):

    def setUp(self):
        """Данные для теста(фикстура для теста)."""
        self.user = User.objects.create(email="test@test.com")
        self.habit = Habit.objects.create(
            habit="Тестовая привычка",
            location="Место",
            time_habit="08:00:00",
            action="Действие",
            pleasant_habit=False,
            periodicity=1,
            award="Вознаграждение",
            publicity="Не опубликована",
            owner=self.user,
        )
        self.client.force_authenticate(user=self.user)

    def test_habit_retrieve(self):
        """Тестирование деталей привычки."""
        url = reverse("habit:habit-detail", args=(self.habit.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("habit"), self.habit.habit)

    def test_habit_create(self):
        """Тестирование создания привычки."""
        url = reverse("habit:habit-list")
        data = {
            "habit": "Тестовая привычка11",
            "location": "Место1",
            "time_habit": "09:00:00",
            "action": "Действие1",
            "pleasant_habit": False,
            "periodicity": 1,
            "award": "Вознаграждение1",
            "publicity": "Не опубликована",
            "owner": self.user.pk,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Habit.objects.all().count(), 2)

    def test_habit_update(self):
        """Тестирование изменения привычки."""
        url = reverse("habit:habit-detail", args=(self.habit.pk,))
        data = {"habit": "Тестовая привычка новая", "periodicity": 1}
        response = self.client.patch(url, data)
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("habit"), "Тестовая привычка новая")

    def test_habit_delete(self):
        """Тестирование удаления привычки."""
        url = reverse("habit:habit-detail", args=(self.habit.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(User.objects.all().count(), 1)
