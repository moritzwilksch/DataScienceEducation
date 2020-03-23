# Parts of SQL
## DDL
- CREATE, ALTER, DROP, RENAME, TRUNCATE
## DML
- SELECT ... FROM ...
- INSERT INTO ... VALUES
- UPDATE ... SET ... WHERE ...
## DCL
`GRANT [right] ON [table] TO user@host`
### Types of Rights
- Rights to (C)reate
    - `CREATE`
- Rights to (R)ead
    - `SELECT`
- Rights to (U)pdate
    - `ALTER`
    - `INSERT`
- Rights to (D)elete
    - `TRUNCATE`
    - `DROP`
## TCL
`COMMIT;` and `ROLLBACK;`
```SQL
# View Table
SELECT 
    *
FROM
    departments_dup;

# Commit current state
COMMIT;

# BROKEN Update - Overwrites everything
UPDATE departments_dup 
SET 
    dept_no = 'd011',
    dept_name = 'Quality Controll';

SELECT 
    *
FROM
    departments_dup;
    
ROLLBACK;
```

# Keys
- Primary Keys: Only one PK per table
- Unique Keys (like phone number)
    - Can be missing, can be multiple columns
    - are just used to specify that there mustn't be dupicate data in a field

# Data Types
- `CHAR(n)` always takes up n Bytes of storage
    - maximum n = 255
    - _**is 50% faster than VARCHAR!**_
- `VARCHAR(maxN)` only takes as much space as there are chars in a specific string
    - maximum maxN = 65,535
- `ENUM('A', 'B', 'C', ...)`
- `INT`
    - TINYINT (1 Byte)
    - SMALLINT (2 Bytes)
    - MEDIUMINT (3 Bytes)
    - INT (4 Bytes)
    - BIGINT (8 Bytes)
    - => Unsigned VS Signed
- `DECIMAL(precision, scale)` <=> `NUMERIC`
    - **FIXED POINT**: Fill with 0 or round (+ warning) to fit the size (precision, scale)
    - precision = total number of digits
    - scale = digits *after the decimal point*
- `FLOAT` and `DOUBLE`
    - Used for approximate values only!
    - Rounds **without warning**
    - FLOAT -> 4 Bytes (23 digits max)
    - DOUBLE -> 8 Bytes (53 digits max)
- OTHER Datatypes
    - DATE (YYYY-MM-DD)
    - DATETIME (YYYY-MM-DD HH:MM:SS[.fraction])
    - TIMESTAMP (POSIX Timestamp)
    - BLOB (Binary Large Object)

# Code
```SQL
-- Set up database and select it for use
CREATE DATABASE IF NOT EXISTS Sales;
USE Sales;

-- Create a table
CREATE TABLE sales
(
    purchase_number INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    date_of_purchase DATE NOT NULL,
    customer_id INT, 
    item_code VARCHAR(10) NOT NULL
);

-- Drop the table
DROP TABLE sales;
```
- instead of `USE Sales;` using Sales.sales is also possible to refer to the sales table

Alternatively: 
```SQL
CREATE TABLE sales
(
    purchase_number INT AUTO_INCREMENT,
    date_of_purchase DATE,
    customer_id INT, 
    item_code VARCHAR(10),
    PRIMARY KEY (purchase_number)
);
```

Additional Tables:
```SQL
CREATE TABLE customers (
    customer_id INT,
    first_name VARCHAR(255),
    last_name VARCHAR(255),
    email_address VARCHAR(255),
    number_of_complaints INT,
    PRIMARY KEY (customer_id)
);

 

CREATE TABLE items (
    item_id VARCHAR(255),
    item VARCHAR(255),
    unit_price NUMERIC(10 , 2 ),
    company_id VARCHAR(255),
    PRIMARY KEY (item_id)
);

CREATE TABLE companies (
    company_id VARCHAR(255),
    company_name VARCHAR(255),
    headquarters_phone_number INT,
    PRIMARY KEY (company_id)
);
```

## Foreign Key Constraints after Table Creation
```SQL
ALTER TABLE sales
ADD FOREIGN KEY (customer_id) REFERENCES customers(customer_id) ON DELETE CASCADE;

-- Dropping FK Constraint

ALTER TABLE sales
DROP FOREIGN KEY sales_ibfk_2
```

## Adding Gender ENUM after Table Creation
```SQL
ALTER TABLE customers
ADD COLUMN gender ENUM('M', 'F') AFTER last_name;
```

## Adding & Dropping Unique Key Constraint
```SQL
CREATE TABLE customers (
    customer_id INT AUTO_INCREMENT,
    first_name VARCHAR(255),
    last_name VARCHAR(255),
    email_address VARCHAR(255),
    number_of_complaints INT,
    PRIMARY KEY (customer_id),
    UNIQUE KEY (email_address)
);

-- OR:

ALTER TABLE customers
ADD UNIQUE KEY (email_address)

-- Dropping the Unique Key Constraint
ALTER TABLE customers
DROP INDEX email_address;
```

## Unique Keys
- Have the same role as *indexes* (reverse is NOT true)
- Indexes help retrieve data more easily
- Indexes are unique columns that are frequently used to retrieve information

## Default Values
```SQL
ALTER TABLE customers
CHANGE COLUMN number_of_complaints number_of_complaints INT DEFAULT 0;

-- Dropping Default Constraint
ALTER TABLE customers
ALTER COLUMN number_of_complaints DROP DEFAULT;
```

## NOT NULL Constraint
```SQL
-- Specific Syntax to remove NOT NULL
ALTER TABLE companies
MODIFY company_name VARCHAR(255) NULL;
```
=> MODIFY COLUMN does everything CHANGE COLUMN can, but without renaming the column!
## Missing Values
- = `NULL``
- 0 or None are user specified values
    - e.g.: "Rate the app" dialogue -> "No thanks" = None whereas "Not clicked anything" -> NULL

## Logical Operator prescedence
- **AND > OR**

## HAVING vs. WHERE
- HAVING is applied to the results of a GROUP BY
- HAVING cannot take mixed (i.e. aggregated an non-aggregated) conditions

## Deleting Rows
```SQL
DELETE FROM employees 
WHERE
    emp_no = 999903;
```

## Replacing NULL Values in Output
```SQL
SELECT 
    dept_no, IFNULL(dept_name, "### not provided ###")
FROM
    departments_dup;
```
### COALESCE
- Returns *first non-NULL value* from provided set
```SQL
SELECT 
    dept_no,
    dept_name,
    COALESCE(dept_manager, dept_name, '#NA#') AS 'Manger'
FROM
    departments_dup;
```

## Duplicate Records
- When joining, duplicates induce multiple additional output rows
- *Solution*: Group by the columns that differs most (e.g. `emp_id`) to prevent duplicates!

## Cross Join
- Is the cartesian product of tables
- combines ALL not just the matching records

## UNION ALL
- used to combine multiple SELECT Statements in a single output (i.e. unifying tables)
- *includes duplicates*
- `UNION` does not include duplicates
- both can only be used on tables with the same structure, columns and datatypes

## Subqueries
```SQL
SELECT 
    first_name, last_name
FROM
    employees
WHERE
    emp_no IN (SELECT 
            dm.emp_no
        FROM
            dept_manager dm);

-- OR USE EXISTS:

SELECT 
    e.first_name, e.last_name
FROM
    employees e
WHERE
    EXISTS( SELECT 
            m.emp_no
        FROM
            dept_manager m
        WHERE
            e.emp_no = m.emp_no);
```

- Using `EXISTS` is quicker than `IN` as EXISTS only tests row values for existence where IN searches
- **most (not all)** nested queries can be rewritten as JOINS 
- JOINS are more efficient in general 

## VIEWS
- virtual temporary data tables retrieving information from base tables
- e.g. if there are multiple entries of employees belonging to different departments, find *the lastest one* per employee
```SQL
CREATE OR REPLACE VIEW v_dep_emp_latest_date AS
    SELECT 
        emp_no, MAX(from_date) AS from_date, MAX(to_date) AS to_date
    FROM
        dept_emp
    GROUP BY emp_no;
```
=> The view acts as a shortcut for writing the whole query and occupies no space as it is executed everytime on live data

## Stored Routines
- set of SQL statements that can be stored on the database server
    - Stored procedures = procedures
    - Function = user-defined or built-in (MAX, COUNT, ...)
- in stored routines you **need a temporary line delimiter different from `;`**
- at the end of a procedure one must **reset the delimiter to the standard `;`!**

### Stored Procedures
```SQL
USE employees;
DROP PROCEDURE IF EXISTS select_employees;

DELIMITER $$
CREATE PROCEDURE select_employees()
BEGIN
	SELECT * FROM employees LIMIT 1000;
END$$
DELIMITER ;


CALL select_employees();
```

### With Input Parameters
```SQL
DELIMITER $$
CREATE PROCEDURE emp_salary(IN p_emp_no INTEGER)
BEGIN
	SELECT e.first_name, e.last_name, s.salary, s.from_date, s.to_date
    FROM employees e 
		JOIN salaries s
	ON s.emp_no = e.emp_no
	WHERE e.emp_no = p_emp_no;
END$$
DELIMITER ;

CALL emp_salary(10021);
```

### With Input and Output Parameters
```SQL
DELIMITER $$
CREATE PROCEDURE emp_avg_salary_out(IN p_emp_no INTEGER, OUT p_avg_salary DECIMAL(10,2))
BEGIN
	SELECT AVG(s.salary) INTO p_avg_salary
    FROM employees e 
		JOIN salaries s
	ON s.emp_no = e.emp_no
	WHERE e.emp_no = p_emp_no;
END$$
DELIMITER ;

-- Store it in result variable
set @result = 0;
call emp_avg_salary_out(10021, @result);
select @result;
```
## Functions
```SQL
DELIMITER $$
CREATE FUNCTION f_emp_avg_salary(p_emp_no INTEGER) RETURNS DECIMAL(10,2)
DETERMINISTIC
BEGIN
DECLARE v_avg_salary DECIMAL(10,2);

SELECT AVG(s.salary) INTO v_avg_salary
FROM salaries s
	JOIN employees e
		ON s.emp_no = e.emp_no
WHERE e.emp_no = p_emp_no;

RETURN v_avg_salary;
END$$
DELIMITER ;

SELECT F_EMP_AVG_SALARY(10021);
-- you CAN NOT call a function
```
==> Functionions SHOULD NOT be used to update or insert data as these operations return nothing
==> Functions can be used in SELECT statements, procedures CAN NOT!

## Indexes
- **Primary** and **Unique** Keys are indexes by default!

```SQL
-- Dropping the index
ALTER TABLE employees
DROP INDEX i_hire_date;

-- Creating the index
CREATE INDEX i_hire_date ON employees(hire_date);

-- Selection is sped up from 0.15s to 0.0008s
SELECT 
    *
FROM
    employees
WHERE
    hire_date > '2000-01-01';
```

## WITH for Subqueries
```SQL
-- better: use HAVING but this is just an example for WITH syntax
WITH subquery (vorname, nachname, gehalt) AS
	(SELECT e.first_name, e.last_name, AVG(s.salary)
    FROM employees e JOIN salaries s ON e.emp_no = s.emp_no
    GROUP BY e.emp_no)

SELECT vorname, nachname, gehalt FROM subquery WHERE gehalt > 100000;
```