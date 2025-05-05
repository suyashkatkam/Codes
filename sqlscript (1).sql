REM   Script: Session 03
REM   This may save your life

CREATE TABLE Dim_Date ( 
    date_id       NUMBER PRIMARY KEY, 
    full_date     DATE, 
    day_name      VARCHAR2(10), 
    month_name    VARCHAR2(10), 
    year          NUMBER 
);

CREATE TABLE Dim_Customer ( 
    customer_id   NUMBER PRIMARY KEY, 
    customer_name VARCHAR2(50), 
    gender        CHAR(1), 
    region        VARCHAR2(30) 
);

CREATE TABLE Dim_Product ( 
    product_id    NUMBER PRIMARY KEY, 
    product_name  VARCHAR2(50), 
    category      VARCHAR2(30), 
    brand         VARCHAR2(30) 
);

CREATE TABLE Dim_Store ( 
    store_id      NUMBER PRIMARY KEY, 
    store_name    VARCHAR2(50), 
    location      VARCHAR2(50) 
);

CREATE TABLE Sales_Fact ( 
    sales_id      NUMBER PRIMARY KEY, 
    date_id       NUMBER REFERENCES Dim_Date(date_id), 
    customer_id   NUMBER REFERENCES Dim_Customer(customer_id), 
    product_id    NUMBER REFERENCES Dim_Product(product_id), 
    store_id      NUMBER REFERENCES Dim_Store(store_id), 
    quantity_sold NUMBER, 
    total_amount  NUMBER 
);

CREATE SEQUENCE seq_date_id START WITH 1 INCREMENT BY 1;

CREATE SEQUENCE seq_customer_id START WITH 1 INCREMENT BY 1;

CREATE SEQUENCE seq_product_id START WITH 1 INCREMENT BY 1;

CREATE SEQUENCE seq_store_id START WITH 1 INCREMENT BY 1;

CREATE SEQUENCE seq_sales_id START WITH 1 INCREMENT BY 1;

INSERT INTO Dim_Date VALUES (seq_date_id.NEXTVAL, TO_DATE('2025-05-01', 'YYYY-MM-DD'), 'Thursday', 'May', 2025);

INSERT INTO Dim_Date VALUES (seq_date_id.NEXTVAL, TO_DATE('2025-05-02', 'YYYY-MM-DD'), 'Friday', 'May', 2025);

INSERT INTO Dim_Date VALUES (seq_date_id.NEXTVAL, TO_DATE('2025-05-03', 'YYYY-MM-DD'), 'Saturday', 'May', 2025);

INSERT INTO Dim_Date VALUES (seq_date_id.NEXTVAL, TO_DATE('2025-05-04', 'YYYY-MM-DD'), 'Sunday', 'May', 2025);

INSERT INTO Dim_Date VALUES (seq_date_id.NEXTVAL, TO_DATE('2025-05-05', 'YYYY-MM-DD'), 'Monday', 'May', 2025);

INSERT INTO Dim_Customer VALUES (seq_customer_id.NEXTVAL, 'Alice', 'F', 'East');

INSERT INTO Dim_Customer VALUES (seq_customer_id.NEXTVAL, 'Bob', 'M', 'West');

INSERT INTO Dim_Customer VALUES (seq_customer_id.NEXTVAL, 'Carol', 'F', 'North');

INSERT INTO Dim_Customer VALUES (seq_customer_id.NEXTVAL, 'Dave', 'M', 'South');

INSERT INTO Dim_Customer VALUES (seq_customer_id.NEXTVAL, 'Eve', 'F', 'Central');

INSERT INTO Dim_Product VALUES (seq_product_id.NEXTVAL, 'Laptop', 'Electronics', 'Dell');

INSERT INTO Dim_Product VALUES (seq_product_id.NEXTVAL, 'Phone', 'Electronics', 'Samsung');

INSERT INTO Dim_Product VALUES (seq_product_id.NEXTVAL, 'Tablet', 'Electronics', 'Apple');

INSERT INTO Dim_Product VALUES (seq_product_id.NEXTVAL, 'Headphones', 'Accessories', 'Sony');

INSERT INTO Dim_Product VALUES (seq_product_id.NEXTVAL, 'Camera', 'Photography', 'Canon');

INSERT INTO Dim_Store VALUES (seq_store_id.NEXTVAL, 'Store A', 'New York');

INSERT INTO Dim_Store VALUES (seq_store_id.NEXTVAL, 'Store B', 'Los Angeles');

INSERT INTO Dim_Store VALUES (seq_store_id.NEXTVAL, 'Store C', 'Chicago');

INSERT INTO Dim_Store VALUES (seq_store_id.NEXTVAL, 'Store D', 'Houston');

INSERT INTO Dim_Store VALUES (seq_store_id.NEXTVAL, 'Store E', 'Phoenix');

INSERT INTO Sales_Fact (sales_id, date_id, customer_id, product_id, store_id, quantity_sold, total_amount) 
SELECT 
    seq_sales_id.NEXTVAL, 
    d.date_id, 
    c.customer_id, 
    p.product_id, 
    s.store_id, 
    FLOOR(DBMS_RANDOM.VALUE(1, 10)), -- quantity_sold (1 to 9) 
    FLOOR(DBMS_RANDOM.VALUE(100, 1000)) -- total_amount ($100 to $999) 
FROM 
    Dim_Date d 
CROSS JOIN 
    Dim_Customer c 
CROSS JOIN 
    Dim_Product p 
CROSS JOIN 
    Dim_Store s;

SELECT COUNT(*) AS total_fact_rows FROM Sales_Fact;

SELECT 
    f.sales_id, d.full_date, c.customer_name, p.product_name, s.store_name, f.total_amount 
FROM 
    Sales_Fact f 
    JOIN Dim_Date d ON f.date_id = d.date_id 
    JOIN Dim_Customer c ON f.customer_id = c.customer_id 
    JOIN Dim_Product p ON f.product_id = p.product_id 
    JOIN Dim_Store s ON f.store_id = s.store_id 
WHERE 
    d.full_date = TO_DATE('2025-05-01', 'YYYY-MM-DD');

SELECT 
    d.full_date, c.customer_name, c.region, p.product_name, p.category, s.store_name, f.total_amount 
FROM 
    Sales_Fact f 
    JOIN Dim_Date d ON f.date_id = d.date_id 
    JOIN Dim_Customer c ON f.customer_id = c.customer_id 
    JOIN Dim_Product p ON f.product_id = p.product_id 
    JOIN Dim_Store s ON f.store_id = s.store_id 
WHERE 
    c.region IN ('East', 'West') 
    AND p.category = 'Electronics';

SELECT 
    p.product_name, 
    s.store_name, 
    SUM(f.total_amount) AS total_sales 
FROM 
    Sales_Fact f 
    JOIN Dim_Product p ON f.product_id = p.product_id 
    JOIN Dim_Store s ON f.store_id = s.store_id 
GROUP BY ROLLUP (p.product_name, s.store_name);

SELECT 
    d.year, 
    d.month_name, 
    d.full_date, 
    SUM(f.total_amount) AS total_sales 
FROM 
    Sales_Fact f 
    JOIN Dim_Date d ON f.date_id = d.date_id 
GROUP BY d.year, d.month_name, d.full_date 
ORDER BY d.year, d.month_name, d.full_date;

SELECT * 
FROM ( 
    SELECT 
        c.customer_name, 
        p.product_name, 
        f.total_amount 
    FROM 
        Sales_Fact f 
        JOIN Dim_Customer c ON f.customer_id = c.customer_id 
        JOIN Dim_Product p ON f.product_id = p.product_id 
) 
PIVOT ( 
    SUM(total_amount) 
    FOR product_name IN ('Laptop' AS Laptop, 'Phone' AS Phone, 'Tablet' AS Tablet, 'Headphones' AS Headphones, 'Camera' AS Camera) 
) 
ORDER BY customer_name;

