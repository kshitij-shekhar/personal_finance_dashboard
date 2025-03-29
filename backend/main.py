from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func,text
from backend.models import Income,Expense
from pydantic import BaseModel
# from passlib.context import CryptContext
# from typing import Optional
import crud
from database import SessionLocal, engine
from datetime import date
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Initialize FastAPI app
app = FastAPI()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# # Password hashing setup
# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
# SECRET_KEY = "your-secret-key-here"  # Replace with a secure key

# Pydantic models for request validation
class UserCreate(BaseModel):
    username: str
    password: str

class ExpenseCreate(BaseModel):
    category: str
    amount: float
    date : date

class IncomeCreate(BaseModel):
    source: str
    amount: float
    date : date

class BudgetCreate(BaseModel):
    category: str
    budget_amount: float

class BudgetUpdate(BaseModel):
    new_amount: float


# Pydantic model for login requests
class LoginRequest(BaseModel):
    username: str
    password: str

# --------------------------
# User Authentication Endpoints
# --------------------------

# Register endpoint
@app.post("/register", status_code=201)
def register(username: str, password: str, db: Session = Depends(get_db)):
    existing_user = crud.get_user_by_username(db=db, username=username)
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")
    
    crud.create_user(db=db, username=username, password=password)
    return {"message": "User created successfully"}

# Login endpoint
@app.post("/login")
def login(request: LoginRequest, db: Session = Depends(get_db)):
    user = crud.get_user_by_credentials(db=db, username=request.username, password=request.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    return {"user_id": user.id}

# --------------------------
# Expense Management Endpoints
# --------------------------

@app.post("/add-expense/{user_id}", status_code=201)
def add_expense(user_id: int, expense: ExpenseCreate, db: Session = Depends(get_db)):
    try:
        new_expense = crud.add_expense_db(db=db, user_id=user_id, category=expense.category, amount=expense.amount, date=expense.date)
        
        # Call the function to update the summary
        db.execute(text("SELECT populate_income_expense_summary(:user_id)"), {"user_id": user_id})
        db.commit()

        return {"message": "Expense added successfully", "expense_id": new_expense.id}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))



@app.get("/totals/{user_id}")
def get_totals(user_id: int, db: Session = Depends(get_db)):
    total_income = db.query(func.sum(Income.amount)).filter(Income.user_id == user_id).scalar() or 0
    total_expenses = db.query(func.sum(Expense.amount)).filter(Expense.user_id == user_id).scalar() or 0
    net_savings = total_income - total_expenses

    return {
        "total_income": total_income,
        "total_expenses": total_expenses,
        "net_savings": net_savings
    }




@app.get("/expenses/{user_id}")
def get_expenses(user_id: int, db: Session = Depends(get_db)):
    try:
        expenses = crud.get_expenses_by_user(db=db, user_id=user_id)
        return expenses
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# --------------------------
# Income Management Endpoints
# --------------------------

@app.post("/add-income/{user_id}", status_code=201)
def add_income(user_id: int, income: IncomeCreate, db: Session = Depends(get_db)):
    try:
        new_income = crud.add_income_db(db=db, user_id=user_id, source=income.source, amount=income.amount, date=income.date)
        
        # Call the function to update the summary
        db.execute(text("SELECT populate_income_expense_summary(:user_id)"), {"user_id": user_id})
        db.commit()

        return {"message": "Income added successfully", "income_id": new_income.id}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/income/{user_id}")
def get_income(user_id: int, db: Session = Depends(get_db)):
    try:
        incomes = crud.get_incomes_by_user(db=db, user_id=user_id)
        return incomes
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# --------------------------
# Budget Management Endpoints
# --------------------------

@app.post("/budgets/{user_id}", status_code=201)
def create_budget(user_id: int, budget: BudgetCreate, db: Session = Depends(get_db)):
    try:
        new_budget = crud.create_budget_db(db=db, user_id=user_id, category=budget.category, budget_amount=budget.budget_amount)
        return {"message": "Budget created successfully", "budget_id": new_budget.id}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.put("/budgets/{budget_id}")
def update_budget(budget_id: int, budget_update: BudgetUpdate, db: Session = Depends(get_db)):
    try:
        updated_budget = crud.update_budget_db(db=db, budget_id=budget_id, new_amount=budget_update.new_amount)
        return {"message": "Budget updated successfully", "budget_id": updated_budget.id}
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))





@app.delete("/budgets/{budget_id}")
def delete_budget(budget_id: int, db: Session = Depends(get_db)):
    try:
        crud.delete_budget_db(db=db, budget_id=budget_id)
        return {"message": "Budget deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
    
    

@app.get("/budgets/{user_id}")
def get_budgets(user_id: int, db: Session = Depends(get_db)):
    try:
        budgets = crud.get_budgets_by_user(db=db, user_id=user_id)
        return budgets
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# --------------------------
# Financial Summary Endpoint
# --------------------------

@app.get("/financial-summary/{user_id}")
def get_financial_summary(user_id: int, db: Session = Depends(get_db)):
    try:
        summary = crud.get_financial_summary_db(db=db, user_id=user_id)
        if not summary:
            raise HTTPException(status_code=404, detail=f"No financial summary found for user ID {user_id}")
        return summary
    except Exception as e:
        logger.error(f"Error fetching financial summary: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.get("/expense-breakdown/{user_id}")
def get_expense_breakdown(user_id: int, db: Session = Depends(get_db)):
    try:
        expense_breakdown = crud.get_expense_breakdown(db=db, user_id=user_id)
        if not expense_breakdown:
            raise HTTPException(status_code=404, detail=f"No expense breakdown found for user ID {user_id}")
        return {"categories": expense_breakdown}
    except Exception as e:
        logger.error(f"Error fetching expense breakdown: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
