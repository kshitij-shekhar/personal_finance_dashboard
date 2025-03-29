from sqlalchemy import Column, Integer, String, Float, ForeignKey, text  
from sqlalchemy.orm import Session
from backend.models import User, Expense, Income, Budget

# User CRUD Operations
def create_user(db: Session, username: str, password: str):
    new_user = User(username=username, password=password)  # Store plain text
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

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
