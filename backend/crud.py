from sqlalchemy.orm import Session
import models, schemas
from sqlalchemy import text


def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(username=user.username, password=user.password)  # Hash password in production!
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def create_expense(db: Session, expense: schemas.ExpenseCreate):
    db_expense = models.Expense(**expense.dict())
    db.add(db_expense)
    db.commit()
    db.refresh(db_expense)
    return db_expense

def get_expenses_by_user(db: Session, user_id: int):
    return db.query(models.Expense).filter(models.Expense.user_id == user_id).all()

# Procedure
def calculate_savings(db: Session, user_id: int):
    try:
        db.execute(
            text("CALL update_savings(:user_id)"),
            {"user_id": user_id}
        )
        db.commit()
        return True
    except Exception as e:
        db.rollback()
        print(f"Error calculating savings: {e}")
        return False

# Create a function to query the view to see the financial report/summary


def get_financial_report(db: Session, user_id: int):
    return db.execute(
        text("SELECT * FROM financial_summary WHERE user_id = :user_id"),
        {"user_id": user_id}
    ).fetchone()

