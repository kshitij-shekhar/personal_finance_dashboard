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
        'net_savings': False
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
        # if st.button("Close Registration Result"):
        #     toggle_section('register')

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
        # if st.button("Close Expense Result"):
        #     toggle_section('add_expense')

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
        # if st.button("Close Expenses List"):
        #     toggle_section('view_expenses')

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
        # if st.button("Close Savings Calculator"):
        #     toggle_section('savings')

# Financial Report Section
with st.container():
    st.header("Financial Report")
    if st.button("Generate Report"):
        toggle_section('financial_report')
    
    if st.session_state.show_sections['financial_report']:
        report = requests.get(f"http://localhost:8000/financial-report/{user_id}").json()
        st.write(f"User: {report['username']}")
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Income", f"${report['total_income']}")
        col2.metric("Total Expenses", f"${report['total_expenses']}")
        col3.metric("Net Savings", f"${report['net_savings']}")
        # if st.button("Close Report"):
        #     toggle_section('financial_report')


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

        # Add a button to close the section
        if st.button("Close Net Savings"):
            toggle_section('net_savings')


