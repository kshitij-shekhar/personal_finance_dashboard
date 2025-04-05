
-- Updates income_expense_summary whenever called(during login, and when something is added/deleted)
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



CREATE OR REPLACE FUNCTION get_assets_by_category(p_user_id INT) 
RETURNS TABLE(category VARCHAR(50), total_value NUMERIC) AS $$
BEGIN
    RETURN QUERY
    SELECT a.category, COALESCE(SUM(a.value), 0) AS total_value
    FROM assets AS a
    WHERE a.user_id = p_user_id
    GROUP BY a.category;
END;
$$ LANGUAGE plpgsql;






CREATE OR REPLACE FUNCTION get_net_worth(p_user_id INT) 
RETURNS NUMERIC AS $$
DECLARE 
    total_assets NUMERIC;
    total_liabilities NUMERIC;
    net_worth NUMERIC;
BEGIN
    -- Calculate total assets by summing up category-wise asset values
    SELECT COALESCE(SUM(total_value), 0) INTO total_assets
    FROM get_assets_by_category(p_user_id);

    -- Get total liabilities
    SELECT get_total_liabilities(p_user_id) INTO total_liabilities;
    
    -- Compute net worth
    net_worth := total_assets - total_liabilities;
    
    RETURN net_worth;
END;
$$ LANGUAGE plpgsql;


-- psql -U your_username -d db_name -a -f backend/db/functions.sql
