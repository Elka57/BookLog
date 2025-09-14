# users/apps.py
from django.apps import AppConfig

class UsersConfig(AppConfig):
    name = "users"

    def ready(self):
        # при старте приложения реально импортируем файл с сигнальными хэндлерами
        import users.signals  


