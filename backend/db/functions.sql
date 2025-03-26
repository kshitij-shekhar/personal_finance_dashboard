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
    total DECIMAL;
BEGIN
    SELECT COALESCE(SUM(amount), 0) INTO total
    FROM income
    WHERE user_id = user_id_param;  

    RETURN total;
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
    SELECT category, COALESCE(SUM(amount), 0) AS total
    FROM expenses
    WHERE user_id = user_id_param
    GROUP BY category
    ORDER BY total DESC;  
END;
$$ LANGUAGE plpgsql;



-- psql -U your_username -d db_name -a -f backend/db/functions.sql
