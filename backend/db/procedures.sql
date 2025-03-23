-- Monthly savings calculation
CREATE OR REPLACE PROCEDURE update_savings(user_id INT)
LANGUAGE PLPGSQL AS $$
DECLARE
    total_income DECIMAL(10,2);
    total_expenses DECIMAL(10,2);
BEGIN
    SELECT COALESCE(SUM(amount), 0) INTO total_income
    FROM income
    WHERE user_id = update_savings.user_id
    AND date >= date_trunc('month', CURRENT_DATE);

    SELECT COALESCE(SUM(amount), 0) INTO total_expenses
    FROM expenses
    WHERE user_id = update_savings.user_id
    AND date >= date_trunc('month', CURRENT_DATE);

    UPDATE savings_goals
    SET current_amount = current_amount + (total_income - total_expenses)
    WHERE user_id = update_savings.user_id;
END;
$$;

-- Run in command line to apply to db
--psql -U your_username -d db_name -a -f backend/db/procedures.sql