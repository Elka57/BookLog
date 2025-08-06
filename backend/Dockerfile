# 1. Базовый образ с Python 3.13
FROM python:3.13-slim

# 2. Переменные окружения для работы Python в контейнере
ENV PYTHONDONTWRITEBYTECODE 1   # не сохранять .pyc-файлы
ENV PYTHONUNBUFFERED 1          # сразу выводить логи


# 3. Установка системных пакетов для Pillow, сборки зависимостей и Git Flow
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       build-essential \
       libjpeg62-turbo-dev \
       zlib1g-dev \
       git-flow \
    && rm -rf /var/lib/apt/lists/*


# 4. Рабочая директория внутри контейнера
WORKDIR /app

# 5. Копируем и устанавливаем Python-зависимости
COPY requirements.txt ./
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# 6. Копируем весь проект
COPY . .

# 7. Открываем порт для Django
EXPOSE 8000

# 8. Команда по умолчанию — запустить dev-сервер
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

