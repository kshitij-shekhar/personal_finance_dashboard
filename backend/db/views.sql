
-- CREATE OR REPLACE VIEW financial_summary AS
-- SELECT 
--     u.id AS user_id,
--     u.username,
--     COALESCE(inc.total_income, 0) AS total_income,
--     COALESCE(exp.total_expenses, 0) AS total_expenses,
--     COALESCE(inc.total_income, 0) - COALESCE(exp.total_expenses, 0) AS net_savings,
--     sg.goal_amount AS savings_goal,
--     sg.current_amount AS current_savings,
--     CASE 
--         WHEN sg.goal_amount > 0 THEN ROUND((sg.current_amount * 100.0 / sg.goal_amount), 2)
--         ELSE 0
--     END AS savings_progress_percentage,
--     CASE 
--         WHEN COALESCE(inc.total_income, 0) > 0 
--         THEN ROUND((COALESCE(exp.total_expenses, 0) * 100.0 / COALESCE(inc.total_income, 0)), 2)
--         ELSE 0
--     END AS expense_to_income_ratio
-- FROM users u
-- LEFT JOIN (
--     SELECT user_id, SUM(amount) AS total_income 
--     FROM income 
--     GROUP BY user_id
-- ) inc ON u.id = inc.user_id
-- LEFT JOIN (
--     SELECT user_id, SUM(amount) AS total_expenses 
--     FROM expenses 
--     GROUP BY user_id
-- ) exp ON u.id = exp.user_id
-- LEFT JOIN savings_goals sg ON u.id = sg.user_id;



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
