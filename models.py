from sqlalchemy import Column, Integer, String, Boolean
from .database import Base


class Todo(Base):
    __tablename__ = "todoss"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    done = Column(Boolean, default=False)
