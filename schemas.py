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
