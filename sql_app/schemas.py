from datetime import date

from pydantic import BaseModel


class LoopBase(BaseModel):
    wages: float
    bags: float


class LoopCreate(LoopBase):
    date: date
    pass


class LoopUpdate(LoopBase):
    pass


class Loop(LoopBase):
    id: int
    date: date
    owner_id: int

    class Config:
        orm_mode = True


class ItemBase(BaseModel):
    title: str
    description: str | None = None


class ItemCreate(ItemBase):
    pass


class Item(ItemBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool
    items: list[Item] = []

    class Config:
        orm_mode = True
