# Используйте подходящий базовый образ
FROM python:3.9-slim

# Установите необходимые зависимости
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Установите рабочую директорию
WORKDIR /app

# Скопируйте файлы вашего приложения
COPY . .

# Убедитесь, что wait-for-it.sh имеет права на выполнение
RUN chmod +x wait-for-it.sh

# Установите зависимости вашего приложения
RUN pip install --no-cache-dir -r requirements.txt

# Команда по умолчанию для запуска приложения
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
