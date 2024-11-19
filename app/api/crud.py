from fastapi import HTTPException, Query
from sqlmodel import SQLModel, Session, select


def create_model(session: Session, model: type[SQLModel], created_model: SQLModel):
    db_model = model.from_orm(created_model)
    session.add(db_model)
    session.commit()
    session.refresh(db_model)
    return db_model


def retrieve_models(session: Session, model: type[SQLModel], offset: int = 0, limit: int = 100):  # TODO: Query(default=100, lte=100)などにしてみる。
    models = session.exec(select(model).offset(offset).limit(limit)).all()
    return models


def retrieve_model(session: Session, model: type[SQLModel], index_col: str, target: str):
    db_model = session.exec(select(model).where(getattr(model, index_col) == target)).first()
    if not db_model:
        raise HTTPException(status_code=404, detail=f'{target} not found')
    return db_model


def update_model(session: Session, model: type[SQLModel], index_col: str, target: str, updated_model: SQLModel):
    db_model = session.exec(select(model).where(getattr(model, index_col) == target)).first()
    if not db_model:
        raise HTTPException(status_code=404, detail=f'{target} not found')
    updated_model_data = updated_model.dict(exclude_unset=True)
    for key, value in updated_model_data.items():
        setattr(db_model, key, value)
    session.add(db_model)
    session.commit()
    session.refresh(db_model)
    return db_model


def delete_model(session: Session, model: type[SQLModel], index_col: str, target: str):
    db_model = session.exec(select(model).where(getattr(model, index_col) == target)).first()
    if not db_model:
        raise HTTPException(status_code=404, detail=f'{target} not found')
    session.delete(db_model)
    session.commit()
    return {'ok': True}
