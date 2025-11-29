from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from . import models, schemas, crud, database

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()


def get_db():
    db = database.SessionLocal()

    try:
        yield db
    finally:
        db.close()


@app.get("/todos", response_model=list[schemas.TodoResponse])
def read_todos(db: Session = Depends(get_db)):
    todos = crud.get_todos(db)
    return todos


@app.post("/todos", response_model=schemas.TodoResponse)
def create_todo(todo: schemas.TodoCreate, db: Session = Depends(get_db)):
    return crud.create_todo(db, todo)


@app.get("/todos/{todo_id}", response_model=schemas.TodoResponse)
def read_todo(todo_id: int, db: Session = Depends(get_db)):
    return crud.get_todo(db, todo_id)


@app.put("/todos/{todo_id}", response_model=schemas.TodoResponse)
def modify_todo(todo_id: int, todo: schemas.TodoUpdate, db: Session = Depends(get_db)):
    return crud.update_todo(db, todo_id, todo)


@app.delete("/todos/{todo_id}", response_model=schemas.TodoResponse)
def remove_todo(todo_id: int, db: Session = Depends(get_db)):
    return crud.delete_todo(db, todo_id)
