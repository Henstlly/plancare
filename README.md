# PlanCare API

API для приложения плана ухода за питомцами.

## Зависимости

- Python 3.9+
- Django==3.2.3
- djangorestframework==3.12.4
- djangorestframework-simplejwt==4.8.0
- djoser==2.1.0
- django-filter==2.4.0
- drf-spectacular==0.26.0

## Переменные окружения

Создайте файл `.env` на основе `.env.example`:

```
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost,0.0.0.0
```

## Локальный запуск

```bash
git clone <repo-url>
cd kittygram2
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 manage.py migrate
python3 manage.py seed_data  # заполнить тестовыми данными
python3 manage.py runserver
```

Тестовые пользователи: `admin/admin`, `user/user`.

## Запуск через Docker

```bash
docker compose up --build -d
```

Миграции применяются автоматически при старте.

## API эндпоинты

### Аутентификация

| Метод | URL | Описание |
|---|---|---|
| POST | `/auth/users/` | Регистрация |
| POST | `/auth/jwt/create/` | Получить JWT токен |
| POST | `/auth/jwt/refresh/` | Обновить токен |

### Кошки

| Метод | URL | Описание | Права |
|---|---|---|---|
| GET | `/cats/` | Список кошек | Все |
| POST | `/cats/` | Создать кошку | Авторизованные |
| GET | `/cats/{id}/` | Детали кошки | Все |
| PUT/PATCH | `/cats/{id}/` | Редактировать кошку | Владелец |
| DELETE | `/cats/{id}/` | Удалить кошку | Владелец |

Фильтры: `color`, `owner`. Поиск: `name`. Сортировка: `name`, `birth_year`.

### Пользователи

| Метод | URL | Описание |
|---|---|---|
| GET | `/users/` | Список пользователей (только чтение) |

### Корма (справочник)

| Метод | URL | Описание |
|---|---|---|
| GET | `/feeds/` | Список кормов |
| POST | `/feeds/` | Создать корм |
| GET/PUT/DELETE | `/feeds/{id}/` | Детали/редактирование/удаление |

### Лекарства (справочник)

| Метод | URL | Описание |
|---|---|---|
| GET | `/medications/` | Список лекарств |
| POST | `/medications/` | Создать лекарство |
| GET/PUT/DELETE | `/medications/{id}/` | Детали/редактирование/удаление |

### План ухода

| Метод | URL | Описание | Права |
|---|---|---|---|
| GET | `/care-plan/` | Список пунктов плана | Владелец кота |
| POST | `/care-plan/` | Создать пункт | Владелец кота |
| GET | `/care-plan/{id}/` | Детали пункта | Владелец кота |
| PUT/PATCH | `/care-plan/{id}/` | Изменить пункт | Владелец кота |
| DELETE | `/care-plan/{id}/` | Удалить пункт | Владелец кота |
| POST | `/care-plan/{id}/execute/` | Отметить выполнение | Владелец кота |
| POST | `/care-plan/{id}/cancel/` | Отменить пункт | Владелец кота |
| GET | `/care-plan/{id}/history/` | История выполнения пункта | Владелец кота |

Фильтры: `cat`, `action_type`, `is_active`. Поиск: `notes`. Сортировка: `scheduled_time`, `created_at`.

### Логи выполнения

| Метод | URL | Описание | Права |
|---|---|---|---|
| GET | `/execution-logs/` | История выполнения | Владелец кота |
| GET | `/execution-logs/{id}/` | Детали записи | Владелец кота |

Фильтры: `cat`, `care_plan_item`, `status`. Сортировка: `executed_at`.

## Документация API

- **Swagger UI:** http://localhost:8000/api/docs/
- **ReDoc:** http://localhost:8000/api/redoc/
- **OpenAPI Schema:** http://localhost:8000/api/schema/

## Валидации

| Правило | Где проверяется | Сообщение |
|---|---|---|
| Для кормления нужен корм | CarePlanItemSerializer | Для кормления необходимо указать корм |
| Для лекарства нужен препарат | CarePlanItemSerializer | Для лекарства необходимо указать препарат |
| Кот должен быть вашим | CarePlanItemSerializer | Вы можете создавать пункты плана только для своих котов |
| Время приёма обязательно | CarePlanItemSerializer | Время приёма обязательно |
| Имя кота ≥ 2 символа | CatSerializer | Имя кота должно содержать минимум 2 символа |
| Год рождения ≤ текущий | CatSerializer | Год рождения не может быть больше текущего |

## Тестовые данные

```bash
python3 manage.py seed_data
```

Создаёт: 2 пользователя, 3 кота, 3 корма, 3 лекарства, 9 пунктов плана, 6 логов выполнения.
