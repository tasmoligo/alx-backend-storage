-- creates a trigger that resets the attribute valid_email
-- only when the email has been changed.
CREATE TRIGGER valid_email
AFTER UPDATE ON users
FOR EACH ROW
BEGIN
	IF OLD.email <> NEW.email THEN
		UPDATE users
		SET valid_email = 0
		WHERE id = NEW.id;
	END IF;
END;
