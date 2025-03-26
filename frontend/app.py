import streamlit as st
import requests

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
