from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer
from . import models, schemas, crud, database, auth

# Create tables
models.Base.metadata.create_all(bind=database.engine)

# OAuth2 scheme for token-based authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

app = FastAPI()


# Dependency: database session
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


# -------------------- TODOS --------------------


@app.get("/todos", response_model=list[schemas.TodoResponse])
def read_todos(db: Session = Depends(get_db)):
    return crud.get_todos(db)


@app.post("/todos", response_model=schemas.TodoResponse)
def create_todo(todo: schemas.TodoCreate, db: Session = Depends(get_db)):
    return crud.create_todo(db, todo)


@app.get("/todos/{todo_id}", response_model=schemas.TodoResponse)
def read_todo(todo_id: int, db: Session = Depends(get_db)):
    todo = crud.get_todo(db, todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo


@app.put("/todos/{todo_id}", response_model=schemas.TodoResponse)
def update_todo(todo_id: int, todo: schemas.TodoUpdate, db: Session = Depends(get_db)):
    updated = crud.update_todo(db, todo_id, todo)
    if not updated:
        raise HTTPException(status_code=404, detail="Todo not found")
    return updated


@app.delete("/todos/{todo_id}", response_model=schemas.TodoResponse)
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    deleted = crud.delete_todo(db, todo_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Todo not found")
    return deleted


# -------------------- USERS --------------------


@app.get("/users", response_model=list[schemas.UserResponse])
def read_users(db: Session = Depends(get_db)):
    return crud.get_users(db)


@app.get("/users/{user_id}", response_model=schemas.UserResponse)
def read_user(user_id: int, db: Session = Depends(get_db)):
    user = crud.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@app.post("/users/{user_id}/change-password", response_model=schemas.UserResponse)
def change_password(user_id: int, new_password: str, db: Session = Depends(get_db)):
    updated = crud.update_user_password(db, user_id, new_password)
    if not updated:
        raise HTTPException(status_code=404, detail="User not found")
    return updated


@app.put("/users/{user_id}", response_model=schemas.UserResponse)
def update_user(user_id: int, user: schemas.UserUpdate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_id(db, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    if user.username:
        db_user.username = user.username
    if user.email:
        db_user.email = user.email
    if user.password:
        db_user.hashed_password = auth.hash_password(user.password)

    db.commit()
    db.refresh(db_user)
    return db_user


@app.delete("/users/{user_id}", response_model=schemas.UserResponse)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    deleted = crud.delete_user(db, user_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="User not found")
    return deleted


# -------------------- AUTH --------------------


@app.post("/register", response_model=schemas.UserResponse)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    existing_user = crud.get_user(db, user.username)
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return crud.create_user(db, user)


@app.post("/login", response_model=schemas.Token)
def login(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user.username)
    if not db_user or not auth.verify_password(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = auth.create_access_token({"sub": db_user.username})
    return {"access_token": token, "token_type": "bearer"}


@app.get("/protected")
def protected_route(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, auth.SECRET_KEY, algorithms=[auth.ALGORITHM])
        username: str = payload.get("sub")
        if not username:
            raise HTTPException(status_code=401, detail="Invalid token payload")
        return {"message": f"Hello, {username}. This is a protected route."}
    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
