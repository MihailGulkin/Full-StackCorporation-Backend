from django.urls import reverse
from django.contrib.auth import get_user_model

from general.tests.generic import BaseTestCaseGeneric
from general.tests.model_factory import make_user

from user.serializers import CustomUserSerializer
from general.tests.model_factory import make_permission

User = get_user_model()


class CustomUserTestCase(BaseTestCaseGeneric):
    """
    Test Cases for :model:`user.CustomUser`.
    """

    all_objects_url = reverse('all-users')
    create_object_url = reverse('customuser-list')

    retrieve_object_url = 'user'
    delete_object_url = 'delete-user'
    update_object_url = 'update-user'

    make_method = make_user

    serializer_class = CustomUserSerializer
    model_class = User

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

    def test_get_all_users(self):
        self._test_get_all_objects()

    def test_user_retrieve(self):
        self._test_retrieve_object()

    def test_user_create(self):
        # Test user without request, because create endpoint have celery task
        staff_role = make_permission(1)
        json = {
            'username': "create_user",
            'email': 'create@user.com',
            'first_name': "create_first",
            "last_name": "create_last",
            "password": "123",
            'staff_role': staff_role.pk
        }
        serializer = CustomUserSerializer(data=json)
        self.assertEqual(
            serializer.is_valid(),
            True
        )

    def test_delete_user(self):
        self._test_delete_object()

    def test_put_user(self):
        name = 'test_put_user'
        json = {
            'username': f'user_{name}',
            'email': f'user{name}@example.com',
            'password': f'user_{name}',
            'first_name': f'first_{name}',
            'last_name': f'second_{name}',
        }
        self._test_put_object(json)

    def test_patch_user(self):
        name = 'test_patch_user'

        json = {
            'first_name': f'first_{name}',
        }
        self._test_patch_object(json)