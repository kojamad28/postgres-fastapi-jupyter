from typing import Optional

from sqlmodel import SQLModel, Field


class BaseUser(SQLModel):
    name: str = Field(index=True)
    email: str = Field()


class User(BaseUser, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)


class CreatedUser(BaseUser):
    pass


class RetrievedUser(BaseUser):
    id: int


class UpdatedUser(BaseUser):
    name: Optional[str] = Field(default=None, index=True)
    email: Optional[str] = Field(default=None)
