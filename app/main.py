from fastapi import FastAPI
from app.routers import table, reservation
from app.database import engine, Base
from app.logging_config import setup_logging

setup_logging()

app = FastAPI()

# Создаем таблицы в БД
Base.metadata.create_all(bind=engine)

app.include_router(table.router)
app.include_router(reservation.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Restaurant Booking API!"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

