import streamlit as st
import requests

st.title("Personal Finance Dashboard")

# User Registration/Login Section 
st.header("User Registration")
username = st.text_input("Username")
password = st.text_input("Password", type='password')

if st.button("Register"):
    response = requests.post("http://localhost:8000/users/", json={"username": username, "password": password})
    
    if response.status_code == 200:
        st.success("User created successfully!")
    else:
        st.error("Error creating user.")

# Expense Input Section 
st.header("Add Expense")
user_id = st.number_input("User ID", min_value=1)
amount = st.number_input("Amount", min_value=0.01)
category = st.text_input("Category")
date = st.date_input("Date")

if st.button("Add Expense"):
    expense_data = {
        "user_id": user_id,
        "amount": amount,
        "category": category,
        "date": str(date),
    }
    
    response = requests.post("http://localhost:8000/expenses/", json=expense_data)
    
    if response.status_code == 200:
        st.success("Expense added successfully!")
    else:
        st.error("Error adding expense.")

# Display Expenses Section 
st.header("View Expenses")
if st.button("Show Expenses"):
    expenses_response = requests.get(f"http://localhost:8000/expenses/{user_id}")
    
    if expenses_response.status_code == 200:
        expenses_data = expenses_response.json()
        for expense in expenses_data:
            st.write(expense)
    else:
        st.error("Error fetching expenses.")
