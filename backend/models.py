from sqlalchemy import Column, Integer, String, Float, ForeignKey,Date
from sqlalchemy.orm import relationship
from backend.database import Base

# User model
class User(Base):
    __tablename__ = "users"
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)  # Store plain-text passwords (as per your requirement)

    # Relationships
    expenses = relationship("Expense", back_populates="user", cascade="all, delete-orphan")
    incomes = relationship("Income", back_populates="user", cascade="all, delete-orphan")
    budgets = relationship("Budget", back_populates="user", cascade="all, delete-orphan")

# Expense model
class Expense(Base):
    __tablename__ = "expenses"
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    category = Column(String)
    amount = Column(Float)
    date = Column(Date, nullable=False)  # Ensure date is required

    user = relationship("User", back_populates="expenses")

# Income model
class Income(Base):
    __tablename__ = "income"
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    source = Column(String)
    amount = Column(Float)
    date = Column(Date, nullable=False) 
    
    # Relationship back to User
    user = relationship("User", back_populates="incomes")

# Budget model
class Budget(Base):
    __tablename__ = "budgets"
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    category = Column(String)
    budget_amount = Column(Float)

    # Relationship back to User
    user = relationship("User", back_populates="budgets")
