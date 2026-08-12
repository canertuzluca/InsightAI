
# Analytics Tool


from app.database.query_executor import execute_query
from app.models.tool_result import ToolResult

import pandas as pd


def analytics_tool(
    question: str,
    context: dict | None = None
) -> ToolResult:
    """
    Performs deterministic sales analytics using PostgreSQL and Pandas.

    If department information is available in context,
    analytics are performed only for that department.

    If the question explicitly requires a department-specific
    analysis but the department context is missing, the tool
    refuses to analyze all-company data.
    """

    try:
        context = context or {}

        sql_result = context.get("sql_result")

        department = None

        # --------------------------------------------------
        # Extract department from SQL result
        # --------------------------------------------------

        if sql_result:
            if isinstance(sql_result, list) and len(sql_result) > 0:

                first_row = sql_result[0]

                if isinstance(first_row, dict):

                    # Ignore INSUFFICIENT_DATA
                    if "?" not in first_row or first_row.get("?column?") != "INSUFFICIENT_DATA":

                        department = (
                            first_row.get("department_name")
                            or first_row.get("name")
                        )

        question_lower = question.lower()

        # --------------------------------------------------
        # Detect department-specific questions
        # --------------------------------------------------

        department_keywords = [
            "departman",
            "departmanının",
            "departmanındaki",
            "department",
        ]

        department_specific = any(
            keyword in question_lower
            for keyword in department_keywords
        )

        # --------------------------------------------------
        # Prevent accidental all-company analytics
        # --------------------------------------------------

        if department_specific and not department:

            return ToolResult(
                tool="ANALYTICS",
                success=False,
                result=None,
                error=(
                    "Departman bilgisi bulunamadığı için "
                    "departman bazlı analiz gerçekleştirilemedi."
                ),
                metadata={
                    "department": None,
                    "requires_department": True,
                }
            )

        # --------------------------------------------------
        # Department-specific query
        # --------------------------------------------------

        if department:

            query = """
            SELECT
                s.sale_date,
                s.quantity,
                s.total_amount
            FROM sales s
            JOIN employees e
                ON s.employee_id = e.id
            JOIN departments d
                ON e.department_id = d.id
            WHERE d.name = :department
            ORDER BY s.sale_date;
            """

            rows = execute_query(
                query,
                {
                    "department": department
                }
            )

        # --------------------------------------------------
        # General company-wide analytics
        # --------------------------------------------------

        else:

            query = """
            SELECT
                sale_date,
                quantity,
                total_amount
            FROM sales
            ORDER BY sale_date;
            """

            rows = execute_query(query)

        # --------------------------------------------------
        # No sales data
        # --------------------------------------------------

        if not rows:

            return ToolResult(
                tool="ANALYTICS",
                success=False,
                result=None,
                error="Analiz yapılacak satış verisi bulunamadı.",
                metadata={
                    "department": department
                }
            )

        # --------------------------------------------------
        # DataFrame
        # --------------------------------------------------

        df = pd.DataFrame(rows)

        df["sale_date"] = pd.to_datetime(
            df["sale_date"]
        )

        # --------------------------------------------------
        # Last 6 months
        # --------------------------------------------------

        if "6 ay" in question_lower:

            max_date = df["sale_date"].max()

            start_date = (
                max_date -
                pd.DateOffset(months=6)
            )

            df = df[
                (df["sale_date"] > start_date)
                &
                (df["sale_date"] <= max_date)
            ]

        # --------------------------------------------------
        # Empty result after filtering
        # --------------------------------------------------

        if df.empty:

            return ToolResult(
                tool="ANALYTICS",
                success=False,
                result=None,
                error="Belirtilen dönem için satış verisi bulunamadı.",
                metadata={
                    "department": department
                }
            )

        # --------------------------------------------------
        # Basic statistics
        # --------------------------------------------------

        total_sales = len(df)

        total_revenue = (
            df["total_amount"].sum()
        )

        total_quantity = (
            df["quantity"].sum()
        )

        average_sale = (
            df["total_amount"].mean()
        )

        # --------------------------------------------------
        # Monthly sales
        # --------------------------------------------------

        monthly_sales = (
            df
            .set_index("sale_date")
            .resample("ME")["total_amount"]
            .sum()
        )

        highest_month = (
            monthly_sales.idxmax()
        )

        highest_value = (
            monthly_sales.max()
        )

        lowest_month = (
            monthly_sales.idxmin()
        )

        lowest_value = (
            monthly_sales.min()
        )

        # --------------------------------------------------
        # Growth
        # --------------------------------------------------

        first_month_value = (
            monthly_sales.iloc[0]
        )

        last_month_value = (
            monthly_sales.iloc[-1]
        )

        if first_month_value != 0:

            growth_percentage = (
                (
                    last_month_value -
                    first_month_value
                )
                /
                first_month_value
            ) * 100

        else:

            growth_percentage = None

        # --------------------------------------------------
        # Result
        # --------------------------------------------------

        result = {

            "department": department,

            "total_sales": total_sales,

            "total_revenue": round(
                float(total_revenue),
                2
            ),

            "total_quantity": int(
                total_quantity
            ),

            "average_sale": round(
                float(average_sale),
                2
            ),

            "highest_month": str(
                highest_month.date()
            ),

            "highest_month_revenue": round(
                float(highest_value),
                2
            ),

            "lowest_month": str(
                lowest_month.date()
            ),

            "lowest_month_revenue": round(
                float(lowest_value),
                2
            ),

            "growth_percentage": (
                round(
                    float(growth_percentage),
                    2
                )
                if growth_percentage is not None
                else None
            ),

            "monthly_sales": {
                str(date.date()): round(
                    float(value),
                    2
                )
                for date, value
                in monthly_sales.items()
            }
        }

        return ToolResult(
            tool="ANALYTICS",
            success=True,
            result=result,
            metadata={
                "department": department
            }
        )

    except Exception as e:

        return ToolResult(
            tool="ANALYTICS",
            success=False,
            result=None,
            error=str(e),
            metadata={
                "department": department
            }
        )
    
