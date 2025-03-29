-- Monthly savings calculation
-- CREATE OR REPLACE PROCEDURE update_savings(user_id_param INT)
-- LANGUAGE PLPGSQL AS $$
-- DECLARE
--     total_income DECIMAL(10,2);
--     total_expenses DECIMAL(10,2);
-- BEGIN
--     SELECT COALESCE(SUM(amount), 0) INTO total_income
--     FROM income
--     WHERE user_id = update_savings.user_id_param
--     AND date >= date_trunc('month', CURRENT_DATE);

--     SELECT COALESCE(SUM(amount), 0) INTO total_expenses
--     FROM expenses
--     WHERE user_id = update_savings.user_id_param
--     AND date >= date_trunc('month', CURRENT_DATE);

--     UPDATE savings_goals
--     SET current_amount = current_amount + (total_income - total_expenses)
--     WHERE user_id = update_savings.user_id_param;
-- END;
-- $$;

CREATE OR REPLACE PROCEDURE add_debt(
    p_user_id INT,
    p_category VARCHAR(50),
    p_amount NUMERIC
)
LANGUAGE plpgsql
AS $$
BEGIN
    INSERT INTO debts (user_id, category, amount) 
    VALUES (p_user_id, p_category, p_amount);
END;
$$;


CREATE OR REPLACE PROCEDURE delete_debt(
    p_debt_id INT
)
LANGUAGE plpgsql
AS $$
BEGIN
    DELETE FROM debts WHERE id = p_debt_id;
END;
$$;


CREATE OR REPLACE PROCEDURE add_asset(
    p_user_id INT,
    p_category VARCHAR(50),
    p_value NUMERIC
)
LANGUAGE plpgsql
AS $$
BEGIN
    INSERT INTO assets (user_id, category, value) 
    VALUES (p_user_id, p_category, p_value);
END;
$$;


CREATE OR REPLACE PROCEDURE delete_asset(
    p_asset_id INT
)
LANGUAGE plpgsql
AS $$
BEGIN
    DELETE FROM assets WHERE id = p_asset_id;
END;
$$;





-- Run in command line to apply to db
--psql -U your_username -d db_name -a -f backend/db/procedures.sql