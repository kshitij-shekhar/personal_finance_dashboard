import streamlit as st
import requests
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
# Initialize session states for all toggleable sections
if 'show_sections' not in st.session_state:
    st.session_state.show_sections = {
        'register': False,
        'add_expense': False,
        'view_expenses': False,
        'savings': False,
        'financial_report': False,
        'total_expenses': False,
        'total_income': False,
        'net_savings': False,
        'expense_breakdown':False,
        'financial_summary':False,
        'budget':False,
        'savings_recommendations':False,
        'financial_health':False

    }


# User Registration and Login
def authenticate_user():
    st.title("User Authentication")
    choice = st.selectbox("Select an option", ["Login", "Register"])

    if choice == "Login":
        username = st.text_input("Username")
        password = st.text_input("Password", type='password')
        if st.button("Login"):
            response = requests.post(f"http://localhost:8000/login", json={"username": username, "password": password})
            if response.status_code == 200:
                st.session_state.user_id = response.json()['user_id']  # Store user ID in session state
                st.session_state.username = username
                st.success("Login successful!")
            else:
                st.error("Invalid username or password")

    elif choice == "Register":
        username = st.text_input("Choose a Username")
        password = st.text_input("Choose a Password", type='password')
        if st.button("Register"):
            response = requests.post(f"http://localhost:8000/register", json={"username": username, "password": password})
            if response.status_code == 201:
                st.success("Registration successful! You can now log in.")
            else:
                st.error("Registration failed. Please try again.")



def toggle_section(section_name):
    st.session_state.show_sections[section_name] = not st.session_state.show_sections[section_name]

st.title("Personal Finance Dashboard")

# User Registration Section
with st.container():
    st.header("User Registration")
    username = st.text_input("Username", key="reg_user")
    password = st.text_input("Password", type='password', key="reg_pass")
    
    if st.button("Register"):
        toggle_section('register')
    
    if st.session_state.show_sections['register']:
        response = requests.post("http://localhost:8000/users/", 
                               json={"username": username, "password": password})
        if response.status_code == 200:
            st.success("User created successfully!")
        else:
            st.error("Error creating user.")


# Expense Input Section
with st.container():
    st.header("Add Expense")
    user_id = st.number_input("User ID", min_value=1, key="expense_user")
    amount = st.number_input("Amount", min_value=0.01, key="expense_amount")
    category = st.text_input("Category", key="expense_cat")
    date = st.date_input("Date", key="expense_date")
    
    if st.button("Add Expense"):
        toggle_section('add_expense')
    
    if st.session_state.show_sections['add_expense']:
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


# View Expenses Section
with st.container():
    st.header("View Expenses")
    if st.button("Show Expenses"):
        toggle_section('view_expenses')
    
    if st.session_state.show_sections['view_expenses']:
        expenses_response = requests.get(f"http://localhost:8000/expenses/{user_id}")
        if expenses_response.status_code == 200:
            expenses_data = expenses_response.json()
            for expense in expenses_data:
                st.write(expense)
        else:
            st.error("Error fetching expenses.")


# Savings Calculator Section
with st.container():
    st.header("Savings Calculator")
    if st.button("Calculate Monthly Savings"):
        toggle_section('savings')
    
    if st.session_state.show_sections['savings']:
        response = requests.post(f"http://localhost:8000/calculate-savings/{user_id}")
        if response.json()["status"] == "success":
            st.success("Savings updated!")
        else:
            st.error("Calculation failed")


# # Financial Report Section
# with st.container():
#     st.header("Financial Report")
#     if st.button("Generate Report"):
#         toggle_section('financial_report')
    
#     if st.session_state.show_sections['financial_report']:
#         report = requests.get(f"http://localhost:8000/financial-report/{user_id}").json()
#         st.write(f"User: {report['username']}")
#         col1, col2, col3 = st.columns(3)
#         col1.metric("Total Income", f"${report['total_income']}")
#         col2.metric("Total Expenses", f"${report['total_expenses']}")
#         col3.metric("Net Savings", f"${report['net_savings']}")



# Total Expenses Section
with st.container():
    st.header("Total Expenses")
    if st.button("Get Total Expenses"):
        toggle_section('total_expenses')
    
    if st.session_state.show_sections['total_expenses']:
        # Make the API request
        response = requests.get(f"http://localhost:8000/total-expenses/{user_id}")
        
        # Check if the response is valid
        if response.status_code == 200:
            try:
                data = response.json()  # Attempt to parse JSON
                total_expenses = data.get('total_expenses', 'N/A')  # Get 'total_expenses' or 'N/A'
                st.write(f"Total Expenses: ${total_expenses}")
            except requests.exceptions.JSONDecodeError:
                st.error("Failed to decode JSON from the server response.")
        else:
            st.error(f"Error fetching total expenses: {response.status_code}")
    




# Total Income Section
with st.container():
    st.header("Total Income")
    if st.button("Get Total Income"):
        toggle_section('total_income')
    
    if st.session_state.show_sections['total_income']:
        response = requests.get(f"http://localhost:8000/total-income/{user_id}")
        
        # Check if the response is valid
        if response.status_code == 200:
            try:
                data = response.json()  # Attempt to parse JSON
                total_income = data.get('total_income', 'N/A')  # Get 'total_income' or 'N/A'
                st.write(f"Total Income: ${total_income}")
            except requests.exceptions.JSONDecodeError:
                st.error("Failed to decode JSON from the server response.")
        else:
            st.error(f"Error fetching total income: {response.status_code}")

        




# Net Savings Section
with st.container():
    st.header("Net Savings")
    if st.button("Get Net Savings"):
        toggle_section('net_savings')
    
    if st.session_state.show_sections['net_savings']:
        response = requests.get(f"http://localhost:8000/net-savings/{user_id}")
        
        # Check if the response is valid
        if response.status_code == 200:
            try:
                data = response.json()  # Attempt to parse JSON
                net_savings = data.get('net_savings', 'N/A')  # Get 'net_savings' or 'N/A'
                st.write(f"Net Savings: ${net_savings}")
            except requests.exceptions.JSONDecodeError:
                st.error("Failed to decode JSON from server response.")
        else:
            st.error(f"Error fetching net savings: {response.status_code}")

        



# Add functionality for Expense Breakdown By Category
with st.container():
    st.header("Expense Breakdown by Category")
    if st.button("Show Expense Breakdown"):
        toggle_section('expense_breakdown')

    if st.session_state.show_sections['expense_breakdown']:
        response = requests.get(f"http://localhost:8000/expense-breakdown/{user_id}")
        
        if response.status_code == 200:
            try:
                data = response.json()
                # Check if data['categories'] is a list before iterating
                if isinstance(data.get('categories', []), list):
                    for category in data['categories']:
                        st.write(f"{category['category']}: ${category['total']}") 
                else:
                    st.error("Invalid data format received.")
            except requests.exceptions.JSONDecodeError:
                st.error("Failed to decode JSON from server response.")
        else:
            st.error(f"Error fetching expense breakdown: {response.status_code}")


with st.container():
    st.header("Financial Summary Dashboard")
    if st.button("Show Financial Summary"):
        toggle_section('financial_summary')

    if st.session_state.show_sections['financial_summary']:
        response = requests.get(f"http://localhost:8000/financial-summary/{user_id}")
        
        if response.status_code == 200:
            data = response.json()
            print(data)
            st.write(f"Username: {data['username']}")
            st.write(f"Savings Goal: ${data['savings_goal']}")
            st.write(f"Current Savings: ${data['current_savings']}")
            st.write(f"Savings Progress: {data['savings_progress_percentage']}%")
            st.write(f"Expense-to-Income Ratio: {data['expense_to_income_ratio']}%")
        else:
            st.error(f"Error fetching financial summary: {response.status_code}")

        if st.button("Close Financial Summary"):
            toggle_section('financial_summary')




        
# with st.container():
#     st.header("Budgeting Tool")
#     if st.button("Show Budgets"):
#         toggle_section('budget')

#     if st.session_state.show_sections['budget']:
#         response = requests.get(f"http://localhost:8000/budget/{user_id}")
        
#         if response.status_code == 200:
#             data = response.json()
#             for budget in data['budgets']:
#                 st.write(f"{budget['category']}: ${budget['budget']}")
#         else:
#             st.error(f"Error fetching budgets: {response.status_code}")

        
with st.container():
    st.header("Savings Recommendations")
    if st.button("Get Recommendations"):
        toggle_section('savings_recommendations')

    if st.session_state.show_sections['savings_recommendations']:
        response = requests.get(f"http://localhost:8000/savings-recommendations/{user_id}")
        
        if response.status_code == 200:
            data = response.json()
            st.write(data['recommendation'])
        else:
            st.error(f"Error fetching recommendations: {response.status_code}")

        if st.button("Close Recommendations"):
            toggle_section('savings_recommendations')




with st.container():
    st.header("Monthly Financial Health Check")
    if st.button("Check Financial Health"):
        toggle_section('financial_health')

    if st.session_state.show_sections['financial_health']:
        response = requests.get(f"http://localhost:8000/financial-health-score/{user_id}")
        
        if response.status_code == 200:
            data = response.json()
            st.write(f"Your Financial Health Score is: {data['score']}")
        else:
            st.error(f"Error fetching financial health score: {response.status_code}")

        if st.button("Close Financial Health Check"):
            toggle_section('financial_health')


with st.container():
    st.header("Budgeting Tool")
    
    # Create a new budget
    st.subheader("Create New Budget")
    category = st.text_input("Category")
    amount = st.number_input("Budget Amount", min_value=0.0)
    
    if st.button("Create Budget"):
        response = requests.post(f"http://localhost:8000/budgets/{user_id}", json={"category": category, "budget_amount": amount})
        if response.status_code == 200:
            st.success("Budget created successfully!")
        else:
            st.error("Error creating budget.")
    
    # View existing budgets
    if st.button("View Budgets"):
        response = requests.get(f"http://localhost:8000/budgets/{user_id}")
        if response.status_code == 200:
            data = response.json()
            for budget in data['budgets']:
                st.write(f"Category: {budget['category']}, Amount: ${budget['budget_amount']}")
                # Optionally add update and delete buttons here for each budget entry
                if st.button(f"Update Budget for {budget['category']}"):
                    new_amount = st.number_input(f"New Amount for {budget['category']}", min_value=0.0)
                    update_response = requests.put(f"http://localhost:8000/budgets/{budget['id']}", json={"budget_amount": new_amount})
                    if update_response.status_code == 200:
                        st.success("Budget updated successfully!")
                    else:
                        st.error("Error updating budget.")

                if st.button(f"Delete Budget for {budget['category']}"):
                    delete_response = requests.delete(f"http://localhost:8000/budgets/{budget['id']}")
                    if delete_response.status_code == 200:
                        st.success("Budget deleted successfully!")
                    else:
                        st.error("Error deleting budget.")
        else:
            st.error("Error fetching budgets.")




# Check if user is logged in
if 'user_id' not in st.session_state:
    authenticate_user()
else:
    # Fetch financial summary data
    user_id = st.session_state.user_id
    response_summary = requests.get(f"http://localhost:8000/financial-summary/{user_id}")
    financial_summary = response_summary.json() if response_summary.status_code == 200 else {}

    # Fetch expense breakdown data
    response_expenses = requests.get(f"http://localhost:8000/expense-breakdown/{user_id}")
    expense_data = response_expenses.json()["categories"] if response_expenses.status_code == 200 else []

    # Sample time-series data (replace with your actual time-series data)
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]
    income_data = [5000, 5500, 6000, 5800, 6200, 6500]  # Replace with API data
    expenses_data = [4000, 4200, 4500, 4300, 4600, 4800]  # Replace with API data
    savings_data = [1000, 1300, 1500, 1500, 1600, 1700]  # Replace with API data

    # Sample categorical data (replace with API data)
    expense_categories = [item["category"] for item in expense_data]
    expense_amounts = [item["total"] for item in expense_data]

    # Create a DataFrame for heatmap
    heatmap_data = pd.DataFrame({
        "Month": months * len(expense_categories),
        "Category": [cat for cat in expense_categories for _ in months],
        "Expense": [amt * (i + 1) for i, amt in enumerate(expense_amounts) for _ in months]  # Mock data
    })
    # ------------------------------
    # Dashboard Layout
    # ------------------------------
    st.title("Personal Finance Dashboard")

    # ------------------------------
    # Section: Key Metrics (Cards)
    # ------------------------------
    st.header("Key Metrics")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Income", f"${financial_summary.get('total_income', 0):.2f}")
    with col2:
        st.metric("Total Expenses", f"${financial_summary.get('total_expenses', 0):.2f}")
    with col3:
        st.metric("Net Savings", f"${financial_summary.get('net_savings', 0):.2f}")

    # ------------------------------
    # Section: Visualizations
    # ------------------------------
    
    # Line Chart (Income vs Expenses)
    fig_line = go.Figure()
    fig_line.add_trace(go.Scatter(
        x=months,
        y=income_data,
        mode='lines+markers',
        name='Income',
        line=dict(color='#2ecc71')
    ))
    
    fig_line.add_trace(go.Scatter(
        x=months,
        y=expenses_data,
        mode='lines+markers',
        name='Expenses',
        line=dict(color='#e74c3c')
    ))
    
    fig_line.update_layout(
        title="Income vs Expenses Over Time",
        xaxis_title="Month",
        yaxis_title="Amount ($)",
        hovermode="x unified"
    )
    
    st.plotly_chart(fig_line)

    # Bar Chart (Expenses by Category)
    fig_bar = px.bar(
        x=expense_categories,
        y=expense_amounts,
        labels={'x': 'Category', 'y': 'Amount ($)'},
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    
    st.plotly_chart(fig_bar)

# ------------------------------
# Action Buttons Section
# ------------------------------
st.header("Manage Your Finances")

if st.button("Add Expense"):
   category = st.text_input("Category")
   amount = st.number_input("Amount", min_value=0.01)
   if st.button("Submit Expense"):
       response_add_expense = requests.post(f"http://localhost:8000/add-expense/{user_id}", json={"category": category, "amount": amount})
       if response_add_expense.status_code == 200:
           st.success("Expense added successfully!")
       else:
           st.error("Failed to add expense.")

if st.button("Add Income"):
   source = st.text_input("Income Source")
   amount_income = st.number_input("Income Amount", min_value=0.01)
   if st.button("Submit Income"):
       response_add_income = requests.post(f"http://localhost:8000/add-income/{user_id}", json={"source": source, "amount": amount_income})
       if response_add_income.status_code == 200:
           st.success("Income added successfully!")
       else:
           st.error("Failed to add income.")

if st.button("Create New Budget"):
   budget_category = st.text_input("Budget Category")
   budget_amount = st.number_input("Budget Amount", min_value=0.01)
   if st.button("Submit Budget"):
       response_create_budget = requests.post(f"http://localhost:8000/budgets/{user_id}", json={"category": budget_category, "budget_amount": budget_amount})
       if response_create_budget.status_code == 200:
           st.success("Budget created successfully!")
       else:
           st.error("Failed to create budget.")

if st.button("Update Budget"):
   budget_id_to_update = st.number_input("Budget ID to Update")
   new_budget_amount = st.number_input("New Budget Amount", min_value=0.01)
   if st.button("Submit Update"):
       response_update_budget = requests.put(f"http://localhost:8000/budgets/{budget_id_to_update}", json={"budget_amount": new_budget_amount})
       if response_update_budget.status_code == 200:
           st.success("Budget updated successfully!")
       else:
           st.error("Failed to update budget.")

if st.button("Delete Budget"):
   budget_id_to_delete = st.number_input("Budget ID to Delete")
   if st.button("Confirm Deletion"):
       response_delete_budget = requests.delete(f"http://localhost:8000/budgets/{budget_id_to_delete}")
       if response_delete_budget.status_code == 200:
           st.success("Budget deleted successfully!")
       else:
           st.error("Failed to delete budget.")