-- Create a financial summary view that joins users, income, expenses, and savings goals
CREATE OR REPLACE VIEW financial_summary AS
SELECT 
    u.id AS user_id,
    u.username,
    COALESCE(SUM(i.amount), 0) AS total_income,
    COALESCE(SUM(e.amount), 0) AS total_expenses,
    sg.goal_amount,
    sg.current_amount,
    (sg.current_amount - COALESCE(SUM(e.amount), 0)) AS net_savings
FROM users u
LEFT JOIN income i ON u.id = i.user_id
LEFT JOIN expenses e ON u.id = e.user_id
LEFT JOIN savings_goals sg ON u.id = sg.user_id
GROUP BY u.id, sg.goal_amount, sg.current_amount;

-- run the following to apply this view to the database
-- psql -U <your_username> -d <name_of_db> -a -f backend/db/views.sql
