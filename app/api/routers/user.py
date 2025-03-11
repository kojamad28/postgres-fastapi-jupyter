from typing import List

from fastapi import APIRouter, Depends, Query
from sqlmodel import Session

from api.crud.base import retrieve_models, retrieve_model, create_model, update_model, delete_model
from api.dependencies import get_session
from api.models.accounts import User
from api.schemas.user import RetrievedUser, CreatedUser, UpdatedUser

router = APIRouter()


@router.get('/list/', response_model=List[RetrievedUser])
async def get_users(
    session: Session = Depends(get_session), offset: int = Query(default=0), limit: int = Query(default=100, lte=100)
) -> List[RetrievedUser]:
    return retrieve_models(session, User, offset, limit)


@router.get('/{target}', response_model=RetrievedUser)
async def get_user(
    target: str, session: Session = Depends(get_session)
) -> RetrievedUser:
    return retrieve_model(session, User, 'name', target)


@router.post('/list/', response_model=RetrievedUser)
async def create_user(
    created_user: CreatedUser, session: Session = Depends(get_session)
) -> RetrievedUser:
    return create_model(session, User, created_user)


@router.put('/{target}', response_model=RetrievedUser)
async def update_user(
    target: str, updated_user: UpdatedUser, session: Session = Depends(get_session)
) -> RetrievedUser:
    return update_model(session, User, 'name', target, updated_user)


@router.delete('/{target}')
async def delete_user(target: str, session: Session = Depends(get_session)) -> dict:
    return delete_model(session, User, 'name', target)
