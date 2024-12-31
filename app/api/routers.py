from fastapi import APIRouter, Depends, Query
from sqlmodel import Session

from . import models, crud
from .dependencies import get_session


router = APIRouter()

@router.get('/list/', response_model=list[models.RetrievedUser])
def get_users(session: Session = Depends(get_session), offset: int = Query(default=0), limit: int = Query(default=100, lte=100)):
    return crud.retrieve_models(session, models.User, offset, limit)


@router.get('/{target}', response_model=models.RetrievedUser)
def get_user(target: str, session: Session = Depends(get_session)):
    return crud.retrieve_model(session, models.User, 'name', target)


@router.post('/list/', response_model=models.RetrievedUser)
def create_user(created_user: models.CreatedUser, session: Session = Depends(get_session)):
    return crud.create_model(session, models.User, created_user)


@router.put('/{target}', response_model=models.RetrievedUser)
def update_user(target: str, updated_user: models.UpdatedUser, session: Session = Depends(get_session)):
    return crud.update_model(session, models.User, 'name', target, updated_user)


@router.delete('/{target}')
def delete_user(target: str, session: Session = Depends(get_session)):
    return crud.delete_model(session, models.User, 'name', target)
