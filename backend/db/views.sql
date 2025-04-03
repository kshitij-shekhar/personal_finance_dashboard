
CREATE OR REPLACE VIEW financial_summary AS
SELECT 
    u.id AS user_id,
    u.username,
    COALESCE(i.total_income, 0) AS total_income,
    COALESCE(e.total_expenses, 0) AS total_expenses,
    COALESCE(i.total_income, 0) - COALESCE(e.total_expenses, 0) AS net_savings
FROM users u
LEFT JOIN (
    -- Compute total income per user
    SELECT user_id, SUM(amount) AS total_income 
    FROM income 
    GROUP BY user_id
) i ON u.id = i.user_id
LEFT JOIN (
    -- Compute total expenses per user
    SELECT user_id, SUM(amount) AS total_expenses 
    FROM expenses 
    GROUP BY user_id
) e ON u.id = e.user_id;




-- run the following to apply this view to the database
-- psql -U <your_username> -d <name_of_db> -a -f backend/db/views.sql
