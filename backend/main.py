from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import models, schemas, crud
from database import SessionLocal, engine

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db=db, user=user)

@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@app.post("/expenses/", response_model=schemas.Expense)
def create_expense(expense: schemas.ExpenseCreate, db: Session = Depends(get_db)):
    return crud.create_expense(db=db, expense=expense)

@app.get("/expenses/{user_id}", response_model=list[schemas.Expense])
def read_expenses(user_id: int, db: Session = Depends(get_db)):
    return crud.get_expenses_by_user(db=db, user_id=user_id)


@app.post("/calculate-savings/{user_id}")
def trigger_savings_calculation(user_id: int, db: Session = Depends(get_db)):
    success = crud.calculate_savings(db, user_id)
    return {"status": "success" if success else "error"}

@app.get("/financial-report/{user_id}")
def get_financial_report(user_id: int, db: Session = Depends(get_db)):
    report = crud.get_financial_report(db, user_id)
    if report is None:
        raise HTTPException(status_code=404, detail="User not found")
    return report


