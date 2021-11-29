from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.authtoken.models import Token
from todo.models import Notification
from todo.apis.serializers import NotificationSerializer

User = get_user_model()


class BaseTestSetup(APITestCase):
    fixtures = ["todo/fixtures/dummy_data.json"]

    def setUp(self) -> None:
        self.user = User.objects.get(pk=1)
        self.todo = self.user.tasks.get(pk=1)

    def _make_use_login(self):
        token = Token.objects.get(user__username=self.user.username)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)


class TodoApiTestCases(BaseTestSetup):
    """ test Todo apis"""

    def test_todo_unauthorised_user_access_401(self):
        """test unauthorised user """
        response = self.client.get(reverse("todo:todo-list"))
        self.assertEqual(response.status_code, 401)

    def test_todo_http_get_with_200(self):
        """method test success response of todo api"""
        self._make_use_login()
        response = self.client.get(reverse("todo:todo-list"))
        self.assertEqual(response.status_code, 200)

    def test_todo_http_get_with_200(self):
        """method test success response of todo api"""
        self._make_use_login()
        response = self.client.get(reverse("todo:todo-list"))
        self.assertEqual(response.status_code, 200)
        response_json = response.json()
        self.assertIsNotNone(response_json)

    def test_todo_http_post_with_400(self):
        """method test success response of todo api
            with missing required fields
        """
        self._make_use_login()
        post_data = {
            "title": "test",
        }
        expected_output = {
            "description": [
                "This field is required."
            ]
        }
        response = self.client.post(reverse("todo:todo-list"), data=post_data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), expected_output)

    def test_todo_http_post_with_200(self):
        """test to create with post and mandatory data's"""
        self._make_use_login()
        post_data = {
            "title": "test", "description": "test descriptions"
        }
        expected_output = {
            "title": "test",
            "description": "test descriptions",
            "schedule_at": None,
            "is_completed": False,
            "created_at": "2021-11-25T14:21:55.785129Z",
            "updated_at": "2021-11-25T14:21:55.785189Z",
            "is_deadline_miss": False
        }
        response = self.client.post(reverse("todo:todo-list"), data=post_data)
        self.assertEqual(response.status_code, 201)
        json_response = response.json()
        # match output
        self.assertEqual(json_response['title'], expected_output['title'])
        self.assertEqual(json_response['is_completed'], expected_output['is_completed'])

    def test_todo_http_patch_with_success(self):
        """test patch data with wrong inputs"""
        before_update_values = {
            "is_completed": False,
        }
        self._make_use_login()
        patch_data = {
            "is_completed": True
        }
        self.assertEqual(before_update_values["is_completed"], self.todo.is_completed)
        response = self.client.patch(reverse("todo:todo-detail", args=[self.todo.id]), data=patch_data)
        json_response = response.json()
        self.assertTrue(json_response["is_completed"])

    def test_todo_http_patch_with_failure(self):
        """test patch data with wrong inputs"""
        self._make_use_login()
        patch_data = {
            "is_completed": True
        }
        expected_data = {
            "is_completed": True,
        }
        response = self.client.patch(reverse("todo:todo-detail", args=[self.todo.id]), data=patch_data)


class TestNotificationApi(BaseTestSetup):
    """test notification Api"""

    def test_notification_with_post(self):
        """try to post data"""
        # 405 is used to no method allow
        self._make_use_login()
        response = self.client.post(reverse("todo:notifications-list"))
        self.assertEqual(response.status_code, 405)

    def test_notification_with_unauthenticated(self):
        """try unauthenticated user"""
        response = self.client.post(reverse("todo:notifications-list"))
        self.assertEqual(response.status_code, 401)

    def test_notification_get_with_user(self):
        """try match user notification with apis"""
        user_notifications = Notification.objects.filter(user=self.user)
        serialize_data = NotificationSerializer(many=True, data=user_notifications)
        serialize_data.is_valid()
        self._make_use_login()
        response = self.client.get(reverse("todo:notifications-list"))
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(str(serialize_data.data), str(response.json()))
