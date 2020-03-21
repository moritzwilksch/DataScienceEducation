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