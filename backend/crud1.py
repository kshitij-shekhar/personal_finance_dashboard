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




# def get_financial_report(db: Session, user_id: int):
#     return db.execute(
#         text("SELECT * FROM financial_summary WHERE user_id = :user_id"),
#         {"user_id": user_id}
#     ).fetchone()

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
        print(f"Error fetching expense breakdown: {e}")
        return []


def get_financial_summary(db: Session, user_id: int):
    try:
        result = db.execute(
            text("SELECT * FROM financial_summary WHERE user_id = :user_id"),
            {"user_id": user_id}
        ).fetchone()
        
        if result:
            return {
                "username": result.username,
                "savings_goal": result.savings_goal,  # Ensure this matches your view definition
                "current_savings": result.current_savings,
                "savings_progress_percentage": result.savings_progress_percentage,
                "expense_to_income_ratio": result.expense_to_income_ratio
            }
        else:
            return None  # Handle case where no results are found
    except Exception as e:
        return None  # Return None or handle it as needed






# def get_budget(db: Session, user_id: int):
#     result = db.execute(
#         text("SELECT * FROM get_budget(:user_id_param)"),
#         {"user_id_param": user_id}
#     ).fetchall()
    
#     return [{"category": row.category, "budget": row.budget} for row in result]

def get_savings_recommendations(db: Session, user_id: int):
    result = db.execute(
        text("SELECT * FROM get_savings_recommendations(:user_id_param)"),
        {"user_id_param": user_id}
    ).fetchone()
    
    return result.recommendation if result else "No recommendations available."



def get_financial_health_score(db: Session, user_id: int):
    result = db.execute(
        text("SELECT * FROM get_financial_health_score(:user_id_param)"),
        {"user_id_param": user_id}
    ).fetchone()
    
    return result.score if result else "No score available."


#For budgeting tool

def create_budget(db: Session, user_id: int, category: str, budget_amount: float):
    db.execute(
        text("INSERT INTO budgets (user_id, category, budget_amount) VALUES (:user_id, :category, :budget_amount)"),
        {"user_id": user_id, "category": category, "budget_amount": budget_amount}
    )
    db.commit()

def get_budgets(db: Session, user_id: int):
    result = db.execute(
        text("SELECT * FROM budgets WHERE user_id = :user_id"),
        {"user_id": user_id}
    ).fetchall()
    
    return [{"id": row.id, "category": row.category, "budget_amount": row.budget_amount} for row in result]

def update_budget(db: Session, budget_id: int, budget_amount: float):
    db.execute(
        text("UPDATE budgets SET budget_amount = :budget_amount WHERE id = :budget_id"),
        {"budget_amount": budget_amount, "budget_id": budget_id}
    )
    db.commit()

def delete_budget(db: Session, budget_id: int):
    db.execute(
        text("DELETE FROM budgets WHERE id = :budget_id"),
        {"budget_id": budget_id}
    )
    db.commit()