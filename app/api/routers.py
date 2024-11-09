from fastapi import APIRouter, Depends
from sqlmodel import Session

from . import models, crud
from .db import get_session


router = APIRouter()

@router.get('/users/', response_model=list[models.RetrievedUser])
def get_users(session: Session = Depends(get_session)):
    return crud.retrieve_models(session, models.User)


@router.get('/users/{target}', response_model=models.RetrievedUser)
def get_user(target: str, session: Session = Depends(get_session)):
    return crud.retrieve_model(session, models.User, 'name', target)


@router.post('/users/', response_model=models.RetrievedUser)
def create_user(created_user: models.CreatedUser, session: Session = Depends(get_session)):
    return crud.create_model(session, models.User, created_user)


@router.put('/users/{target}', response_model=models.RetrievedUser)
def update_user(target: str, session: Session = Depends(get_session)):
    return crud.update_model(session, models.User, 'name', target)


@router.delete('/users/{target}')
def delete_user(target: str, session: Session = Depends(get_session)):
    return crud.delete_model(session, models.User, 'name', target)
