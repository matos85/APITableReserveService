▎README.md

# API для бронирования столиков в ресторане

Это REST API для управления бронированием столиков в ресторане. С помощью этого API можно создавать, просматривать и удалять брони, а также управлять столиками и временными слотами.

## Функциональные возможности

- Создание, просмотр и удаление столиков.
- Создание, просмотр и удаление броней.
- Проверка доступности столиков на заданное время.

## Технологии

- FastAPI для создания API.
- SQLAlchemy для работы с базой данных.
- PostgreSQL в качестве СУБД.
- Alembic для миграций базы данных.
- Docker для контейнеризации приложения.

## Установка и запуск

Для запуска приложения вам потребуется Docker и Docker Compose.
Убедитесь, что они установлены на вашем компьютере.

1. Клонируйте репозиторий:

   
bash
   git clone https://github.com/matos85/APITableReserveService

   cd restaurant_reservation
   

2. Соберите и запустите контейнеры:

bash
docker-compose up --build

3. После успешного запуска API будет доступен по адресу: `http://host:8000`.

## Использование API

### Столики

- *Получить список столиков:*
  - `GET /tables/`

- *Создать новый столик:*
  - `POST /tables/`
  - Пример запроса:

json
{
  "name": "Table 1",
  "seats": 4,
  "location": "зал у окна"
}

- *Удалить столик:*
  - `DELETE /tables/{id}`

### Брони

- *Получить список броней:*
  - `GET /reservations/`

- *Создать новую бронь:*
  - `POST /reservations/`
  - Пример запроса:

json
{
  "customer_name": "Иван Иванов",
  "table_id": 1,
  "reservation_time": "2023-12-31T20:00:00",
  "duration_minutes": 120
}

- *Удалить бронь:*
  - `DELETE /reservations/{id}`

## Логгирование и тестирование

В проекте реализовано базовое логгирование. Для тестирования используйте `pytest`. 

### Запуск тестов

bash
pytest tests/

