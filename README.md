# 📚 BookLog - читательский дневник

Веб‑приложение для ведения и чтения читательских дневников: пользователи создают записи о прочитанных книгах, ведут личные заметки и могут делиться публичными записями с другими. Проект включает backend на Django REST Framework и frontend на React, с окружением разработки в Docker.

> Важно: это личный некоммерческий проект. Репозиторий открыт публично исключительно для демонстрации кода в портфолио и оценки навыков. Код не позиционируется как эталонный, некоторые части могут быть упрощены и не оптимизированы для продакшена.

---

## 📄 Описание проекта

- **Назначение:** Простой сервис для каталогизации авторов и книг, ведения личных заметок о чтении и просмотра публичных дневников других пользователей.
- **Ключевые сущности:** Авторы, Книги, Пользователи, Записи дневника, Профили и настройки приватности.
- **Модель приватности:** Записи по умолчанию приватные, автор может пометить запись как публичную для общего доступа.
- **Цель публикации:** Показать структуру проекта, подход к API, работу с авторизацией и клиентской частью в React.

---

## 📡 Стек и возможности

#### Технологии

- **Backend:** 
  - **Django, Django REST Framework**
  - **Simple JWT** (через rest_framework_simplejwt) с ротацией refresh и blacklist
  - **dj-rest-auth** + **django-allauth** (регистрация, подтверждение email, социальные провайдеры при необходимости)
  - **django-filter** (фильтрация), **rest_framework.filters** (поиск, сортировка)
  - **rest_framework_roles** (роли/разграничение доступа)
  - **corsheaders** (CORS)
  - **PostgreSQL** (dev/prod), подключения через DATABASES
- **Frontend:** React, React Router, Fetch/Axios, компонентный подход
- **Инфраструктура:** **Docker**, docker-compose, .env конфигурация через **python-decouple**, статика и медиа, CSRF/CORS настройки

#### Аутентификация и авторизация

- **JWT:** Bearer-токены, ACCESS_TOKEN_LIFETIME 15 минут, REFRESH_TOKEN_LIFETIME 30 дней, включена ротация и blacklist.
- **Логин/регистрация:** **dj-rest-auth** поверх **django-allauth**; уникальный email, опциональная верификация почты.
- **Редиректы после подтверждения email/сброса пароля:** на фронтенд через FRONTEND_URL.
- **Роли:** базовая роль‑модель через **rest_framework_roles** (конфиг BookLog.roles.ROLES).

#### Фильтрация, поиск и сортировка

- **Фильтрация:** django_filters.rest_framework.DjangoFilterBackend
- **Поиск:** rest_framework.filters.SearchFilter
- **Сортировка:** rest_framework.filters.OrderingFilter

#### CORS и CSRF

- **CORS:** разрешены куки/креденшелы (CORS_ALLOW_CREDENTIALS=True), источники из FRONTEND_URL.
- **CSRF:** доверенный origin из FRONTEND_URL, CSRF_COOKIE_HTTPONLY=False (для SPA — учитывайте риски и по необходимости ужесточайте в проде).

#### Конфигурация окружения

- **Переменные среды:** через python-decouple (SECRET_KEY, ALLOWED_HOSTS, TIME_ZONE, FRONTEND_URL, DB_HOST, DB_PORT, POSTGRES_* и т.д.).
- **Часовой пояс:** задаётся из .env (TIME_ZONE, по умолчанию UTC).
- **ALLOWED_HOSTS:** берутся из .env (CSV-формат).
- **Email/редиректы:** ACCOUNT_EMAIL_CONFIRMATION_* и кастомные пути для redirect на фронт.

#### Пример .env(backend)

```env
# Основное
SECRET_KEY=change-me
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
TIME_ZONE=Europe/Moscow

# База
POSTGRES_DB=booklog
POSTGRES_USER=booklog
POSTGRES_PASSWORD=booklog
DB_HOST=db
DB_PORT=5432

# Фронтенд
FRONTEND_URL=http://localhost:3000
```

#### 🪩 Основные функции

- **Каталог:** Просмотр и поиск авторов и книг.
- **Дневник:** Создание, редактирование и удаление записей с заметками и статусом прочтения.
- **Публичные записи:** Просмотр записей, отмеченных как публичные, со страницы ленты.
- **Пользователи:** Регистрация, вход, профиль, базовые настройки приватности.
- **API:** REST API для всех основных операций, пагинация и фильтрация.

#### 🏛️ Архитектура

- **Разделение слоёв:** Отдельные директории для backend и frontend.
- **API‑контракты:** Чёткие эндпоинты DRF, сериализаторы и валидация.
- **Ветки:** main как витрина стабильной версии, develop для активной разработки и фич.

---

## 🚀 Старт работы

#### 🐳 Быстрый старт в Docker

**Требования:** Docker и docker-compose, файл `.env` в корне (см. пример ниже).

```bash
# 1) Клонируем репозиторий и переходим в него
git clone https://github.com/Elka57/BookLog.git
cd BookLog

# 2) Создаём .env из примера
cp .env.example .env

# 3) Запускаем контейнеры
docker-compose up --build

# 4) Применяем миграции и создаём суперпользователя
docker-compose exec backend python manage.py migrate
docker-compose exec backend python manage.py createsuperuser
```

**Доступы по умолчанию:**
- Backend: http://localhost:8000
- Frontend: http://localhost:3000

#### ⚙️ Сервисы Docker

- **devcontainer:** среда разработки (Python 3.13 + Node 20, tools, WakaTime). Используется для работы из IDE (например, VS Code Dev Containers). Контейнер «спит» и ждёт подключения.
- **backend:** Django (runserver), монтируется `./backend` внутрь контейнера, горячая перезагрузка кода.
- **frontend:** React (npm start), монтируется `./frontend`, включён `CHOKIDAR_USEPOLLING=true` для стабильного отслеживания изменений в Docker.

**Порты:**
- `8000:8000` — Django
- `3000:3000` — React

**Изоляция зависимостей:**
- **Python venv** и **node_modules** подключены как тома внутри контейнеров, чтобы избежать конфликтов прав и перезаписи.


#### 🧰 Devcontainer (опционально)

В проекте есть `devcontainer` для удобной разработки:
- База: `python:3.13-slim` + Node 20, system deps.
- Сразу ставятся зависимости backend (`requirements-dev.txt`) и frontend (`npm ci`).
- Монтируется весь проект (`/workspace`), чтобы изменение кода не требовало пересборки.
- Поддерживает WakaTime (если есть `~/.wakatime.cfg` и `WAKATIME_API_KEY`).

Запуск (альтернативный сценарий, обычно IDE делает это за вас):
```bash
docker-compose up -d devcontainer
docker exec -it <project>_devcontainer_1 bash
# Далее внутри:
cd backend && python -m venv .venv && source .venv/bin/activate
```

#### Локальный запуск без Docker

1. Клонирование: 

```bash
git clone https://github.com/Elka57/BookLog.git
cd BookLog
```

2. Backend окружение: 

```bash
cd backend
python -m venv .venv && source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
python manage.py migrate
python manage.py runserver
```

3. Frontend окружение: 

```bash
cd ../frontend
npm install
npm start
```

## 📜 Статус и ограничения

- **Статус проекта**: Личный pet‑проект, публикуется для портфолио и демонстрации кода.
- **Ограничения**: dev‑compose использует `runserver/npm start`; для продакшена потребуются gunicorn/uvicorn, сборка фронта, отдельный compose/infra.
- **Производственная готовность**: Не предназначен для продакшена без дополнительной доработки по безопасности, логированию, мониторингу и нагрузочному тестированию.
- **Безопасность**: Секреты и ключи в репозитории отсутствуют; используйте .env. При развёртывании в интернете отключайте DEBUG, настраивайте ALLOWED_HOSTS, CORS и HTTPS.
- **Данные**: В репозитории могут быть демо‑данные и фикстуры для локального запуска; не используйте их в продакшене.
- **Лицензия использования**: Открытый исходный код для чтения и обучения; коммерческое использование — на усмотрение владельца лицензии (см. LICENSE).

## 🐍 Заметки по выпускам

#### **14 сентября**

##### **Реализовано:**
1. Налажена регистрация и авторизация пользователя с помощью `dj-rest-auth` и `django-allauth`. 
2. Налажена работа токенов с помощью `Simple JWT`. 

##### **Баги:**
1. Не срабатывает refresh-token по истечению 'ACCESS_TOKEN_LIFETIME'. 

## 🤝 Контакты и лицензия

- **Автор:** Анна Михалева
- **Профиль GitHub:** https://github.com/Elka57
- **Связь:** elka57btk@yandex.ru
- **Лицензия:** MIT (см. файл LICENSE)













