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

# Incorporate functions.sql : 

def get_total_expenses(db: Session, user_id: int):
    try:
        result = db.execute(
            text("SELECT get_total_expenses(:user_id) AS total"),
            {"user_id": user_id}
        ).fetchone()
        return result.total if result else 0
    except Exception as e:
        print(f"Error fetching total expenses: {e}")
        return 0



def get_total_income(db: Session, user_id: int):
    try:
        result = db.execute(
            text("SELECT get_total_income(:user_id) AS total"),
            {"user_id": user_id}
        ).fetchone()
        
        return result.total if result and result.total is not None else 0  # Return 0 if no result or total is None
    except Exception as e:
        print(f"Error fetching total income: {e}")
        return 0  # Return 0 on error



def get_net_savings(db: Session, user_id: int):
    try:
        result = db.execute(
            text("SELECT get_net_savings(:user_id_param) AS net_savings"),
            {"user_id_param": user_id}  # Use the updated parameter name
        ).fetchone()
        
        return result.net_savings if result and result.net_savings is not None else 0  # Return 0 if no result or net_savings is None
    except Exception as e:
        print(f"Error fetching net savings: {e}")
        return 0  # Return 0 on error





def get_expense_breakdown(db: Session, user_id: int):
    try:
        result = db.execute(
            text("SELECT * FROM get_expense_breakdown(:user_id_param)"),
            {"user_id_param": user_id}
        ).fetchall()
    
        return [{"category": row.category, "total": row.total} for row in result]
    except Exception as e:
        print(f"Error fetching net savings: {e}")
        return 0  # Return 0 on error

