import streamlit as st
import requests
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from sqlalchemy.orm import Session
from sqlalchemy import text
from backend.database import SessionLocal, engine
from backend import crud
import datetime

# Initialize session states for user authentication
if 'user_id' not in st.session_state:
    st.session_state.user_id = None

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
                st.success("Login successful!")
                st.rerun()  # Refresh to show dashboard
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


#  Function to fetch user data
def fetch_user_data(user_id):
    db: Session = SessionLocal()
    
    # Fetch income, expenses, and savings data
    income_query = "SELECT SUM(amount) AS total_income FROM income WHERE user_id = :user_id"
    expenses_query = "SELECT SUM(amount) AS total_expenses FROM expenses WHERE user_id = :user_id"
    # savings_query = "SELECT amount FROM savings WHERE user_id = :user_id"  # Assuming you have a savings table

    total_income = db.execute(text(income_query), {"user_id": user_id}).scalar() or 0
    total_expenses = db.execute(text(expenses_query), {"user_id": user_id}).scalar() or 0
    # savings_amount = db.execute(text(savings_query), {"user_id": user_id}).scalars().all()
    
    return total_income, total_expenses




# def populate_income_expense_summary(user_id):
#     # Check if summary data exists for this user
#     query_check = """
#         SELECT COUNT(*) 
#         FROM income_expense_summary 
#         WHERE user_id = :user_id;
#     """
    
#     with engine.connect() as connection:
#         result = connection.execute(text(query_check), {"user_id": user_id}).fetchone()
    
#     if result[0] == 0:  # No records found for this user
#         # Populate summary from income and expenses tables
#         query_populate = """
#             INSERT INTO income_expense_summary (user_id, year, month, total_income, total_expenses)
#             SELECT 
#                 e.user_id,
#                 EXTRACT(YEAR FROM COALESCE(i.date, e.date)) AS year,
#                 EXTRACT(MONTH FROM COALESCE(i.date, e.date)) AS month,
#                 COALESCE(SUM(i.amount), 0) AS total_income,
#                 COALESCE(SUM(e.amount), 0) AS total_expenses
#             FROM users u
#             LEFT JOIN income i ON u.id = i.user_id
#             LEFT JOIN expenses e ON u.id = e.user_id
#             WHERE u.id = :user_id
#             GROUP BY e.user_id, year, month;
#         """
        
#         with engine.connect() as connection:
#             connection.execute(text(query_populate), {"user_id": user_id})


# def display_income_vs_expenses_chart(user_id):
#     db: Session = SessionLocal()  # Create a new database session

#     # Check if sufficient data exists
#     message = crud.check_user_data(db, user_id)
#     if message != "Data available":
#         st.warning(message)
#         return

#     # Fetch actual data from the database
#     data = crud.fetch_income_expense_summary(db, user_id)

#     if not data:
#         st.warning("No data available to display.")
#         return

#     # Prepare lists for months, income, and expenses
#     months = [f"{row.month}/{row.year}" for row in data]
#     income_data = [row.total_income for row in data]
#     expenses_data = [row.total_expenses for row in data]

#     # Create a line chart using Plotly
#     fig_line = go.Figure()

#     fig_line.add_trace(go.Scatter(
#         x=months,
#         y=income_data,
#         mode="lines+markers",
#         name="Income",
#         line=dict(color="#2ecc71")
#     ))

#     fig_line.add_trace(go.Scatter(
#         x=months,
#         y=expenses_data,
#         mode="lines+markers",
#         name="Expenses",
#         line=dict(color="#e74c3c")
#     ))

#     fig_line.update_layout(
#         title="Income vs Expenses Over Time",
#         xaxis_title="Month",
#         yaxis_title="Amount ($)",
#         hovermode="x unified"
#     )

#     st.plotly_chart(fig_line)


def populate_income_expense_summary(user_id):
    """
    Calls the SQL function populate_income_expense_summary to update the summary table.
    """
    with engine.connect() as connection:
        connection.execute(text("SELECT populate_income_expense_summary(:user_id);"), 
                           {"user_id": user_id})

def display_income_vs_expenses_chart(user_id):
    db: Session = SessionLocal()  # Create a new database session

    # **Ensure data is updated before displaying the chart**
    populate_income_expense_summary(user_id)

    # Check if sufficient data exists
    message = crud.check_user_data(db, user_id)
    if message != "Data available":
        st.warning(message)
        return

    # Fetch actual data from the database
    data = crud.fetch_income_expense_summary(db, user_id)

    if not data:
        st.warning("No data available to display.")
        return

    # Prepare lists for months, income, and expenses
    months = [f"{row.month}/{row.year}" for row in data]
    income_data = [row.total_income for row in data]
    expenses_data = [row.total_expenses for row in data]

    # Create a line chart using Plotly
    fig_line = go.Figure()

    fig_line.add_trace(go.Scatter(
        x=months,
        y=income_data,
        mode="lines+markers",
        name="Income",
        line=dict(color="#2ecc71")
    ))

    fig_line.add_trace(go.Scatter(
        x=months,
        y=expenses_data,
        mode="lines+markers",
        name="Expenses",
        line=dict(color="#e74c3c")
    ))

    fig_line.update_layout(
        title="Income vs Expenses Over Time",
        xaxis_title="Month",
        yaxis_title="Amount ($)",
        hovermode="x unified"
    )

    st.plotly_chart(fig_line)



def display_expense_heatmap(user_id):
    db: Session = SessionLocal()  # Create a new database session

    # Fetch expense breakdown by category and month
    query = """
        SELECT 
            EXTRACT(YEAR FROM e.date) AS year,
            EXTRACT(MONTH FROM e.date) AS month,
            e.category,
            SUM(e.amount) AS total_expense
        FROM 
            expenses e
        WHERE 
            e.user_id = :user_id
        GROUP BY 
            year, month, e.category
        ORDER BY 
            year, month;
    """
    
    result = db.execute(text(query), {"user_id": user_id}).fetchall()

    if not result:
        st.warning("No expense data available to display.")
        return

    # Prepare data for heatmap
    months = []
    categories = set()
    
    for row in result:
        year_month = f"{int(row.month)}/{int(row.year)}"
        months.append(year_month)
        categories.add(row.category)

    expense_matrix = pd.DataFrame(0, index=list(categories), columns=list(set(months)))

    for row in result:
        year_month = f"{int(row.month)}/{int(row.year)}"
        expense_matrix.at[row.category, year_month] += row.total_expense

    # Reset index to use it as a column in heatmap visualization
    expense_matrix.reset_index(inplace=True)
    
    # Melt the DataFrame for heatmap plotting
    heatmap_data = pd.melt(expense_matrix, id_vars='index', value_vars=expense_matrix.columns[1:], 
                            var_name='Month', value_name='Expense')
    
    heatmap_data.rename(columns={'index': 'Category'}, inplace=True)

    # Create heatmap using Plotly Express
    fig_heatmap = px.imshow(
        heatmap_data.pivot(index="Category", columns="Month", values="Expense"),
        labels=dict(x="Month", y="Category", color="Expense"),
        title="Expenses Heatmap by Category and Month",
        color_continuous_scale='Viridis'
    )
    
    st.plotly_chart(fig_heatmap)


# Function to display financial health check
def display_financial_health_check(total_income, total_expenses):
    st.header("Financial Health Check")
    
    financial_health_score = (total_income - total_expenses) / total_income * 100 if total_income > 0 else 0
    
    fig_gauge = go.Figure(go.Indicator(
        mode="gauge+number",
        value=financial_health_score,
        title={"text": "Financial Health Score"},
        gauge={
            "axis": {"range": [0, 100]},
            "bar": {"color": "green"},
            "steps": [
                {"range": [0, 50], "color": "red"},
                {"range": [50, 75], "color": "yellow"},
                {"range": [75, 100], "color": "lightgreen"},
            ],
        },
    ))
    
    st.plotly_chart(fig_gauge)

# Function to display budget allocation
def display_budget_allocation(user_id):
    st.header("Budget Allocation")
    
    query = """
        SELECT category, SUM(amount) AS total_expense 
        FROM expenses 
        WHERE user_id = :user_id 
        GROUP BY category;
    """
    
    db: Session = SessionLocal()
    results = db.execute(text(query), {"user_id": user_id}).fetchall()
    
    categories = [row.category for row in results]
    expenses = [row.total_expense for row in results]

    fig_bar = go.Figure(data=[
        go.Bar(x=categories, y=expenses)
    ])
    
    fig_bar.update_layout(title="Budget Allocation by Category", xaxis_title="Category", yaxis_title="Total Expenses")
    
    st.plotly_chart(fig_bar)

# Function to display net worth tracker
def display_net_worth_tracker(user_id):
    st.header("Net Worth Tracker")
    
    query_assets = """
        SELECT SUM(value) AS total_assets FROM assets WHERE user_id = :user_id;
    """
    
    # query_liabilities = """
    #     SELECT SUM(value) AS total_liabilities FROM liabilities WHERE user_id = :user_id;
    # """
    
    db: Session = SessionLocal()
    
    total_assets = db.execute(text(query_assets), {"user_id": user_id}).scalar() or 0
    # total_liabilities = db.execute(text(query_liabilities), {"user_id": user_id}).scalar() or 0
    total_liabilities=calculate_liabilities(user_id)
    net_worth = total_assets - total_liabilities
    
    fig_net_worth = go.Figure(go.Indicator(
        mode="number",
        value=net_worth,
        title={"text": "Net Worth"},
        number={"prefix": "$"},
        domain={'x': [0, 1], 'y': [0, 1]}
    ))
    
    st.plotly_chart(fig_net_worth)




# Function to calculate savings based on income and expenses
def calculate_savings(user_id):
    db: Session = SessionLocal()
    
    savings_query = """
        SELECT 
            year,
            month,
            (total_income - total_expenses) AS savings
        FROM income_expense_summary
        WHERE user_id = :user_id;
    """
    
    results = db.execute(text(savings_query), {"user_id": user_id}).fetchall()
    
    return pd.DataFrame(results)

# Function to calculate total liabilities
def calculate_liabilities(user_id):
    db: Session = SessionLocal()
    
    query_liabilities = """
        SELECT 
            SUM(amount) AS total_liabilities 
        FROM debts 
        WHERE user_id = :user_id;
    """
    
    return db.execute(text(query_liabilities), {"user_id": user_id}).scalar() or 0

# Function to display savings recommendations
def display_savings_recommendations(total_income, total_expenses):
    st.header("Savings Recommendations")
    
    monthly_savings_rate = (total_income - total_expenses) / total_income * 100 if total_income > 0 else 0
    print(type(total_income), type(0.20))
    recommended_savings = float(total_income) * 0.20  # Recommend saving 20% of income
    
    st.write(f"**Current Savings Rate:** {monthly_savings_rate:.2f}%")
    st.write(f"**Recommended Monthly Savings:** ${recommended_savings:.2f}")
    
    if (total_income - total_expenses) < recommended_savings:
        st.warning("You are not saving enough! Consider increasing your monthly savings.")
    else:
        st.success("Great job! You are meeting your savings goals.")

# Function to display liabilities
def display_liabilities(user_id):
    st.header("Total Liabilities")
    
    total_liabilities = calculate_liabilities(user_id)
    
    st.write(f"**Total Liabilities:** ${total_liabilities:.2f}")

# Function to display net financial position
def display_net_financial_position(user_id):
    st.header("Net Financial Position")
    
    total_income, total_expenses = fetch_user_data(user_id)
    
    # Calculate savings
    savings_df = calculate_savings(user_id)
    
    # Calculate liabilities
    total_liabilities = calculate_liabilities(user_id)
    
    # Calculate net financial position for each month
    net_financial_positions = []
    
    for index, row in savings_df.iterrows():
        net_position = row.savings - total_liabilities
        net_financial_positions.append(net_position)

    savings_df['net_financial_position'] = net_financial_positions
    
    # Plotting Net Financial Position
    fig_net_position = go.Figure()
    
    fig_net_position.add_trace(go.Scatter(
        x=savings_df['month'].astype(str) + '/' + savings_df['year'].astype(str),
        y=savings_df['net_financial_position'],
        mode='lines+markers',
        name='Net Financial Position',
        line=dict(color='blue')
    ))
    
    fig_net_position.update_layout(title="Net Financial Position Over Time",
                                    xaxis_title="Month/Year",
                                    yaxis_title="Net Position ($)")
    
    st.plotly_chart(fig_net_position)

# Function to display debt management insights
def display_debt_management(user_id):
    st.header("Debt Management Insights")
    
    query_debt = """
        SELECT category, SUM(amount) AS total_debt 
        FROM debts 
        WHERE user_id = :user_id 
        GROUP BY category;
    """
    
    db: Session = SessionLocal()
    
    results_debt = db.execute(text(query_debt), {"user_id": user_id}).fetchall()
    
    debt_categories = [row.category for row in results_debt]
    debts = [row.total_debt for row in results_debt]

    fig_debt_pie = go.Figure(data=[go.Pie(labels=debt_categories, values=debts)])
    
    fig_debt_pie.update_layout(title="Debt Distribution by Category")
    
    st.plotly_chart(fig_debt_pie)


# Check if user is logged in
if not st.session_state.user_id:
    authenticate_user()
else:
    user_id = st.session_state.user_id

    # Fetch financial summary data
    response_summary = requests.get(f"http://localhost:8000/financial-summary/{user_id}")
    financial_summary = response_summary.json() if response_summary.status_code == 200 else {}

    # Fetch expense breakdown data
    response_expenses = requests.get(f"http://localhost:8000/expense-breakdown/{user_id}")
    expense_data = response_expenses.json()["categories"] if response_expenses.status_code == 200 else []

    



    expense_categories = [item["category"] for item in expense_data]
    expense_amounts = [item["total"] for item in expense_data]

    

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
    
    # Display Income vs Expenses Chart
    populate_income_expense_summary(st.session_state.user_id)

    display_income_vs_expenses_chart(st.session_state.user_id)

   # Display Expense Heatmap
    display_expense_heatmap(st.session_state.user_id)

    # Create Bar Chart for Expenses by Category
    if expense_categories and expense_amounts:  # Ensure data is available
        fig_bar = px.bar(
            x=expense_categories,
            y=expense_amounts,
            labels={'x': 'Category', 'y': 'Amount ($)'},
            title="Expenses by Category",
            color=expense_categories,  # Optional: Color by category
        )
        st.plotly_chart(fig_bar)
    else:
        st.warning("No expense data available.")


    total_income, total_expenses = fetch_user_data(user_id)
   
    # Display all sections
    display_savings_recommendations(total_income, total_expenses)
    display_liabilities(user_id)
    display_net_financial_position(user_id)
    display_financial_health_check(total_income,total_expenses)
    display_budget_allocation(user_id)
    display_net_worth_tracker(user_id)
    display_debt_management(user_id)

# ------------------------------
# Action Buttons Section
# ------------------------------
st.header("Manage Your Finances")

# Initialize session state variables
if "expense_clicked" not in st.session_state:
    st.session_state.expense_clicked = False
if "income_clicked" not in st.session_state:
    st.session_state.income_clicked = False
if "budget_create_clicked" not in st.session_state:
    st.session_state.budget_create_clicked = False
if "budget_update_clicked" not in st.session_state:
    st.session_state.budget_update_clicked = False
if "budget_delete_clicked" not in st.session_state:
    st.session_state.budget_delete_clicked = False




def fetch_totals():
    user_id=st.session_state.user_id
    response = requests.get(f"http://localhost:8000/totals/{user_id}")
    if response.status_code == 200:
        return response.json()
    return {"total_income": 0, "total_expenses": 0, "net_savings": 0}

#  Fetch fresh totals on every run
totals = fetch_totals()






# -------------------- Add Expense --------------------
if st.button("Add Expense"):
    st.session_state.expense_clicked = not(st.session_state.expense_clicked)

if st.session_state.expense_clicked:
    user_id=st.session_state.user_id
    category = st.text_input("Category", key="expense_category")
    amount = st.number_input("Amount", min_value=0.01, key="expense_amount")
    date = st.date_input("Date", value=datetime.date.today(), key="expense_date")

    if st.button("Submit Expense"):
        payload = {"category": category, "amount": amount,"date":str(date)}

        response = requests.post(f"http://localhost:8000/add-expense/{user_id}", json=payload)
        
        if response.status_code == 201:
            st.success("Expense added successfully!")
            st.rerun()
        else:
            st.error(f"Failed to add expense. Server response: {response.text}")



# -------------------- Add Income --------------------
if st.button("Add Income"):
    st.session_state.income_clicked = not(st.session_state.income_clicked)

if st.session_state.income_clicked:
    user_id=st.session_state.user_id
    source = st.text_input("Income Source", key="income_source")
    amount_income = st.number_input("Income Amount", min_value=0.01, key="income_amount")
    date = st.date_input("Date", value=datetime.date.today()) 

    if st.button("Submit Income"):
        response = requests.post(f"http://localhost:8000/add-income/{user_id}", json={"source": source, "amount": amount_income,"date":str(date)})
        if response.status_code ==201:
            st.success("Income added successfully!")
            st.rerun()
        else:
            st.error(f"Failed to add income. Server response: {response.text}")

# -------------------- Create New Budget --------------------
if st.button("Create New Budget"):
    st.session_state.budget_create_clicked = not(st.session_state.budget_create_clicked)

if st.session_state.budget_create_clicked:
    budget_category = st.text_input("Budget Category", key="budget_category")
    budget_amount = st.number_input("Budget Amount", min_value=0.01, key="budget_amount")

    if st.button("Submit Budget"):
        response = requests.post(f"http://localhost:8000/budgets/{user_id}", json={"category": budget_category, "budget_amount": budget_amount})
        if response.status_code == 200:
            st.success("Budget created successfully!")
            st.session_state.budget_create_clicked = False
        else:
            st.error("Failed to create budget.")

# -------------------- Update Budget --------------------
if st.button("Update Budget"):
    st.session_state.budget_update_clicked = True

if st.session_state.budget_update_clicked:
    budget_id_to_update = st.number_input("Budget ID to Update", key="budget_id_update")
    new_budget_amount = st.number_input("New Budget Amount", min_value=0.01, key="new_budget_amount")

    if st.button("Submit Update"):
        response = requests.put(f"http://localhost:8000/budgets/{budget_id_to_update}", json={"budget_amount": new_budget_amount})
        if response.status_code == 200:
            st.success("Budget updated successfully!")
            st.session_state.budget_update_clicked = False
        else:
            st.error("Failed to update budget.")

# -------------------- Delete Budget --------------------
if st.button("Delete Budget"):
    st.session_state.budget_delete_clicked = True

if st.session_state.budget_delete_clicked:
    budget_id_to_delete = st.number_input("Budget ID to Delete", key="budget_id_delete")

    if st.button("Confirm Deletion"):
        response = requests.delete(f"http://localhost:8000/budgets/{budget_id_to_delete}")
        if response.status_code == 200:
            st.success("Budget deleted successfully!")
            st.session_state.budget_delete_clicked = False
        else:
            st.error("Failed to delete budget.")






















# if st.button("Add Expense"):
#    category = st.text_input("Category")
#    amount = st.number_input("Amount", min_value=0.01)
#    if st.button("Submit Expense"):
#        response_add_expense = requests.post(f"http://localhost:8000/add-expense/{user_id}", json={"category": category, "amount": amount})
#        if response_add_expense.status_code == 200:
#            st.success("Expense added successfully!")
#        else:
#            st.error("Failed to add expense.")




# if st.button("Add Income"):
#    source = st.text_input("Income Source")
#    amount_income = st.number_input("Income Amount", min_value=0.01)
#    if st.button("Submit Income"):
#        response_add_income = requests.post(f"http://localhost:8000/add-income/{user_id}", json={"source": source, "amount": amount_income})
#        if response_add_income.status_code == 200:
#            st.success("Income added successfully!")
#        else:
#            st.error("Failed to add income.")



# if st.button("Create New Budget"):
#    budget_category = st.text_input("Budget Category")
#    budget_amount = st.number_input("Budget Amount", min_value=0.01)
#    if st.button("Submit Budget"):
#        response_create_budget = requests.post(f"http://localhost:8000/budgets/{user_id}", json={"category": budget_category, "budget_amount": budget_amount})
#        if response_create_budget.status_code == 200:
#            st.success("Budget created successfully!")
#        else:
#            st.error("Failed to create budget.")

# if st.button("Update Budget"):
#    budget_id_to_update = st.number_input("Budget ID to Update")
#    new_budget_amount = st.number_input("New Budget Amount", min_value=0.01)
#    if st.button("Submit Update"):
#        response_update_budget = requests.put(f"http://localhost:8000/budgets/{budget_id_to_update}", json={"budget_amount": new_budget_amount})
#        if response_update_budget.status_code == 200:
#            st.success("Budget updated successfully!")
#        else:
#            st.error("Failed to update budget.")

# if st.button("Delete Budget"):
#    budget_id_to_delete = st.number_input("Budget ID to Delete")
#    if st.button("Confirm Deletion"):
#        response_delete_budget = requests.delete(f"http://localhost:8000/budgets/{budget_id_to_delete}")
#        if response_delete_budget.status_code == 200:
#            st.success("Budget deleted successfully!")
#        else:
#            st.error("Failed to delete budget.")
