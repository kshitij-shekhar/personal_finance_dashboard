-- Expense audit trigger
CREATE TABLE IF NOT EXISTS expense_audit (
    audit_id SERIAL PRIMARY KEY,
    expense_id INT,
    old_amount DECIMAL(10,2),
    new_amount DECIMAL(10,2),
    changed_at TIMESTAMP
);

CREATE OR REPLACE FUNCTION log_expense_changes()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.amount <> OLD.amount THEN
        INSERT INTO expense_audit(expense_id, old_amount, new_amount, changed_at)
        VALUES (OLD.id, OLD.amount, NEW.amount, NOW());
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE PLPGSQL;

CREATE TRIGGER expense_update_trigger
AFTER UPDATE ON expenses
FOR EACH ROW EXECUTE PROCEDURE log_expense_changes();


CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;




--Trigger for income updates 
CREATE OR REPLACE FUNCTION update_income_summary()
RETURNS TRIGGER AS $$
BEGIN
    -- Adjust total income on INSERT or UPDATE
    -- INSERT INTO income_expense_summary (user_id, year, month, total_income)
    -- VALUES (
    --     NEW.user_id,
    --     EXTRACT(YEAR FROM NEW.date)::INT,
    --     EXTRACT(MONTH FROM NEW.date)::INT,
    --     NEW.amount
    -- )
    -- ON CONFLICT (user_id, year, month)
    -- DO UPDATE SET total_income = income_expense_summary.total_income 
    --                - COALESCE(OLD.amount, 0) + NEW.amount;

    -- Adjust total income on DELETE
    IF TG_OP = 'DELETE' THEN
        UPDATE income_expense_summary
        SET total_income = total_income - COALESCE(OLD.amount, 0)
        WHERE user_id = OLD.user_id 
        AND year = EXTRACT(YEAR FROM OLD.date)::INT 
        AND month = EXTRACT(MONTH FROM OLD.date)::INT;
    END IF;


    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_update_income_summary
AFTER INSERT OR UPDATE OR DELETE ON income
FOR EACH ROW EXECUTE FUNCTION update_income_summary();


-- Trigger for Expense Updates
CREATE OR REPLACE FUNCTION update_expense_summary()
RETURNS TRIGGER AS $$
BEGIN
    -- Adjust total expenses on INSERT or UPDATE
    -- INSERT INTO income_expense_summary (user_id, year, month, total_expenses)
    -- VALUES (
    --     NEW.user_id,
    --     EXTRACT(YEAR FROM NEW.date)::INT,
    --     EXTRACT(MONTH FROM NEW.date)::INT,
    --     NEW.amount
    -- )
    -- ON CONFLICT (user_id, year, month)
    -- DO UPDATE SET total_expenses = income_expense_summary.total_expenses 
    --                - COALESCE(OLD.amount, 0) + NEW.amount;

    -- Adjust total expenses on DELETE
    IF TG_OP = 'DELETE' THEN
        UPDATE income_expense_summary
        SET total_expenses = total_expenses - COALESCE(OLD.amount, 0)
        WHERE user_id = OLD.user_id 
        AND year = EXTRACT(YEAR FROM OLD.date)::INT 
        AND month = EXTRACT(MONTH FROM OLD.date)::INT;
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_update_expense_summary
AFTER INSERT OR UPDATE OR DELETE ON expenses
FOR EACH ROW EXECUTE FUNCTION update_expense_summary();



CREATE OR REPLACE FUNCTION prevent_negative_assets()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.value < 0 THEN
        RAISE EXCEPTION 'Asset value cannot be negative';
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER check_negative_assets
BEFORE INSERT OR UPDATE ON assets
FOR EACH ROW EXECUTE FUNCTION prevent_negative_assets();



-- run the following in the command line to apply triggers.sql to the db
-- psql -U your_username -d db_name -a -f backend/db/triggers.sql
