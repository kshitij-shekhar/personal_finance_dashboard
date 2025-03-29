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

# @app.get("/financial-report/{user_id}")
# def get_financial_report(user_id: int, db: Session = Depends(get_db)):
#     report = crud.get_financial_report(db, user_id)
#     if report is None:
#         raise HTTPException(status_code=404, detail="User not found")
#     return report



@app.get("/total-expenses/{user_id}")
def read_total_expenses(user_id: int, db: Session = Depends(get_db)):
    try:
        total_expenses = crud.get_total_expenses(db, user_id)
        return {"total_expenses": total_expenses}
    except Exception as e:
        return {"error": str(e)}



@app.get("/total-income/{user_id}")
def read_total_income(user_id: int, db: Session = Depends(get_db)):
    try:
        total_income = crud.get_total_income(db, user_id)
        return {"total_income": total_income}
    except Exception as e:
        return {"error": str(e)}  # Return error message in JSON format


@app.get("/net-savings/{user_id}")
def read_net_savings(user_id: int, db: Session = Depends(get_db)):
    try:
        net_savings = crud.get_net_savings(db, user_id)
        return {"net_savings": net_savings}
    except Exception as e:
        return {"error": str(e)}  # Return error message in JSON format


@app.get("/expense-breakdown/{user_id}")
def read_expense_breakdown(user_id: int, db: Session = Depends(get_db)):
    expense_breakdown = crud.get_expense_breakdown(db, user_id)
    return {"categories": expense_breakdown}


@app.get("/financial-summary/{user_id}")
def read_financial_summary(user_id: int, db: Session = Depends(get_db)):
    try:
        summary = crud.get_financial_summary(db, user_id)
        return summary
    except Exception as e:
        return {"error": str(e)}





# @app.get("/budget/{user_id}")
# def read_budget(user_id: int, db: Session = Depends(get_db)):
#     budget = crud.get_budget(db, user_id)
#     return {"budgets": budget}


@app.get("/savings-recommendations/{user_id}")
def read_savings_recommendations(user_id: int, db: Session = Depends(get_db)):
    recommendation = crud.get_savings_recommendations(db, user_id)
    return {"recommendation": recommendation}



@app.get("/financial-health-score/{user_id}")
def read_financial_health_score(user_id: int, db: Session = Depends(get_db)):
    score = crud.get_financial_health_score(db, user_id)
    return {"score": score}



# @app.post("/budgets/{user_id}")
# def create_budget_endpoint(user_id: int, category: str, budget_amount: float, db: Session = Depends(get_db)):
#     crud.create_budget(db, user_id, category, budget_amount)
#     return {"message": "Budget created successfully"}

# @app.get("/budgets/{user_id}")
# def read_budgets_endpoint(user_id: int, db: Session = Depends(get_db)):
#     budgets = crud.get_budgets(db, user_id)
#     return {"budgets": budgets}

# @app.put("/budgets/{budget_id}")
# def update_budget_endpoint(budget_id: int, budget_amount: float, db: Session = Depends(get_db)):
#     crud.update_budget(db, budget_id, budget_amount)
#     return {"message": "Budget updated successfully"}

# @app.delete("/budgets/{budget_id}")
# def delete_budget_endpoint(budget_id: int, db: Session = Depends(get_db)):
#     crud.delete_budget(db, budget_id)
#     return {"message": "Budget deleted successfully"}


@app.post("/register")
def register(username: str, password: str):
   # Logic to register a new user (hash password and store it)
   return {"message": "User registered successfully"}

@app.post("/login")
def login(username: str, password: str):
   # Logic to authenticate user (check username and hashed password)
   return {"user_id": user_id} 

@app.post("/add-expense/{user_id}")
def add_expense(user_id: int, category: str, amount: float):
   # Logic to add an expense entry to the database
   return {"message": "Expense added successfully"}

@app.post("/add-income/{user_id}")
def add_income(user_id: int, source: str, amount: float):
   # Logic to add an income entry to the database
   return {"message": "Income added successfully"}

@app.post("/budgets/{user_id}")
def create_budget(user_id: int):
   # Logic to create a new budget entry in the database
   return {"message": "Budget created successfully"}

@app.put("/budgets/{budget_id}")
def update_budget(budget_id: int):
   # Logic to update an existing budget entry in the database
   return {"message": "Budget updated successfully"}

@app.delete("/budgets/{budget_id}")
def delete_budget(budget_id: int):
   # Logic to delete a specific budget entry from the database
   return {"message": "Budget deleted successfully"}