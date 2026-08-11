
from app.database.sql_guard import validate_sql

queries = [
    "SELECT * FROM employees;",
    "select first_name from employees;",
    "DROP TABLE employees;",
    "DELETE FROM employees;",
    "UPDATE employees SET salary=0;",
    "INSERT INTO employees VALUES (...);",
]

for query in queries:
    print(query)
    print("VALID:", validate_sql(query))
    print("-" * 40)
    