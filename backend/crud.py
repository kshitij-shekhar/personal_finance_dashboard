from sqlalchemy import  text  
from sqlalchemy.orm import Session
from backend.models import User, Expense, Income, Budget
from backend.models import Debt, Asset
from datetime import date
from sqlalchemy.exc import SQLAlchemyError
import logging



# User CRUD Operations
def create_user(db: Session, username: str, password: str):
    new_user = User(username=username, password=password)  # Store plain text
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def update_savings(db: Session, user_id: int):
    db.execute(text("CALL update_savings(:user_id_param)"), {"user_id_param": user_id})
    db.commit()

def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()

def get_user_by_credentials(db: Session, username: str, password: str):
    user = db.query(User).filter(User.username == username).first()
    if user and user.password == password:  # Plain-text comparison
        return user
    return None

def fetch_income_expense_summary(db: Session, user_id: int):
    query = """
        SELECT 
            year,
            month,
            total_income,
            total_expenses 
        FROM income_expense_summary 
        WHERE user_id = :user_id
        ORDER BY year ASC, month ASC;
    """
    result = db.execute(text(query), {"user_id": user_id})
    return result.fetchall()

def check_user_data(db: Session, user_id: int):
    query = """
        SELECT COUNT(*) AS record_count 
        FROM income_expense_summary 
        WHERE user_id = :user_id;
    """
    result = db.execute(text(query), {"user_id": user_id}).fetchone()
    if result.record_count == 0:
        return "No income or expense data available for this user."
    elif result.record_count < 1:
        return "At least one month's income and expenses data is required to show the chart."
    return "Data available"


# Expense CRUD Operations
def add_expense_db(db: Session, user_id: int, category: str, amount: float, date):
    new_expense = Expense(user_id=user_id, category=category, amount=amount, date=date)
    db.add(new_expense)
    db.commit()
    db.refresh(new_expense)
    return new_expense


def get_expenses_by_user(db: Session, user_id: int):
    return db.query(Expense).filter(Expense.user_id == user_id).all()

# Income CRUD Operations
def add_income_db(db: Session, user_id: int, source: str, amount: float,date : str):
    new_income = Income(user_id=user_id, source=source, amount=amount,date=date)
    db.add(new_income)
    db.commit()
    db.refresh(new_income)
    return new_income

def get_incomes_by_user(db: Session, user_id: int):
    return db.query(Income).filter(Income.user_id == user_id).all()

# Budget CRUD Operations
def get_budgets_by_user(db: Session, user_id: int):
    return db.query(Budget).filter(Budget.user_id == user_id).all()

def create_budget_db(db: Session, user_id: int, category: str, budget_amount: float):
    new_budget = Budget(user_id=user_id, category=category,
                        budget_amount=budget_amount)
    
    db.add(new_budget)
    db.commit()
    db.refresh(new_budget)
    return new_budget

def update_budget_db(db: Session, budget_id: int, new_amount: float):
    budget = db.query(Budget).filter(Budget.id == budget_id).first()
    if not budget:
        raise Exception("Budget not found")
    
    budget.budget_amount = new_amount
    db.commit()
    db.refresh(budget)
    return budget

def delete_budget_db(db: Session, budget_id: int):
    budget = db.query(Budget).filter(Budget.id == budget_id).first()
    if not budget:
        raise Exception("Budget not found")
    
    db.delete(budget)
    db.commit()

# Financial Summary Operations
def get_financial_summary_db(db: Session, user_id: int):
    result = db.execute(
        text("SELECT * FROM financial_summary WHERE user_id = :user_id"),
        {"user_id": user_id}
    ).fetchone()

    if not result:
        raise Exception("No financial summary found for this user")

    return {
        "total_income": getattr(result, 'total_income', None),
        "total_expenses": getattr(result, 'total_expenses', None),
        "net_savings": getattr(result, 'net_savings', None),  
        "savings_goal": getattr(result, 'savings_goal', None),
        "current_savings": getattr(result, 'current_savings', None),
        "savings_progress_percentage": getattr(result, 'savings_progress_percentage', None),
        "expense_to_income_ratio": getattr(result, 'expense_to_income_ratio', None)
    }



# Expense Breakdown Operations
def get_expense_breakdown(db: Session, user_id: int):
    try:
        result = db.execute(
            text("SELECT * FROM get_expense_breakdown(:user_id_param)"),
            {"user_id_param": user_id}
        ).fetchall()

        if not result:
            return []

        return [{"category": row.category, "total": row.total} for row in result]
    
    except Exception as e:
        print(f"Error fetching expense breakdown: {e}")
        return []


# Assets and Debts :
def add_debt_db(db: Session, user_id: int, category: str, amount: float, date_incurred: date):
    try:
        new_debt = Debt(user_id=user_id, category=category, amount=amount, date_incurred=date_incurred)
        db.add(new_debt)
        db.commit()
        db.refresh(new_debt)
        return new_debt
    except SQLAlchemyError as e:
        db.rollback()
        raise Exception(f"Error adding debt: {str(e)}")

def delete_debt_db(db: Session, debt_id: int):
    try:
        debt = db.query(Debt).filter(Debt.id == debt_id).first()
        if not debt:
            raise Exception("Debt not found")
        db.delete(debt)
        db.commit()
    except SQLAlchemyError as e:
        db.rollback()
        raise Exception(f"Error deleting debt: {str(e)}")

def get_debts_by_user(db: Session, user_id: int):
    try:
        return db.query(Debt).filter(Debt.user_id == user_id).all()
    except SQLAlchemyError as e:
        raise Exception(f"Error fetching debts: {str(e)}")

# def add_asset_db(db: Session, user_id: int, category: str, value: float, date_added: date):
#     try:
#         new_asset = Asset(user_id=user_id, category=category, value=value, date_added=date_added)
#         db.add(new_asset)
#         db.commit()
#         db.refresh(new_asset)
#         return new_asset
#     except SQLAlchemyError as e:
#         db.rollback()
#         raise Exception(f"Error adding asset: {str(e)}")

logging.basicConfig(level=logging.ERROR)

def add_asset_db(db: Session, user_id: int, category: str, value: float, date_added: date):
    try:
        new_asset = Asset(user_id=user_id, category=category, value=value, date_added=date_added)
        db.add(new_asset)
        db.commit()
        db.refresh(new_asset)
        return new_asset
    except SQLAlchemyError as e:
        db.rollback()
        logging.error(f"Database error: {str(e)}")  # Log the actual SQL error
        raise Exception(f"Error adding asset: {str(e)}")



def delete_asset_db(db: Session, asset_id: int):
    try:
        asset = db.query(Asset).filter(Asset.id == asset_id).first()
        if not asset:
            raise Exception("Asset not found")
        db.delete(asset)
        db.commit()
    except SQLAlchemyError as e:
        db.rollback()
        raise Exception(f"Error deleting asset: {str(e)}")

def get_assets_by_user(db: Session, user_id: int):
    try:
        return db.query(Asset).filter(Asset.user_id == user_id).all()
    except SQLAlchemyError as e:
        raise Exception(f"Error fetching assets: {str(e)}")
