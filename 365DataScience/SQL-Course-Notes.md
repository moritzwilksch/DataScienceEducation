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

# Keys
- Primary Keys: Only one PK per table
- Unique Keys (like phone number)
    - Can be missing, can be multiple columns
    - are just used to specify that there mustn't be dupicate data in a field