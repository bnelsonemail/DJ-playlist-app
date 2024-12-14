### Conceptual Exercise

Answer the following questions below:

- **QUESTION** What is PostgreSQL?
- **PostgreSQL, or Postgres, is a powerful, open-source relational database management system (RDBMS) known for its robustness, extensibility, and compliance with SQL standards. It is widely used in web applications, data warehousing, and analytics due to its rich feature set and reliability.  Postgres is open source and free.  Postgres adheres closely to SQL standards and supports advanced SQL features.  Postgres supports authentication mechanisms (e.g., SSL, Kerberos, SCRAM) and offers granular access control.  Postgres enforces data integrity with primary/foreign keys, unique constraints, and other checks.**






- **QUESTION:** What is the difference between SQL and PostgreSQL?
- **The difference between SQL and PostgreSQL lies in their definitions and roles in database management:**
## SQL (Structured Query Language)  
- **Definition: SQL is a standard programming language used for managing and interacting with relational databases. It allows you to create, read, update, and delete data in a database.**
### Purpose: 
- **Provides a way to communicate with and manipulate relational database systems.**
### Scope:
- **SQL is a language, not a database.**
- **It is supported by nearly all relational database management systems (RDBMS), including PostgreSQL, MySQL, SQL Server, and Oracle.**
### Standards: 
- **SQL has an ANSI/ISO standard that defines core syntax and functionality. However, different database systems extend it with proprietary features.**

## PostgreSQL
### Definition: 
- **PostgreSQL is an open-source relational database management system (RDBMS) that uses SQL as its query language.**
### Purpose: 
- **Acts as a database system where you store, organize, and manage your data.**
### Scope:
- **PostgreSQL implements the SQL standard and extends it with advanced features like custom data types, JSON support, and user-defined functions.**
- **It is a software system that provides tools for creating databases, executing SQL commands, and ensuring data integrity.**
### Features Beyond SQL:
- **Advanced indexing methods (e.g., GiST, GIN).**
- **Support for geospatial data with PostGIS.**
- **Extensibility through plugins and custom scripts.**
- **JSON/JSONB support for semi-structured data.**
- **Concurrency management with Multi-Version Concurrency Control (MVCC).**

- In `psql`, how do you connect to a database?
### Connection to psql:
- **Syntax: psql -d database_name, where -d is the flag used to specify the name of the database to connect to.**






- **QUESTION:** What is the difference between `HAVING` and `WHERE`?
## WHERE Clause
- **Purpose: Filters rows before any grouping or aggregation occurs.**
- **Scope: Operates on individual rows in the dataset.**
- **Usage: Used to filter rows based on column values or expressions that do not involve aggregate functions.**

## HAVING Clause
- **Purpose: Filters groups of rows after grouping or aggregation occurs.**
- **Scope: Operates on aggregated data (e.g., results of SUM, AVG, etc.).**
- **Usage: Used with aggregate functions to filter grouped results.**

## Summary
- **Use WHERE to filter individual rows before grouping.**
- **Use HAVING to filter groups or aggregate results after grouping.**




- **QUESTION:** What is the difference between an `INNER` and `OUTER` join?
## INNER JOIN
- **Definition: Returns only the rows where there is a match in both tables.**
- **Behavior:**
    - **Rows from the two tables are combined only if the join condition is met.**
    - **Unmatched rows are excluded from the result.**
- **Use Case: When you want to retrieve only matching data between two tables.**

## OUTER JOIN
Definition: Returns all rows from one or both tables, including unmatched rows.
Types:
  ### LEFT OUTER JOIN:
      Returns all rows from the left table, and matching rows from the right table.
      If there's no match, columns from the right table are filled with NULL.
  ### RIGHT OUTER JOIN:
      Returns all rows from the right table, and matching rows from the left table.
      If there's no match, columns from the left table are filled with NULL.
  ### FULL OUTER JOIN:
      Returns all rows from both tables, with unmatched rows in either table filled with NULL.




- **QUESTION:** What is the difference between a `LEFT OUTER` and `RIGHT OUTER` join?
### See Above





- **QUESTION:** What is an ORM? What do they do?
### ORM (Object-Relational Mapping)
- **An ORM (Object-Relational Mapping) is a programming technique used to interact with a relational database by abstracting database operations into objects and methods within a programming language. It provides a way to map tables in a database to classes in a programming language, allowing developers to work with database records as objects rather than writing raw SQL queries.**

### Purpose
#### Maps Database Tables to Classes:
- Each table in the database corresponds to a class in the programming language.
- Each row in a table is represented as an object, and each column is an attribute of that object.
#### Simplifies Database Operations:
- Provides methods to perform CRUD operations (Create, Read, Update, Delete) without writing raw SQL.
- Examples:
    - Fetching rows → Model.query.all()
    - Updating a row → object.update_attribute(value)

#### Handles Relationships:
- Automatically manages relationships like one-to-many, many-to-one, and many-to-many between tables (e.g., foreign keys).
- Relationships can be accessed as attributes of the objects.

#### Abstracts SQL Queries:
- Developers interact with high-level Python, Ruby, or Java code instead of raw SQL.
- The ORM translates this code into optimized SQL queries.

#### Database Portability:
- Allows the application to be database-agnostic (e.g., switching from PostgreSQL to MySQL requires minimal changes).

#### Manages Schema and Migrations:
- Some ORMs support schema definition and automatic migration to update database structure as the code evolves.





- **QUESTION:** What are some differences between making HTTP requests using AJAX 
  and from the server side using a library like `requests`?
### 1. Environment
- AJAX: Runs in the browser (client-side).
- Server-Side: Runs on the server (e.g., Python requests).
### 2. Use Case
- AJAX: Updates the webpage dynamically (e.g., search suggestions).
- Server-Side: Fetches and processes data before sending it to the client (e.g., API integration).
### 3. Restrictions
- AJAX: Limited by CORS rules.
- Server-Side: No CORS restrictions; can access any reachable resource.
### 4. Security
- AJAX: Exposes requests to the browser; avoid sending sensitive data (e.g., API keys).
- Server-Side: Safely handles sensitive information.
### 5. Performance
- AJAX: Puts load on the client.
- Server-Side: Centralizes processing on the server.
### 6. Execution
- AJAX: Runs after the page loads in response to user actions.
- Server-Side: Executes during backend operations (e.g., page rendering, background tasks).
### 7. Complexity
- AJAX: Uses browser APIs (e.g., fetch) or libraries like Axios.
- Server-Side: Simplified with libraries like Python's requests.
### 8. Result Handling
- AJAX: Updates the DOM dynamically.
- Server-Side: Returns preprocessed data to the client.






- **QUESTION:** What is CSRF? What is the purpose of the CSRF token?
### CSRF (Cross-Site Request Forgery)
- CSRF (Cross-Site Request Forgery) is an attack where a malicious user tricks a victim into performing unwanted actions on a web application where they are authenticated.
- It occurs when an attacker uses the identity and privileges of an authenticated user to send unauthorized requests to a web application.
### Purpose of the CSRF Token
- **Prevent CSRF Attacks:** A CSRF token is a unique, secret value generated by the server and included in forms or requests. This token helps ensure that the request originated from the intended user and not from a malicious source.
- **How it Works:** The token is included in every form or request sent to the server. When the server receives the request, it verifies that the token is valid and matches the one stored for the authenticated session. If it doesn’t match, the request is rejected, protecting against CSRF.
### Summary
- **CSRF:** Attacks users by tricking them into making unauthorized requests.
- **CSRF Token:** A unique token that helps the server verify that the request is legitimate and not forged.






- **QUESTION:** What is the purpose of `form.hidden_tag()`?
### Purpose
- The purpose of form.hidden_tag() in Flask-WTF (a Flask extension for working with forms) is to render all hidden fields in a form, including the CSRF token, in a single call.
### Primary Use
- **CSRF Protection:** Automatically includes the hidden input field for the CSRF token in your form. This ensures that the CSRF token generated by Flask-WTF is sent with the form submission and validated on the server side.
### Why Use form.hidden_tag()?
#### 1. Convenience:
- Instead of manually adding the CSRF token field in your form template, form.hidden_tag() handles it automatically.
#### 2. Safety:
- Ensures the CSRF token is included in all forms, providing protection against CSRF attacks.
#### 3. Cleaner Code:
- Handles rendering of all hidden fields in one place, keeping the form templates tidy.
