
from faker import Faker
from datetime import date, timedelta
import random

from sqlalchemy import create_engine, text


# ============================================================
# CONFIGURATION
# ============================================================

DATABASE_URL = (
    "postgresql+psycopg2://postgres:postgres@localhost:5432/insight_ai"
)

fake = Faker()
Faker.seed(42)
random.seed(42)

engine = create_engine(DATABASE_URL)


# ============================================================
# CONSTANTS
# ============================================================

DEPARTMENTS = [
    "Finance",
    "Marketing",
    "Production",
    "Sales",
    "IT",
]

LEAVE_TYPES = [
    "annual",
    "sick",
    "personal",
]

EXPENSE_CATEGORIES = [
    "software",
    "advertising",
    "equipment",
    "travel",
    "office",
    "consulting",
]

MACHINE_BRANDS = [
    "Siemens",
    "Bosch",
    "Fanuc",
]

PRODUCT_CATEGORIES = [
    "Electronics",
    "Industrial",
    "Components",
    "Accessories",
]


# ============================================================
# DATA DATE RANGE
# ============================================================

DATA_START_DATE = date(2024, 1, 1)
DATA_END_DATE = date(2026, 7, 30)


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def random_date(start_date, end_date):
    """
    Generate a random date between start_date and end_date.
    Both dates are inclusive.
    """

    delta = end_date - start_date
    random_days = random.randint(0, delta.days)

    return start_date + timedelta(days=random_days)


# ============================================================
# MAIN SEED FUNCTION
# ============================================================

def generate_data():

    print("InsightAI - Synthetic Data Generator")
    print("------------------------------------")

    with engine.begin() as connection:

        # ----------------------------------------------------
        # 1. CLEAN EXISTING DATA
        # ----------------------------------------------------

        print("\nCleaning existing data...")

        connection.execute(
            text(
                """
                TRUNCATE TABLE
                    sales,
                    products,
                    production_records,
                    machines,
                    expenses,
                    leave_records,
                    employees,
                    departments
                RESTART IDENTITY CASCADE;
                """
            )
        )

        print("Existing data cleaned.")

        # ----------------------------------------------------
        # 2. DEPARTMENTS
        # ----------------------------------------------------

        print("\nCreating departments...")

        department_ids = {}

        for department_name in DEPARTMENTS:

            result = connection.execute(
                text(
                    """
                    INSERT INTO departments (name)
                    VALUES (:name)
                    RETURNING id;
                    """
                ),
                {"name": department_name},
            )

            department_id = result.scalar_one()

            department_ids[department_name] = department_id

        print(f"Created {len(department_ids)} departments.")

        # ----------------------------------------------------
        # 3. EMPLOYEES
        # ----------------------------------------------------

        print("\nCreating employees...")

        employee_ids = []

        employee_count = 50

        # ----------------------------------------------------
        # 3A. GUARANTEED DEMO EMPLOYEE
        # ----------------------------------------------------

        result = connection.execute(
            text(
                """
                INSERT INTO employees
                (
                    first_name,
                    last_name,
                    department_id,
                    hire_date,
                    salary
                )
                VALUES
                (
                    :first_name,
                    :last_name,
                    :department_id,
                    :hire_date,
                    :salary
                )
                RETURNING id;
                """
            ),
            {
                "first_name": "Caner",
                "last_name": "Tuzluca",
                "department_id": department_ids["IT"],
                "hire_date": date(2023, 6, 1),
                "salary": 85000.00,
            },
        )

        employee_ids.append(
            {
                "id": result.scalar_one(),
                "department_id": department_ids["IT"],
                "first_name": "Caner",
                "last_name": "Tuzluca",
            }
        )

        # ----------------------------------------------------
        # 3B. RANDOM EMPLOYEES
        # ----------------------------------------------------

        for _ in range(employee_count - 1):

            department_name = random.choice(DEPARTMENTS)
            department_id = department_ids[department_name]

            first_name = fake.first_name()
            last_name = fake.last_name()

            hire_date = random_date(
                date(2018, 1, 1),
                DATA_END_DATE,
            )

            salary = round(
                random.uniform(30000, 120000),
                2,
            )

            result = connection.execute(
                text(
                    """
                    INSERT INTO employees
                    (
                        first_name,
                        last_name,
                        department_id,
                        hire_date,
                        salary
                    )
                    VALUES
                    (
                        :first_name,
                        :last_name,
                        :department_id,
                        :hire_date,
                        :salary
                    )
                    RETURNING id;
                    """
                ),
                {
                    "first_name": first_name,
                    "last_name": last_name,
                    "department_id": department_id,
                    "hire_date": hire_date,
                    "salary": salary,
                },
            )

            employee_ids.append(
                {
                    "id": result.scalar_one(),
                    "department_id": department_id,
                    "first_name": first_name,
                    "last_name": last_name,
                }
            )

        print(f"Created {employee_count} employees.")

        # ----------------------------------------------------
        # 4. LEAVE RECORDS
        # ----------------------------------------------------

        print("\nCreating leave records...")

        leave_count = 200

        # ----------------------------------------------------
        # 4A. GUARANTEED CANER LEAVE RECORDS
        # ----------------------------------------------------

        caner_employee = employee_ids[0]

        caner_leaves = [
            {
                "leave_type": "annual",
                "start_date": date(2026, 1, 12),
                "end_date": date(2026, 1, 16),
                "days": 5,
            },
            {
                "leave_type": "annual",
                "start_date": date(2026, 4, 6),
                "end_date": date(2026, 4, 10),
                "days": 5,
            },
            {
                "leave_type": "personal",
                "start_date": date(2026, 6, 15),
                "end_date": date(2026, 6, 16),
                "days": 2,
            },
            {
                "leave_type": "sick",
                "start_date": date(2026, 7, 6),
                "end_date": date(2026, 7, 7),
                "days": 2,
            },
        ]

        for leave in caner_leaves:

            connection.execute(
                text(
                    """
                    INSERT INTO leave_records
                    (
                        employee_id,
                        leave_type,
                        start_date,
                        end_date,
                        days
                    )
                    VALUES
                    (
                        :employee_id,
                        :leave_type,
                        :start_date,
                        :end_date,
                        :days
                    );
                    """
                ),
                {
                    "employee_id": caner_employee["id"],
                    **leave,
                },
            )

        # ----------------------------------------------------
        # 4B. RANDOM LEAVE RECORDS
        # ----------------------------------------------------

        for _ in range(leave_count - len(caner_leaves)):

            employee = random.choice(employee_ids)

            start_date = random_date(
                DATA_START_DATE,
                DATA_END_DATE,
            )

            days = random.randint(1, 10)

            end_date = start_date + timedelta(days=days - 1)

            # Do not allow leave records to extend beyond
            # the current project data date.
            if end_date > DATA_END_DATE:
                end_date = DATA_END_DATE
                days = (end_date - start_date).days + 1

            connection.execute(
                text(
                    """
                    INSERT INTO leave_records
                    (
                        employee_id,
                        leave_type,
                        start_date,
                        end_date,
                        days
                    )
                    VALUES
                    (
                        :employee_id,
                        :leave_type,
                        :start_date,
                        :end_date,
                        :days
                    );
                    """
                ),
                {
                    "employee_id": employee["id"],
                    "leave_type": random.choice(LEAVE_TYPES),
                    "start_date": start_date,
                    "end_date": end_date,
                    "days": days,
                },
            )

        print(f"Created {leave_count} leave records.")

        # ----------------------------------------------------
        # 5. EXPENSES
        # ----------------------------------------------------

        print("\nCreating expenses...")

        expense_count = 300

        for _ in range(expense_count):

            department_name = random.choice(DEPARTMENTS)

            department_id = department_ids[department_name]

            expense_date = random_date(
                DATA_START_DATE,
                DATA_END_DATE,
            )

            amount = round(
                random.uniform(100, 50000),
                2,
            )

            connection.execute(
                text(
                    """
                    INSERT INTO expenses
                    (
                        department_id,
                        expense_date,
                        category,
                        amount,
                        description
                    )
                    VALUES
                    (
                        :department_id,
                        :expense_date,
                        :category,
                        :amount,
                        :description
                    );
                    """
                ),
                {
                    "department_id": department_id,
                    "expense_date": expense_date,
                    "category": random.choice(EXPENSE_CATEGORIES),
                    "amount": amount,
                    "description": fake.sentence(),
                },
            )

        print(f"Created {expense_count} expenses.")

        # ----------------------------------------------------
        # 6. MACHINES
        # ----------------------------------------------------

        print("\nCreating machines...")

        machine_ids = []

        for machine_number in range(1, 4):

            brand = MACHINE_BRANDS[machine_number - 1]

            result = connection.execute(
                text(
                    """
                    INSERT INTO machines
                    (
                        name,
                        brand,
                        model,
                        department_id
                    )
                    VALUES
                    (
                        :name,
                        :brand,
                        :model,
                        :department_id
                    )
                    RETURNING id;
                    """
                ),
                {
                    "name": f"Machine {machine_number}",
                    "brand": brand,
                    "model": f"{brand}-M{random.randint(100, 999)}",
                    "department_id": department_ids["Production"],
                },
            )

            machine_ids.append(result.scalar_one())

        print("Created 3 production machines.")

        # ----------------------------------------------------
        # 7. PRODUCTION RECORDS
        # ----------------------------------------------------

        print("\nCreating production records...")

        production_count = 500

        for _ in range(production_count):

            machine_id = random.choice(machine_ids)

            production_date = random_date(
                DATA_START_DATE,
                DATA_END_DATE,
            )

            quantity_produced = random.randint(
                500,
                5000,
            )

            defective_quantity = random.randint(
                0,
                int(quantity_produced * 0.10),
            )

            connection.execute(
                text(
                    """
                    INSERT INTO production_records
                    (
                        machine_id,
                        production_date,
                        quantity_produced,
                        defective_quantity
                    )
                    VALUES
                    (
                        :machine_id,
                        :production_date,
                        :quantity_produced,
                        :defective_quantity
                    );
                    """
                ),
                {
                    "machine_id": machine_id,
                    "production_date": production_date,
                    "quantity_produced": quantity_produced,
                    "defective_quantity": defective_quantity,
                },
            )

        print(
            f"Created {production_count} production records."
        )

        # ----------------------------------------------------
        # 8. PRODUCTS
        # ----------------------------------------------------

        print("\nCreating products...")

        product_ids = []

        product_count = 20

        for _ in range(product_count):

            result = connection.execute(
                text(
                    """
                    INSERT INTO products
                    (
                        name,
                        category,
                        unit_price
                    )
                    VALUES
                    (
                        :name,
                        :category,
                        :unit_price
                    )
                    RETURNING id;
                    """
                ),
                {
                    "name": fake.catch_phrase(),
                    "category": random.choice(
                        PRODUCT_CATEGORIES
                    ),
                    "unit_price": round(
                        random.uniform(50, 5000),
                        2,
                    ),
                },
            )

            product_ids.append(result.scalar_one())

        print(f"Created {product_count} products.")

        # ----------------------------------------------------
        # 9. SALES
        # ----------------------------------------------------

        print("\nCreating sales...")

        sales_count = 400

        for _ in range(sales_count):

            product_id = random.choice(product_ids)

            employee = random.choice(employee_ids)

            quantity = random.randint(1, 50)

            # Retrieve product price
            result = connection.execute(
                text(
                    """
                    SELECT unit_price
                    FROM products
                    WHERE id = :product_id;
                    """
                ),
                {"product_id": product_id},
            )

            unit_price = result.scalar_one()

            total_amount = round(
                float(unit_price) * quantity,
                2,
            )

            sale_date = random_date(
                DATA_START_DATE,
                DATA_END_DATE,
            )

            connection.execute(
                text(
                    """
                    INSERT INTO sales
                    (
                        product_id,
                        employee_id,
                        sale_date,
                        quantity,
                        total_amount
                    )
                    VALUES
                    (
                        :product_id,
                        :employee_id,
                        :sale_date,
                        :quantity,
                        :total_amount
                    );
                    """
                ),
                {
                    "product_id": product_id,
                    "employee_id": employee["id"],
                    "sale_date": sale_date,
                    "quantity": quantity,
                    "total_amount": total_amount,
                },
            )

        print(f"Created {sales_count} sales.")

    # ========================================================
    # COMPLETED
    # ========================================================

    print("\n------------------------------------")
    print("Synthetic data generation completed!")
    print("------------------------------------")


if __name__ == "__main__":
    generate_data()

    