from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from tasks.models import Task

User = get_user_model()

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {"refresh": str(refresh), "access": str(refresh.access_token)}

class TaskAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="alice", password="pass1234")
        self.user2 = User.objects.create_user(username="bob", password="pass1234")
        self.task1 = Task.objects.create(title="Task 1", description="desc", owner=self.user)
        self.task2 = Task.objects.create(title="Task 2", description="desc2", owner=self.user2, completed=True)

    def test_register(self):
        url = "/api/auth/register/"
        data = {"username": "test", "password": "abc12345"}
        resp = self.client.post(url, data)
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username="test").exists())

    def test_get_tasks_list(self):
        url = "/api/tasks/"
        resp = self.client.get(url)
        # Without token → should fail
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)
        # With token → should succeed
        tokens = get_tokens_for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {tokens['access']}")
        resp2 = self.client.get(url)
        self.assertEqual(resp2.status_code, status.HTTP_200_OK)

    def test_create_task_requires_auth(self):
        url = "/api/tasks/"
        data = {"title": "New Task", "description": "x", "completed": False, "owner_id": self.user.id}

        # Without token → should fail
        resp = self.client.post(url, data, format="json")
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

        # With token → should succeed
        tokens = get_tokens_for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {tokens['access']}")
        resp2 = self.client.post(url, data, format="json")
        self.assertEqual(resp2.status_code, status.HTTP_201_CREATED)

    def test_update_task_owner_only(self):
        url = f"/api/tasks/{self.task1.id}/"

        # Bob tries to update Alice's task → forbidden
        tokens_bob = get_tokens_for_user(self.user2)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {tokens_bob['access']}")
        resp = self.client.patch(url, {"completed": True}, format="json")
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

        # Alice updates her own task → success
        tokens_alice = get_tokens_for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {tokens_alice['access']}")
        resp2 = self.client.patch(url, {"completed": True}, format="json")
        self.assertEqual(resp2.status_code, status.HTTP_200_OK)
        self.task1.refresh_from_db()
        self.assertTrue(self.task1.completed)
