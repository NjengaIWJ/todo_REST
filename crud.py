from sqlalchemy.orm import Session
from . import models, schemas, auth


def get_todos(db: Session):
    return db.query(models.Todo).all()


def create_todo(db: Session, todo: schemas.TodoCreate):
    db_todo = models.Todo(title=todo.title, done=todo.done)

    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)

    return db_todo


def update_todo(db: Session, todo_id: int, todo: schemas.TodoUpdate):
    db_todo = db.query(models.Todo).filter(models.Todo.id == todo_id).first()

    if db_todo:
        if todo.title is not None:
            db_todo.title = todo.title

        if todo.done is not None:
            db_todo.done = todo.done

        db.commit()
        db.refresh(db_todo)
    return db_todo


def delete_todo(db: Session, todo_id: int):
    db_todo = db.query(models.Todo).filter(models.Todo.id == todo_id).first()

    if db_todo:
        db.delete(db_todo)

        db.commit()
    return db_todo


def get_todo(db: Session, todo_id: int):
    return db.query(models.Todo).filter(models.Todo.id == todo_id).first()


def create_user(db: Session, user: schemas.UserCreate):
    hashed = auth.hash_password(user.password)

    db_user = models.User(username=user.username, email=user.email, password=hashed)

    db.add(db_user)

    db.commit()
    db.refresh(db_user)

    return db_user


def get_users(db: Session):
    return db.query(models.User).all()


def get_user(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


def get_user_by_id(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def update_user_password(db: Session, user_id: int, new_password: str):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()

    if db_user:
        hashed = auth.hash_password(new_password)
        db_user.password = hashed

        db.commit()
        db.refresh(db_user)

    return db_user


def delete_user(db: Session, user_id: int):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()

    if db_user:
        db.delete(db_user)

        db.commit()
    return db_user
