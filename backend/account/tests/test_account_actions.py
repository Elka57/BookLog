from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model

from account.models import EmailChangeRequest, PasswordResetRequest

User = get_user_model()

class AccountFlowTest(APITestCase):
    def setUp(self):
        # заводим тестового пользователя
        self.user = User.objects.create_user(
            username='tester', 
            email='tester@example.com', 
            password='pass1234'
        )

        # получаем JWT-токен через простую точку SimpleJWT
        url = reverse('token_obtain_pair')
        resp = self.client.post(url, {
            'username': 'tester', 
            'password': 'pass1234'
        }, format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        
        # сохраняем access-токен и ставим заголовок Authorization
        access = resp.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access}')

    def test_email_change_and_confirm(self):
        # 1) запрос на смену email
        url_req = reverse('account:email-change-request')
        resp = self.client.post(url_req, {
            'new_email': 'x@example.com'
        }, format='json')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        # 2) достаём токен из модели
        token = EmailChangeRequest.objects.get(user=self.user).token

        # 3) подтверждаем смену
        url_conf = reverse('account:email-change-confirm')
        resp = self.client.post(url_conf, {
            'token': str(token)
        }, format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        # 4) проверяем, что email действительно поменялся
        self.user.refresh_from_db()
        self.assertEqual(self.user.email, 'x@example.com')

    def test_password_reset_and_confirm(self):
        # 1) запрос на сброс пароля (без авторизации)
        #    (у вас AllowAny на этом viewset-е)
        url_req = reverse('account:password-reset-request')
        resp = self.client.post(url_req, {
            'email': 'tester@example.com'
        }, format='json')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        # 2) достаём токен
        token = PasswordResetRequest.objects.get(user=self.user).token

        # 3) подтверждаем сброс пароля — не забываем re_new_password!
        url_conf = reverse('account:password-reset-confirm')
        resp = self.client.post(url_conf, {
            'token': str(token),
            'new_password': 'newpass123',
            're_new_password': 'newpass123'
        }, format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        # 4) проверяем, что пароль сохранился
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('newpass123'))
