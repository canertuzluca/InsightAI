
-- ============================================================
-- InsightAI - PostgreSQL Database Schema
-- ============================================================

-- ============================================================
-- 1. DEPARTMENTS
-- ============================================================

CREATE TABLE departments (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE
);


-- ============================================================
-- 2. EMPLOYEES
-- ============================================================

CREATE TABLE employees (
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    department_id INTEGER NOT NULL,

    hire_date DATE NOT NULL,
    salary NUMERIC(12, 2) NOT NULL,

    CONSTRAINT fk_employee_department
        FOREIGN KEY (department_id)
        REFERENCES departments(id)
);


-- ============================================================
-- 3. LEAVE RECORDS
-- ============================================================

CREATE TABLE leave_records (
    id SERIAL PRIMARY KEY,
    employee_id INTEGER NOT NULL,

    leave_type VARCHAR(50) NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    days INTEGER NOT NULL,

    CONSTRAINT fk_leave_employee
        FOREIGN KEY (employee_id)
        REFERENCES employees(id)
);


-- ============================================================
-- 4. EXPENSES
-- ============================================================

CREATE TABLE expenses (
    id SERIAL PRIMARY KEY,

    department_id INTEGER NOT NULL,

    expense_date DATE NOT NULL,
    category VARCHAR(100) NOT NULL,
    amount NUMERIC(12, 2) NOT NULL,
    description TEXT,

    CONSTRAINT fk_expense_department
        FOREIGN KEY (department_id)
        REFERENCES departments(id)
);


-- ============================================================
-- 5. MACHINES
-- ============================================================

CREATE TABLE machines (
    id SERIAL PRIMARY KEY,

    name VARCHAR(100) NOT NULL,
    brand VARCHAR(100) NOT NULL,
    model VARCHAR(100),
    department_id INTEGER NOT NULL,

    CONSTRAINT fk_machine_department
        FOREIGN KEY (department_id)
        REFERENCES departments(id)
);


-- ============================================================
-- 6. PRODUCTION RECORDS
-- ============================================================

CREATE TABLE production_records (
    id SERIAL PRIMARY KEY,

    machine_id INTEGER NOT NULL,

    production_date DATE NOT NULL,
    quantity_produced INTEGER NOT NULL,
    defective_quantity INTEGER NOT NULL,

    CONSTRAINT fk_production_machine
        FOREIGN KEY (machine_id)
        REFERENCES machines(id)
);


-- ============================================================
-- 7. PRODUCTS
-- ============================================================

CREATE TABLE products (
    id SERIAL PRIMARY KEY,

    name VARCHAR(150) NOT NULL,
    category VARCHAR(100),
    unit_price NUMERIC(12, 2) NOT NULL
);


-- ============================================================
-- 8. SALES
-- ============================================================

CREATE TABLE sales (
    id SERIAL PRIMARY KEY,

    product_id INTEGER NOT NULL,
    employee_id INTEGER,

    sale_date DATE NOT NULL,
    quantity INTEGER NOT NULL,
    total_amount NUMERIC(12, 2) NOT NULL,

    CONSTRAINT fk_sale_product
        FOREIGN KEY (product_id)
        REFERENCES products(id),

    CONSTRAINT fk_sale_employee
        FOREIGN KEY (employee_id)
        REFERENCES employees(id)
);
