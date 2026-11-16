from lession_001_prompting_generate_data_set import PromptEvaluator
from lesson_001_requests import add_user_message, chat

model = "claude-haiku-4-5"

def run_prompt(prompt_inputs):
    prompt = f"""
        <sql_generation_task>
            <objective>Write a SQL extract query and production design rationale for Detail Design based on the Base Design Requirement.</objective>
            
            <inputs>
                <overview>{prompt_inputs["Overview"]}</overview>
                <table_schema>{prompt_inputs["Table Schema"]}</table_schema>
                <mapping>{prompt_inputs["Mapping"]}</mapping>
            </inputs>
                    
            <guidelines>
                <guideline id="1" name="Strict Mapping Contract (No Extra or Missing Columns)">
                Explicitly <sql_keyword>SELECT</sql_keyword> *only and exactly* the columns and attributes specified in the Mapping documentation. The Mapping serves as a strict contract: do not omit any required mapped fields, and strictly **avoid selecting unmapped columns** (e.g., audit flags, `is_active`, `created_date`, or extra table attributes not present in the mapping specification).
                </guideline>
                
                <guideline id="2" name="Precise Grouping and Aggregation">
                When the business requirement or mapping specifies aggregations (e.g., grouped by customer, payment method, etc.), the <sql_keyword>GROUP BY</sql_keyword> clause must <emphasis>only</emphasis> include those specific grouping dimensions. Non-aggregated metric or attribute columns must use appropriate aggregate functions (e.g., <sql_func>SUM</sql_func>, <sql_func>COUNT</sql_func>, <sql_func>MAX</sql_func>, <sql_func>MIN</sql_func>) rather than blindly grouping by every selected column.
                </guideline>
                
                <guideline id="3" name="Strict ORDER BY Compliance">
                The <sql_keyword>ORDER BY</sql_keyword> clause must <emphasis>strictly</emphasis> reference columns that are explicitly present in both the <sql_keyword>SELECT</sql_keyword> clause and the Mapping specification (or valid aggregate aliases). Never include unselected or unmapped columns in <sql_keyword>ORDER BY</sql_keyword> to maintain design consistency and platform compatibility.
                </guideline>

                <guideline id="4" name="Production Security and Performance Considerations">
                The response must include a mandatory evaluation of production readiness, addressing:
                1. **Performance**: Index utilization (e.g., filtering/joining on indexed foreign keys or date columns), avoiding heavy table scans, and handling large dataset volumes.
                2. **Security & Data Privacy**: Handling of PII/sensitive data, access control implications, and safe parameterization/filtering practices.
                </guideline>
            </guidelines>
        </sql_generation_task>

        Here is an example with a sample input and an ideal output:
        <sample_input>
            Overview: Extract customer order details from an e-commerce database. Source tables: Orders (contains order transactions), Customers (contains customer information), and Products (contains product catalog). Extraction condition: All orders placed in the last 30 days with order status 'Completed' or 'Shipped'.
            Table Schema: CUSTOMERS: customer_id (INT, PK), customer_name (VARCHAR(100)), email (VARCHAR(100)), country (VARCHAR(50)). ORDERS: order_id (INT, PK), customer_id (INT, FK), order_date (DATE), order_status (VARCHAR(20)), total_amount (DECIMAL(10,2)). PRODUCTS: product_id (INT, PK), product_name (VARCHAR(100)), category (VARCHAR(50)), unit_price (DECIMAL(10,2)). ORDER_ITEMS: order_item_id (INT, PK), order_id (INT, FK), product_id (INT, FK), quantity (INT), item_price (DECIMAL(10,2)).
            Mapping: Customer ID (logical) -> customer_id (physical, INT, required). Customer Name (logical) -> customer_name (physical, VARCHAR(100), required). Order ID (logical) -> order_id (physical, INT, required). Order Date (logical) -> order_date (physical, DATE, required). Order Status (logical) -> order_status (physical, VARCHAR(20), required). Total Amount (logical) -> total_amount (physical, DECIMAL(10,2), required). Product ID (logical) -> product_id (physical, INT, required). Product Name (logical) -> product_name (physical, VARCHAR(100), required). Quantity (logical) -> quantity (physical, INT, required). Item Price (logical) -> item_price (physical, DECIMAL(10,2), required). Transfer rule: Filter by order_date >= CURRENT_DATE - 30 days AND order_status IN ('Completed', 'Shipped').
        </sample_input>
        <ideal_output>
            # SQL Extract Query for Customer Order Details

            Based on the Base Design Requirement and guidelines provided, here is the detail design SQL extract query:

            ```sql
            SELECT
                c.customer_id,
                c.customer_name,
                o.order_id,
                o.order_date,
                o.order_status,
                o.total_amount,
                p.product_id,
                p.product_name,
                oi.quantity,
                oi.item_price
            FROM
                ORDERS o
                INNER JOIN CUSTOMERS c ON o.customer_id = c.customer_id
                INNER JOIN ORDER_ITEMS oi ON o.order_id = oi.order_id
                INNER JOIN PRODUCTS p ON oi.product_id = p.product_id
            WHERE
                o.order_date >= CURRENT_DATE - INTERVAL '30 days'
                AND o.order_status IN ('Completed', 'Shipped')
            ORDER BY
                o.order_date DESC,
                o.order_id ASC,
                oi.order_item_id ASC;
            ```

            ## Query Design Rationale

            | Aspect | Implementation | Compliance |
            |--------|----------------|-----------|
            | **Column Selection** | Exactly the 10 mapped columns selected across tables (no extra/unmapped columns included) | ✓ Guideline 1 (Strict Mapping Contract) |
            | **Join Strategy** | INNER JOINs enforce referential integrity across customer-order-product hierarchy | ✓ Data integrity |
            | **Filtering Condition** | `order_date >= CURRENT_DATE - INTERVAL '30 days'` AND `order_status IN ('Completed', 'Shipped')` | ✓ Mapping transfer rule |
            | **Grouping** | No GROUP BY (detail-level extraction, not aggregation) | ✓ Guideline 2 |
            | **ORDER BY** | All columns referenced (`order_date`, `order_id`) exist in the SELECT clause and mapping | ✓ Guideline 3 |
            | **Performance Impact** | Leverages indexes on `ORDERS.order_date` and foreign keys (`customer_id`, `product_id`) to optimize join and filter performance | ✓ Guideline 4 (Performance) |
            | **Security & Privacy** | Filters out sensitive fields not required by mapping; ensures data extraction adheres to least-privilege attribute scope | ✓ Guideline 4 (Security) |
            | **Result Type** | Granular detail records (one row per order-item combination) | ✓ Business requirement |
        </ideal_output>
    """

    messages = []
    add_user_message(messages, prompt)
    return chat(messages, model=model)

evaluator = PromptEvaluator(max_concurrent_tasks=5)

results = evaluator.run_evaluation(
    run_prompt_function=run_prompt, 
    dataset_file="dataset_dd.json",
    extra_criteria="""
        The output should include:
        - All of column in Mapping must be Selected.
        - The where, join Clauses are all correct
        - The Order by are all correct.
        - The security and the performance of the SQL
    """
)

print(results)