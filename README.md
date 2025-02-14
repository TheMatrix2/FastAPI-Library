#  FastAPI Library API

## Описание проекта

FastAPI-приложение для управления библиотечным каталогом.  
Реализованы:
- Аутентификация (JWT)
- Ролевая система (Администратор, Читатель)
- CRUD для книг, авторов, читателей и выдачи книг
- Пагинация, фильтрация, логирование и обработка ошибок

## Стек технологий

- **Python 3.12**
- **FastAPI**
- **PostgreSQL**
- **SQLAlchemy + Alembic**
- **Pydantic**
- **JWT (аутентификация)**
- **Docker + Docker Compose**
- **Pytest (тестирование)**

---

## Установка и запуск приложения

### 1. Установка зависимостей

#### 1. Установите **Python 3.12**
#### 2. Создайте и активируйте виртуальное окружение:

```
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
# или
.venv\Scripts\activate  # Window
```
	
#### 3.	Установите зависимости:

```pip install -r requirements.txt```

### 2. Настройка переменных окружения

Скопируйте пример содержимого .env файла и настройте под сове окружение:

```cp .env.example .env```

### 3. Настройка базы данных (если без Docker)

Если PostgreSQL установлен локально:
1.	Запустите PostgreSQL
2. Создайте базу данных:

```CREATE DATABASE library_db;```

3.	Примените миграции:

alembic upgrade head

### 4. Запуск приложения

Запустите сервер:

```uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload```

Приложение будет доступно по адресу:
http://127.0.0.1:8000

Запуск в Docker
1.	Убедитесь, что установлен Docker и Docker Compose.
2. Соберите и запустите контейнеры:

```docker-compose up --build```

Приложение будет доступно на порту 8000.
3.	При первом запуске примените миграции:

```docker-compose exec app alembic upgrade head```

Остановить контейнеры:

```docker-compose down```

## Запуск тестов

### 1. Локально (без Docker)

```pytest -v```

### 2. В Docker-контейнере

```docker-compose exec app pytest -v```

## Функциональность API

### Аутентификация
	•	Регистрация (POST /auth/register)
	•	Вход в систему (POST /auth/login)
	•	Получение профиля (GET /users/me)

### Управление книгами
	•	Создание книги (POST /books/, только админ)
	•	Получение списка книг (GET /books/)
	•	Получение книги по ID (GET /books/{book_id})
	•	Обновление книги (PUT /books/{book_id}, только админ)
	•	Удаление книги (DELETE /books/{book_id}, только админ)

### Управление авторами
	•	Создание автора (POST /authors/, только админ)
	•	Получение списка авторов (GET /authors/)
	•	Получение автора по ID (GET /authors/{author_id})
	•	Обновление автора (PUT /authors/{author_id}, только админ)
	•	Удаление автора (DELETE /authors/{author_id}, только админ)

### Управление пользователями
	•	Получение списка пользователей (GET /users/, только админ)
	•	Обновление профиля (PUT /users/me)

### Выдача и возврат книг
	•	Выдача книги (POST /loans/, только админ)
	•	Возврат книги (PUT /loans/{loan_id}, только админ)
	•	Просмотр активных выдач (GET /loans/)

