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



-- CREATE OR REPLACE FUNCTION get_budget(user_id_param INT)
-- RETURNS TABLE(category TEXT, budget DECIMAL) AS $$
-- BEGIN
--     RETURN QUERY
--     SELECT category, budget_amount AS budget 
--     FROM budgets 
--     WHERE user_id = user_id_param;
-- END;
-- $$ LANGUAGE plpgsql;


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


-- psql -U your_username -d db_name -a -f backend/db/functions.sql
