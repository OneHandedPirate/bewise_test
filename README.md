## Тестовое задание Bewise


<details>
<summary>ТЗ</summary>
Разработайте сервис для обработки заявок пользователей. Сервис должен:
Принимать заявки через REST API (FastAPI).
Обрабатывать и записывать заявки в PostgreSQL.
Публиковать информацию о новых заявках в Kafka.
Обеспечивать эндпоинт для получения списка заявок с фильтрацией и пагинацией.
Включать Docker-файл для развертывания приложения.

Детали реализации:

**REST API**:

Создайте эндпоинт POST /applications для создания новой заявки. Заявка содержит следующие поля:
- id (генерируется автоматически)
- user_name (имя пользователя)
- description (описание заявки)
- created_at (дата и время создания, устанавливается автоматически)
Создайте эндпоинт GET /applications для получения списка заявок:
Поддержка фильтрации по имени пользователя (user_name).
Поддержка пагинации (параметры page и size).

**PostgreSQL**:

Спроектируйте таблицу для хранения заявок.
Используйте SQLAlchemy для работы с базой данных.

**Kafka**:

Настройте публикацию данных о новых заявках в топик Kafka.
В сообщении должно содержаться:
- id заявки
- user_name
- description
- created_at

**Асинхронность**:

Убедитесь, что все взаимодействия с Kafka и PostgreSQL реализованы асинхронно.

**Docker**:

Подготовьте Dockerfile и docker-compose.yml для локального запуска:
Приложение (FastAPI)
PostgreSQL
Kafka
Документация:
Опишите инструкцию по запуску проекта.
Добавьте пример запроса и ответа для эндпоинтов.
</details>


### Запуск 

Выполните команды:
```
git clone https://github.com/OneHandedPirate/bewise_test.git
cd bewise_test
make create_env
docker compose up -d
```
Это склонирует данный репозиторий, перейдет в директорию проекта и создаст минимальный `.env` файл для запуска Docker Compose и поднимет docker compose в detached-режиме.

### Использование:
По умолчанию FastApi будет запущено на `8000` порту (можно изменить в `.env` в строке `GUNICORN__PORT`).
Swagger-документация доступна на стандартом FastApi эндпоинте (`/docs`).

### Эндпоинты

- heathcheck:
    - `api/v1/heathcheck/status`(GET) - проверяет доступность приложения. 
      - Ответ: `{"status": "OK"}` 
    - `api/v1/heathcheck/service-status` (GET) - опрашивает сервисы на предмет их доступности (в данном случае у нас сервисы "db" (Postgres) и "kafka"). В случае ошибки в поле `error_message` будет ее строковое представление.
      - Ответ (пример):
        ```
        result: [
          { 
            "service_name": "db",
            "status": "OK"
            "response_time": 0.06464,
            "error_message": null
          },
          { 
            "service_name": "kafka",
            "status": "OK"
            "response_time": 0.00536,
            "error_message": null
          },
        ```

- applications:
  - `api/v1/applications` (POST) - запрос на создание нового объекта Application. Принимает JSON вида:
    
    - `{user_name: "string", description": "string"}`
      
      - Оба поля обязательны.
      - Длина строки `user_name` не должна превышать 60 знаков (валидность длины значения проверяется pydantic).
    - Ответ (пример):
    
      ```
      {
        "id": "4fc3b475-6415-445a-a736-18e62c1dbff2",
        "user_name": "string",
        "description": "string",
        "created_at": "2025-01-19T11:09:29.111038",
        "updated_at": "2025-01-19T11:09:29.111038"
      }
      ```
  - `api/v1/applications/filter` (GET) - получение пагинированного списка заявок.
    - Query-параметры:
      
      - `page` - номер страницы (по умолчанию 1, валидные значения: >0)
      - `page_size` - количество записей на странице (по умолчанию 20, валидные значения: 1-150)
      - `user_name` - (опциональный) - фильтрация по имени пользователя (я реализовал регистрозависимую фильтрацию по полному совпадению). Если этот параметр не передан - будет выведен пагинированный список всех заявок.
    - Ответ (пример):
      ```
      {
        "page": 1,
        "page_size": 20,
        "total_pages": 1,
        "total_items": 1,
        "items": [
          {
            "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
            "user_name": "string",
            "description": "string",
            "created_at": "2025-01-21T00:39:56.426Z",
            "updated_at": "2025-01-21T00:39:56.426Z"
          }
        ]
      }
      ```
      
### Примечания:

- данные БД (директория `/var/lib/postgresql/data` из контейнера) будет примонтированная к директории `postgres-data` в корневой папке проекта.
- логи приложения можно посмотреть в директории `/logs`:
  
  - `gunicorn.errors.log` - стандартный лог ошибок gunicorn.
  - `logs.log` - логгер событий приложения. В текущей реализации логируются события создания объектов записей в бд и их передача в кафку.
  - `requests.log` - логгер запросов. Логируется тип запроса, эндпоинт, тело запроса (если передано. Если передается не JSON, то логируется Content-Type), query-параметры (если переданы), статус код ответа и его время.
