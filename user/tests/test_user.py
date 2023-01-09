from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework.test import APITestCase
from rest_framework import status

from user.serializers import CustomUserSerializer
from user.tests.utils import create_users_list, create_permissions
from user.models.profile import Profile

User = get_user_model()


class CustomUserTestCase(APITestCase):
    """
    Test Cases for :model:`user.CustomUser`.
    """

    all_users_url = reverse('all-users')
    create_user_url = reverse('create-user')

    retrieve_user = 'user'
    delete_user = 'delete-user'
    update_user = 'update-user'

    number_of_users = 4

    @classmethod
    def setUpTestData(cls):
        for index, user in enumerate(
                create_users_list(cls.number_of_users),
                start=1
        ):
            setattr(cls,
                    f'user_{index}',
                    user
                    )

    def setUp(self) -> None:
        self.client.force_login(self.user_1)

    def test_get_all_users(self):
        response = self.client.get(self.all_users_url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(
            len(response.json()),
            self.number_of_users
        )

    def test_user_retrieve(self):
        user = self.user_2
        response = self.client.get(
            reverse(self.retrieve_user, kwargs={'pk': user.pk})
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        response_json = response.json()
        self.assertEqual(
            response_json['username'],
            user.username
        )
        self.assertEqual(
            response_json,
            CustomUserSerializer(user).data
        )

    def test_user_create(self):
        staff_role = create_permissions()[0]
        json = {
            'username': "create_user",
            'email': 'create@user.com',
            'first_name': "create_first",
            "last_name": "create_last",
            "password": "123",
            'staff_role': staff_role.pk
        }
        response = self.client.post(
            self.create_user_url,
            data=json
        )
        response_json = response.json()
        pk = response_json['pk']
        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )
        self.assertEqual(
            response_json,
            CustomUserSerializer(User.objects.get(pk=pk)).data
        )

    def test_profile_create_signal_from_user(self):
        staff_role = create_permissions()[0]
        json = {
            'username': "create_user_signal",
            'email': 'create_user_signal@user.com',
            'first_name': "create_first",
            "last_name": "create_last",
            "password": "123",
            'staff_role': staff_role.pk
        }
        response = self.client.post(
            self.create_user_url,
            data=json
        )
        response_json = response.json()
        pk = response_json['pk']
        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )
        self.assertEqual(
            Profile.objects.filter(user_id=pk).exists(),
            True
        )

    def test_delete_user(self):
        pk = self.user_1.pk
        response = self.client.delete(
            reverse(self.delete_user, kwargs={'pk': pk})
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )
        self.assertEqual(
            User.objects.filter(pk=pk).exists(),
            False
        )

    def test_put_user(self):
        pk = self.user_4.pk

        json = {
            'username': f'user_{pk}',
            'email': f'user{pk}@example.com',
            'password': f'user_{pk}',
            'first_name': f'first_{pk}',
            'last_name': f'second_{pk}',
        }

        response = self.client.put(
            reverse(self.update_user, kwargs={'pk': pk}),
            data=json
        )
        response_json = response.json()

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(
            response_json['last_name'],
            json['last_name'],
        )

    def test_patch_user(self):
        pk = self.user_4.pk

        json = {
            'first_name': f'first_{pk}',
        }
        response = self.client.patch(
            reverse(self.update_user, kwargs={'pk': pk}),
            data=json
        )
        response_json = response.json()
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(
            response_json['first_name'],
            json['first_name'],
        )
