-- creates a table 'users' following these requirements:
--	id, integer, never null, auto increment and primary key
--	email, string (255 characters), never null and unique
--	name, string (255 characters)
CREATE TABLE IF NOT EXISTS users (
	id int NOT NULL AUTO_INCREMENT,
	email VARCHAR(255) NOT NULL,
	name VARCHAR(255),
	PRIMARY KEY (id),
	UNIQUE (email)
);
