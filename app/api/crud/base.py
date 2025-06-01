from fastapi import HTTPException
from sqlalchemy import text, select
from sqlalchemy.orm import Session
from sqlmodel import SQLModel


def check_connection(session: Session) -> dict:
    try:
        session.execute(text("SELECT 1"))
        return {
            "Status": "Success",
            "Detail": "Connection to database is successful",
            "Host": session.bind.url.host,
            "Database": session.bind.url.database,
            "Query": session.bind.url.query,
        }
    except Exception as e:
        return {
            "Status": "Failed",
            "Detail": str(e),
        }


def create_model(session: Session, model: type[SQLModel], created_model: SQLModel):
    db_model = model.from_orm(created_model)
    session.add(db_model)
    session.commit()
    return db_model


def retrieve_models(session: Session, model: type[SQLModel], offset: int, limit: int):
    models = session.execute(select(model).offset(offset).limit(limit)).all()
    return models


def retrieve_model(session: Session, model: type[SQLModel], index_col: str, target: str):
    db_model = session.execute(select(model).where(getattr(model, index_col) == target)).first()
    if not db_model:
        raise HTTPException(status_code=404, detail=f'{target} not found')
    return db_model


def update_model(session: Session, model: type[SQLModel], index_col: str, target: str, updated_model: SQLModel):
    db_model = session.execute(select(model).where(getattr(model, index_col) == target)).first()
    if not db_model:
        raise HTTPException(status_code=404, detail=f'{target} not found')
    updated_model_data = updated_model.dict(exclude_unset=True)
    for key, value in updated_model_data.items():
        setattr(db_model, key, value)
    session.commit()
    return db_model


def delete_model(session: Session, model: type[SQLModel], index_col: str, target: str):
    db_model = session.execute(select(model).where(getattr(model, index_col) == target)).first()
    if not db_model:
        raise HTTPException(status_code=404, detail=f'{target} not found')
    session.delete(db_model)
    session.commit()
    return {'ok': True}
