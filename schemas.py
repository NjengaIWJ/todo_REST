from pydantic import BaseModel


class TodoBase(BaseModel):
    title: str
    done: bool = False


class TodoCreate(TodoBase):
    pass


class TodoUpdate(BaseModel):
    title: str | None = None
    done: bool | None = None


class TodoResponse(TodoBase):
    id: int

    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    username: str
    email: str
    password: str


class UserUpdate(BaseModel):
    username: str | None = None
    email: str | None = None
    password: str | None = None


class UserResponse(BaseModel):
    id: int
    username: str
    email: str

    class Comfig:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str
