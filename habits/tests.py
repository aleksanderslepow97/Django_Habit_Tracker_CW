from datetime import time
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from habits.models import Habit
from users.models import User


class HabitTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email="test1@test1.ru",)
        self.habit = Habit.objects.create(time=time(12, 0), action="Полезная привычка", user=self.user)
        self.client.force_authenticate(user=self.user)

    def test_habit_list(self):
        url = reverse("habits:habit_list")
        response = self.client.get(url)
        data = response.json()
        result = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": self.habit.pk,
                    "execution_time": 0,
                    "periodicity": 1,
                    "location": "Где угодно",
                    "time": "12:00:00",
                    "action": "Полезная привычка",
                    "is_pleasant_habit": False,
                    "award": None,
                    "is_public": False,
                    "user": self.user.pk,
                    "related_habit": None,
                }
            ],
        }

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, result)

    def test_habit_retrieve(self):
        url = reverse("habits:habit_retrieve", args=(self.habit.pk,))
        response = self.client.get(url)
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("action"), self.habit.action)

    def test_habit_create(self):
        url = reverse("habits:habit_create")
        data = {
            "time": "12:01:00",
            "action": "Приятная привычка",
            "is_pleasant_habit": True,
            "user": self.user.pk,
        }

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Habit.objects.all().count(), 2)

    def test_habit_update(self):
        url = reverse("habits:habit_create")
        data = {
            "time": "12:01:00",
            "action": "Приятная привычка",
            "is_pleasant_habit": True,
            "user": self.user.pk,
        }

        self.client.post(url, data)
        url = reverse("habits:habit_update", args=(self.habit.pk,))
        data = {"related_habit": Habit.objects.get(action="Приятная привычка").pk}
        response = self.client.patch(url, data)
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("related_habit"), Habit.objects.get(action="Приятная привычка").pk)

    def test_lesson_delete(self):
        url = reverse("habits:habit_delete", args=(self.habit.pk,))
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Habit.objects.all().count(), 0)
