-- E-Commerce Sales Analysis
-- Dialect: MySQL 8.0+
-- Create the database and table, import data/ecommerce_sales.csv into
-- ecommerce_sales with MySQL Workbench, then run the queries below.

CREATE DATABASE IF NOT EXISTS ecommerce_sales_analysis;
USE ecommerce_sales_analysis;

CREATE TABLE IF NOT EXISTS ecommerce_sales (
    Order_ID VARCHAR(20) NOT NULL,
    Order_Date DATE NOT NULL,
    Customer_ID VARCHAR(20) NOT NULL,
    Product VARCHAR(100) NOT NULL,
    Category VARCHAR(50) NOT NULL,
    Region VARCHAR(30) NOT NULL,
    Quantity INT NOT NULL,
    Unit_Price DECIMAL(12, 2) NOT NULL,
    Discount DECIMAL(5, 2) NOT NULL,
    Sales DECIMAL(12, 2) NOT NULL,
    Payment_Method VARCHAR(40) NOT NULL,
    Customer_Segment VARCHAR(30) NOT NULL
);

-- Data quality checks

-- Imported row count; the supplied CSV has 1,500 rows.
SELECT COUNT(*) AS total_rows
FROM ecommerce_sales;

-- A clean dataset returns no rows.
SELECT
    Order_ID,
    COUNT(*) AS occurrences
FROM ecommerce_sales
GROUP BY Order_ID
HAVING COUNT(*) > 1;

-- A clean dataset returns no rows.
SELECT
    Order_ID,
    Sales AS recorded_sales,
    ROUND(Quantity * Unit_Price * (1 - Discount), 2) AS expected_sales
FROM ecommerce_sales
WHERE ABS(
    Sales - ROUND(Quantity * Unit_Price * (1 - Discount), 2)
) > 0.01;

-- NULL counts for each column
SELECT
    SUM(Order_ID IS NULL) AS missing_order_id,
    SUM(Order_Date IS NULL) AS missing_order_date,
    SUM(Customer_ID IS NULL) AS missing_customer_id,
    SUM(Product IS NULL) AS missing_product,
    SUM(Category IS NULL) AS missing_category,
    SUM(Region IS NULL) AS missing_region,
    SUM(Quantity IS NULL) AS missing_quantity,
    SUM(Unit_Price IS NULL) AS missing_unit_price,
    SUM(Discount IS NULL) AS missing_discount,
    SUM(Sales IS NULL) AS missing_sales,
    SUM(Payment_Method IS NULL) AS missing_payment_method,
    SUM(Customer_Segment IS NULL) AS missing_customer_segment
FROM ecommerce_sales;

-- Date, quantity, and sales ranges
SELECT
    MIN(Order_Date) AS earliest_order_date,
    MAX(Order_Date) AS latest_order_date
FROM ecommerce_sales;

SELECT
    MIN(Quantity) AS minimum_quantity,
    MAX(Quantity) AS maximum_quantity,
    MIN(Unit_Price) AS minimum_unit_price,
    MAX(Unit_Price) AS maximum_unit_price,
    MIN(Discount) AS minimum_discount,
    MAX(Discount) AS maximum_discount,
    MIN(Sales) AS minimum_sales,
    MAX(Sales) AS maximum_sales
FROM ecommerce_sales;

-- Overall sales metrics
SELECT
    ROUND(SUM(Sales), 2) AS total_sales,
    COUNT(DISTINCT Order_ID) AS total_orders,
    COUNT(DISTINCT Customer_ID) AS unique_customers,
    ROUND(SUM(Sales) / NULLIF(COUNT(DISTINCT Order_ID), 0), 2)
        AS average_order_value
FROM ecommerce_sales;

-- Sales, quantity, and order count by category
SELECT
    Category,
    ROUND(SUM(Sales), 2) AS total_sales,
    SUM(Quantity) AS total_quantity,
    COUNT(DISTINCT Order_ID) AS order_count
FROM ecommerce_sales
GROUP BY Category
ORDER BY total_sales DESC;

-- Sales, quantity, and order count by region
SELECT
    Region,
    ROUND(SUM(Sales), 2) AS total_sales,
    SUM(Quantity) AS total_quantity,
    COUNT(DISTINCT Order_ID) AS order_count
FROM ecommerce_sales
GROUP BY Region
ORDER BY total_sales DESC;

-- Monthly sales and orders, ordered chronologically
SELECT
    DATE_FORMAT(Order_Date, '%Y-%m') AS order_month,
    ROUND(SUM(Sales), 2) AS total_sales,
    COUNT(DISTINCT Order_ID) AS order_count
FROM ecommerce_sales
GROUP BY DATE_FORMAT(Order_Date, '%Y-%m')
ORDER BY order_month;

-- Ten products with the highest sales
SELECT
    Product,
    ROUND(SUM(Sales), 2) AS total_sales,
    SUM(Quantity) AS total_quantity,
    COUNT(DISTINCT Order_ID) AS order_count
FROM ecommerce_sales
GROUP BY Product
ORDER BY total_sales DESC
LIMIT 10;

-- Ten products with the highest quantity sold
SELECT
    Product,
    SUM(Quantity) AS total_quantity,
    ROUND(SUM(Sales), 2) AS total_sales
FROM ecommerce_sales
GROUP BY Product
ORDER BY total_quantity DESC, total_sales DESC
LIMIT 10;

-- Sales and order count by customer segment
SELECT
    Customer_Segment,
    ROUND(SUM(Sales), 2) AS total_sales,
    COUNT(DISTINCT Order_ID) AS order_count
FROM ecommerce_sales
GROUP BY Customer_Segment
ORDER BY total_sales DESC;

-- Payment-method usage and associated sales
SELECT
    Payment_Method,
    COUNT(DISTINCT Order_ID) AS order_count,
    ROUND(SUM(Sales), 2) AS total_sales
FROM ecommerce_sales
GROUP BY Payment_Method
ORDER BY order_count DESC;

-- Ten customers with the highest sales contribution
SELECT
    Customer_ID,
    ROUND(SUM(Sales), 2) AS total_sales,
    COUNT(DISTINCT Order_ID) AS order_count,
    SUM(Quantity) AS total_quantity
FROM ecommerce_sales
GROUP BY Customer_ID
ORDER BY total_sales DESC
LIMIT 10;
