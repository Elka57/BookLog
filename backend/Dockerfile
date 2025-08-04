# Базовый образ с Python 3.13
FROM python:3.13-slim

# Рабочая директория внутри контейнера
WORKDIR /app

# Скопировать файл зависимостей и установить пакеты
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Скопировать весь код приложения
COPY . .

# Открыть порт для Django
EXPOSE 8000

# Команда по умолчанию — запустить сервер
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
