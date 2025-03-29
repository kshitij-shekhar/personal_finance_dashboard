-- Function to calculate the total expenses for a user
CREATE OR REPLACE FUNCTION get_total_expenses(user_id_param INT)
RETURNS DECIMAL AS $$
DECLARE
    total DECIMAL;
BEGIN
    SELECT COALESCE(SUM(amount), 0) INTO total
    FROM expenses
    WHERE user_id = user_id_param;
    
    RETURN total;
END;
$$ LANGUAGE plpgsql;

-- Function to calculate the total income for a user
CREATE OR REPLACE FUNCTION get_total_income(user_id_param INT)
RETURNS DECIMAL AS $$
DECLARE
    total_income DECIMAL;
BEGIN
    SELECT COALESCE(SUM(amount), 0) INTO total_income
    FROM income
    WHERE user_id = user_id_param;

    RETURN total_income;
END;
$$ LANGUAGE plpgsql;




-- Function to calculate net savings for a user
CREATE OR REPLACE FUNCTION get_net_savings(user_id_param INT)
RETURNS DECIMAL AS $$
DECLARE
    expenses DECIMAL;
    income DECIMAL;
BEGIN
    expenses := get_total_expenses(user_id_param);
    income := get_total_income(user_id_param);
    
    RETURN income - expenses;
END;
$$ LANGUAGE plpgsql;


-- Function to calculate expense breakdown by category
CREATE OR REPLACE FUNCTION get_expense_breakdown(user_id_param INT)
RETURNS TABLE(category TEXT, total DECIMAL) AS $$
BEGIN
    RETURN QUERY
    SELECT e.category::TEXT, COALESCE(SUM(e.amount), 0) AS total  -- Cast to TEXT
    FROM expenses e
    WHERE e.user_id = user_id_param
    GROUP BY e.category
    ORDER BY total DESC;
END;
$$ LANGUAGE plpgsql;



CREATE OR REPLACE FUNCTION get_savings_recommendations(user_id_param INT)
RETURNS TABLE(recommendation TEXT) AS $$
BEGIN
    RETURN QUERY 
    SELECT CASE 
               WHEN (SELECT SUM(amount) FROM expenses WHERE user_id = user_id_param) > 
                    (SELECT SUM(amount) FROM income WHERE user_id = user_id_param) THEN 
                   'Consider reducing your discretionary spending.'
               ELSE 
                   'You are within your budget; keep saving!'
           END AS recommendation;
END;
$$ LANGUAGE plpgsql;



CREATE OR REPLACE FUNCTION get_financial_health_score(user_id_param INT)
RETURNS TABLE(score INT) AS $$
BEGIN
   RETURN QUERY 
   SELECT CASE 
              WHEN (SELECT SUM(amount) FROM income WHERE user_id = user_id_param) - 
                   (SELECT SUM(amount) FROM expenses WHERE user_id = user_id_param) > 1000 THEN 
                   5 -- Excellent health score
              WHEN (SELECT SUM(amount) FROM income WHERE user_id = user_id_param) - 
                   (SELECT SUM(amount) FROM expenses WHERE user_id = user_id_param) BETWEEN 500 AND 1000 THEN 
                   4 -- Good health score
              ELSE 
                   3 -- Needs improvement score
          END AS score;
END;
$$ LANGUAGE plpgsql;



CREATE OR REPLACE FUNCTION populate_income_expense_summary(uid INT) RETURNS INT AS $$
DECLARE
    affected_rows INT;
BEGIN
    WITH income_summary AS (
        SELECT user_id, 
               EXTRACT(YEAR FROM date) AS year, 
               EXTRACT(MONTH FROM date) AS month, 
               SUM(amount) AS total_income
        FROM income
        WHERE user_id = uid
        GROUP BY user_id, year, month
    ),
    expense_summary AS (
        SELECT user_id, 
               EXTRACT(YEAR FROM date) AS year, 
               EXTRACT(MONTH FROM date) AS month, 
               SUM(amount) AS total_expenses
        FROM expenses
        WHERE user_id = uid
        GROUP BY user_id, year, month
    )
    INSERT INTO income_expense_summary (user_id, year, month, total_income, total_expenses)
    SELECT 
        COALESCE(i.user_id, e.user_id) AS user_id,
        COALESCE(i.year, e.year) AS year,
        COALESCE(i.month, e.month) AS month,
        COALESCE(i.total_income, 0) AS total_income,
        COALESCE(e.total_expenses, 0) AS total_expenses
    FROM income_summary i
    FULL OUTER JOIN expense_summary e
    ON i.user_id = e.user_id AND i.year = e.year AND i.month = e.month
    ON CONFLICT (user_id, year, month) 
    DO UPDATE SET 
        total_income = EXCLUDED.total_income, 
        total_expenses = EXCLUDED.total_expenses;

    -- Get number of rows affected
    GET DIAGNOSTICS affected_rows = ROW_COUNT;

    RETURN affected_rows;  -- Return count of rows inserted/updated
END;
$$ LANGUAGE plpgsql;



CREATE OR REPLACE FUNCTION get_total_liabilities(user_id_input INT) 
RETURNS NUMERIC AS $$
BEGIN
    RETURN (
        SELECT COALESCE(SUM(amount), 0) 
        FROM debts 
        WHERE user_id = user_id_input
    );
END;
$$ LANGUAGE plpgsql;



CREATE OR REPLACE FUNCTION get_total_assets(p_user_id INT) 
RETURNS NUMERIC AS $$
DECLARE 
    total_assets NUMERIC;
BEGIN
    SELECT COALESCE(SUM(value), 0) INTO total_assets 
    FROM assets WHERE user_id = p_user_id;
    
    RETURN total_assets;
END;
$$ LANGUAGE plpgsql;



CREATE OR REPLACE FUNCTION get_net_worth(p_user_id INT) 
RETURNS NUMERIC AS $$
DECLARE 
    total_assets NUMERIC;
    total_liabilities NUMERIC;
    net_worth NUMERIC;
BEGIN
    SELECT get_total_assets(p_user_id) INTO total_assets;
    SELECT get_total_liabilities(p_user_id) INTO total_liabilities;
    
    net_worth := total_assets - total_liabilities;
    
    RETURN net_worth;
END;
$$ LANGUAGE plpgsql;

-- psql -U your_username -d db_name -a -f backend/db/functions.sql
