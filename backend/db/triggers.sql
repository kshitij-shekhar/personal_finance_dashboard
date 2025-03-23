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

-- run the following in the command line to apply triggers.sql to the db
-- psql -U your_username -d db_name -a -f backend/db/triggers.sql
