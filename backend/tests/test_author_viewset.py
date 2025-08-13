import pytest
from django.urls import reverse
from rest_framework import status

from users.models import UserTypes
from journal.models import ApprovalStatus


@pytest.mark.django_db
class TestAuthorAPI:

    def make_user(self, user_factory, role_str):
        """
        Создаёт и возвращает пользователя с правильным user_type.
        """
        # Получаем значение поля (строку или число) из Enum
        user_type_value = getattr(UserTypes, role_str).value
        print("user_type_value = ", user_type_value)

        user = user_factory(username=f'user_{role_str.lower()}')
        user.user_type = user_type_value
        user.save()

        print("Сохранили пользователя = ", user, "c типом = ", user.user_type)

        return user

    @pytest.mark.parametrize('role_str,expected_status', [
        ('READER',     status.HTTP_403_FORBIDDEN),
        ('JOURNALIST', status.HTTP_201_CREATED),
        ('STAFF',      status.HTTP_201_CREATED),
        ('ADMIN',      status.HTTP_201_CREATED),
    ])
    def test_create_author_permissions(self, api_client, user_factory, role_str, expected_status):
        print("role = ", role_str)
        user = self.make_user(user_factory, role_str)
        print("user = ", user)
        api_client.force_authenticate(user=user)

        url = reverse('journal:authors-list')
        print("url = ", url)
        payload = {
            'first_name': 'New',
            'last_name':  'Author',
            'status':     ApprovalStatus.PENDING,
        }
        response = api_client.post(
            url,
            payload,
            content_type='application/json'
        )
        print("response = ", response)
        assert response.status_code == expected_status

        if expected_status == status.HTTP_201_CREATED:
            data = response.json()
            assert data['first_name'] == 'New'
            assert data['last_name']  == 'Author'
            assert data['status']     == ApprovalStatus.PENDING

    @pytest.mark.parametrize('role_str,expected_status', [
        ('READER',     status.HTTP_200_OK),
        ('JOURNALIST', status.HTTP_200_OK),
        ('STAFF',      status.HTTP_200_OK),
        ('ADMIN',      status.HTTP_200_OK),
    ])
    def test_list_authors_authenticated(self, api_client, user_factory, author, role_str, expected_status):
        user = self.make_user(user_factory, role_str)
        api_client.force_authenticate(user=user)

        url = reverse('journal:authors-list')
        response = api_client.get(url)
        assert response.status_code == expected_status

        # Для аутентифицированных проверяем, что список приходит
        if expected_status == status.HTTP_200_OK:
            data = response.json()
            assert isinstance(data, list)
            assert 'first_name' in data[0]
            assert 'last_name'  in data[0]

    def test_list_authors_unauthenticated(self, api_client, author):
        url = reverse('journal:authors-list')
        response = api_client.get(reverse('journal:authors-list'))
        assert response.status_code == status.HTTP_200_OK

    @pytest.mark.parametrize('role_str,expected_status', [
        ('READER',     status.HTTP_200_OK),
        ('JOURNALIST', status.HTTP_200_OK),
        ('STAFF',      status.HTTP_200_OK),
        ('ADMIN',      status.HTTP_200_OK),
    ])
    def test_retrieve_author_authenticated(self, api_client, user_factory, author, role_str, expected_status):
        user = self.make_user(user_factory, role_str)
        api_client.force_authenticate(user=user)

        url = reverse('journal:authors-detail', args=[author.pk])
        response = api_client.get(url)
        assert response.status_code == expected_status

        if expected_status == status.HTTP_200_OK:
            data = response.json()
            assert data['first_name'] == author.first_name
            assert data['last_name']  == author.last_name

    def test_retrieve_author_unauthenticated(self, api_client, author):
        url = reverse('journal:authors-detail', args=[author.pk])
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK

    @pytest.mark.parametrize('role_str,expected_status', [
        ('READER',     status.HTTP_403_FORBIDDEN),
        ('JOURNALIST', status.HTTP_200_OK),
        ('STAFF',      status.HTTP_200_OK),
        ('ADMIN',      status.HTTP_200_OK),
    ])
    def test_update_author_permissions(self, api_client, user_factory, author, role_str, expected_status):
        user = self.make_user(user_factory, role_str)
        api_client.force_authenticate(user=user)

        url = reverse('journal:authors-detail', args=[author.pk])
        payload = {'first_name': 'Updated'}
        response = api_client.patch(
            url,
            payload,
            content_type='application/json'
        )
        assert response.status_code == expected_status

        if expected_status == status.HTTP_200_OK:
            data = response.json()
            assert data['first_name'] == 'Updated'
            assert data['last_name']  == author.last_name

    @pytest.mark.parametrize('role_str,expected_status', [
        ('READER',     status.HTTP_403_FORBIDDEN),
        ('JOURNALIST', status.HTTP_403_FORBIDDEN),
        ('STAFF',      status.HTTP_204_NO_CONTENT),
        ('ADMIN',      status.HTTP_204_NO_CONTENT),
    ])
    def test_delete_author_permissions(self, api_client, user_factory, author, role_str, expected_status):
        user = self.make_user(user_factory, role_str)
        api_client.force_authenticate(user=user)

        url = reverse('journal:authors-detail', args=[author.pk])
        response = api_client.delete(url)
        assert response.status_code == expected_status
