from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.models.tables import Table
from app.schemas.table import TableCreate
from app.database import get_db

router = APIRouter()

@router.get("/tables/")
def read_tables(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    tables = db.query(Table).offset(skip).limit(limit).all()
    return tables

@router.post("/tables/")
def create_table(table: TableCreate, db: Session = Depends(get_db)):
    db_table = Table(**table.dict())
    db.add(db_table)
    db.commit()
    db.refresh(db_table)
    return db_table

@router.delete("/tables/{id}")
def delete_table(id: int, db: Session = Depends(get_db)):
    db_table = db.query(Table).filter(Table.id == id).first()
    if db_table is None:
        raise HTTPException(status_code=404, detail="Table not found")
    db.delete(db_table)
    db.commit()
    return {"detail": "Table deleted"}
