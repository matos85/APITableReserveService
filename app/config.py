import os
from dotenv import load_dotenv

# Загружаем переменные окружения из .env файла
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost/mydatabase")
