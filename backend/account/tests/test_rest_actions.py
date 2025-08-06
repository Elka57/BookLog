# account/tests/test_rest_actions.py

import uuid
import pytest
from datetime import timedelta
from django.utils import timezone
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from account.models import EmailChangeRequest, PasswordResetRequest

User = get_user_model()


class EmailChangeNegativeTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='neg_tester',
            email='neg@example.com',
            password='pass1234'
        )
        self.client.force_authenticate(user=self.user)

    def test_request_same_email_returns_400(self):
        url = reverse('account:email-change-request')
        resp = self.client.post(
            url, {'new_email': self.user.email}, format='json'
        )

        assert resp.status_code == status.HTTP_400_BAD_REQUEST
        assert 'new_email' in resp.data

    def test_request_invalid_email_format_returns_400(self):
        url = reverse('account:email-change-request')
        resp = self.client.post(
            url, {'new_email': 'not-an-email'}, format='json'
        )

        assert resp.status_code == status.HTTP_400_BAD_REQUEST
        assert 'new_email' in resp.data
        assert resp.data['new_email'][0].code == 'invalid'

    def test_confirm_invalid_token_raises_validation_error(self):
        """
        Некорректный формат UUID вызывает ValidationError на уровне ORM/DRF.
        """
        url = reverse('account:email-change-confirm')
        with pytest.raises(ValidationError):
            self.client.post(url, {'token': 'deadbeef'}, format='json')

    def test_confirm_nonexistent_uuid_returns_404(self):
        """
        Корректный, но несуществующий UUID -> 404.
        """
        token = uuid.uuid4()
        url = reverse('account:email-change-confirm')
        resp = self.client.post(url, {'token': str(token)}, format='json')

        assert resp.status_code == status.HTTP_404_NOT_FOUND

    def test_confirm_expired_token_returns_400(self):
        req = EmailChangeRequest.objects.create(
            user=self.user, new_email='new@example.com'
        )
        # Делаем токен «просроченным» на 5 лет
        req.created_at = timezone.now() - timedelta(days=365 * 5)
        req.save(update_fields=['created_at'])

        url = reverse('account:email-change-confirm')
        resp = self.client.post(
            url, {'token': str(req.token)}, format='json'
        )

        assert resp.status_code == status.HTTP_400_BAD_REQUEST
        # Ответ приходит в detail
        assert 'detail' in resp.data
        assert 'Срок действия' in resp.data['detail']

    def test_confirm_already_used_token_returns_400(self):
        req = EmailChangeRequest.objects.create(
            user=self.user, new_email='new2@example.com'
        )
        req.used = True
        req.save(update_fields=['used'])

        url = reverse('account:email-change-confirm')
        resp = self.client.post(
            url, {'token': str(req.token)}, format='json'
        )

        assert resp.status_code == status.HTTP_400_BAD_REQUEST
        assert resp.data.get('detail') == 'Запрос уже выполнен'


class PasswordResetNegativeTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='pwd_tester',
            email='pwd@example.com',
            password='old_pass'
        )

    def test_request_nonexistent_email_returns_400(self):
        url = reverse('account:password-reset-request')
        resp = self.client.post(
            url, {'email': 'noone@nowhere.com'}, format='json'
        )

        assert resp.status_code == status.HTTP_400_BAD_REQUEST
        assert 'email' in resp.data

    def test_confirm_with_mismatched_passwords_returns_400(self):
        reset = PasswordResetRequest.objects.create(user=self.user)

        url = reverse('account:password-reset-confirm')
        data = {
            'token': str(reset.token),
            'new_password': 'abc12345',
            're_new_password': 'xyz98765',
        }
        resp = self.client.post(url, data, format='json')

        assert resp.status_code == status.HTTP_400_BAD_REQUEST
        assert 're_new_password' in resp.data

    def test_confirm_invalid_token_returns_400(self):
        url = reverse('account:password-reset-confirm')
        data = {
            'token': 'invalid-token',
            'new_password': 'whatever123',
            're_new_password': 'whatever123',
        }
        resp = self.client.post(url, data, format='json')

        assert resp.status_code == status.HTTP_400_BAD_REQUEST
        assert 'token' in resp.data

    def test_confirm_expired_token_returns_400(self):
        reset = PasswordResetRequest.objects.create(user=self.user)
        # Просрочим его надолго
        reset.created_at = timezone.now() - timedelta(days=365 * 5)
        reset.save(update_fields=['created_at'])

        url = reverse('account:password-reset-confirm')
        data = {
            'token': str(reset.token),
            'new_password': 'new_pass_1',
            're_new_password': 'new_pass_1',
        }
        resp = self.client.post(url, data, format='json')

        assert resp.status_code == status.HTTP_400_BAD_REQUEST

        # Проверяем, что хотя бы в одном из полей есть ошибка
        assert 'token' in resp.data or 'non_field_errors' in resp.data

    def test_confirm_already_used_token_returns_400(self):
        reset = PasswordResetRequest.objects.create(user=self.user)
        url = reverse('account:password-reset-confirm')
        data = {
            'token': str(reset.token),
            'new_password': 'abc12345',
            're_new_password': 'abc12345',
        }

        # Первый запрос должен сработать
        resp1 = self.client.post(url, data, format='json')
        assert resp1.status_code == status.HTTP_200_OK

        # Второй раз — ошибка
        resp2 = self.client.post(url, data, format='json')
        assert resp2.status_code == status.HTTP_400_BAD_REQUEST

        errors = resp2.data.get('token') or resp2.data.get('non_field_errors') or []
        messages = [str(e) for e in errors]
        assert any('уже' in m or 'expired' in m for m in messages)
