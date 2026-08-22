-- ============================================================================
-- RETAIL SALES & CUSTOMER INSIGHTS: DATABASE SCHEMA DEFINITION (DDL)
-- Database Engine: PostgreSQL 14+ / ANSI SQL
-- Star Schema Model: 1 Fact Table (fact_sales) + 4 Dimension Tables
-- ============================================================================

-- Drop tables if they already exist (in reverse dependency order)
DROP TABLE IF EXISTS fact_sales CASCADE;
DROP TABLE IF EXISTS dim_customer CASCADE;
DROP TABLE IF EXISTS dim_product CASCADE;
DROP TABLE IF EXISTS dim_region CASCADE;
DROP TABLE IF EXISTS dim_date CASCADE;

-- ----------------------------------------------------------------------------
-- 1. DIMENSION: REGIONS (dim_region)
-- ----------------------------------------------------------------------------
CREATE TABLE dim_region (
    region_id VARCHAR(10) PRIMARY KEY,
    region_name VARCHAR(50) NOT NULL,
    state VARCHAR(100) NOT NULL,
    zone VARCHAR(50) NOT NULL
);

-- ----------------------------------------------------------------------------
-- 2. DIMENSION: CUSTOMERS (dim_customer)
-- ----------------------------------------------------------------------------
CREATE TABLE dim_customer (
    customer_id VARCHAR(20) PRIMARY KEY,
    customer_name VARCHAR(100) NOT NULL,
    gender VARCHAR(10) NOT NULL CHECK (gender IN ('Male', 'Female', 'Other')),
    age INTEGER NOT NULL CHECK (age >= 18 AND age <= 100),
    city VARCHAR(50) NOT NULL,
    region_id VARCHAR(10) NOT NULL,
    signup_date DATE NOT NULL,
    customer_segment VARCHAR(30) NOT NULL CHECK (customer_segment IN ('Consumer', 'Corporate', 'Small Business')),
    CONSTRAINT fk_customer_region FOREIGN KEY (region_id) REFERENCES dim_region (region_id)
);

-- ----------------------------------------------------------------------------
-- 3. DIMENSION: PRODUCTS (dim_product)
-- ----------------------------------------------------------------------------
CREATE TABLE dim_product (
    product_id VARCHAR(20) PRIMARY KEY,
    product_name VARCHAR(150) NOT NULL,
    category VARCHAR(50) NOT NULL,
    subcategory VARCHAR(50) NOT NULL,
    brand VARCHAR(50) NOT NULL,
    unit_cost NUMERIC(10, 2) NOT NULL CHECK (unit_cost > 0),
    unit_price NUMERIC(10, 2) NOT NULL CHECK (unit_price > 0)
);

-- ----------------------------------------------------------------------------
-- 4. DIMENSION: DATE (dim_date)
-- ----------------------------------------------------------------------------
CREATE TABLE dim_date (
    date DATE PRIMARY KEY,
    year INTEGER NOT NULL,
    quarter VARCHAR(5) NOT NULL,
    month VARCHAR(20) NOT NULL,
    month_number INTEGER NOT NULL CHECK (month_number BETWEEN 1 AND 12),
    week INTEGER NOT NULL CHECK (week BETWEEN 1 AND 53),
    day INTEGER NOT NULL CHECK (day BETWEEN 1 AND 31),
    day_name VARCHAR(15) NOT NULL
);

-- ----------------------------------------------------------------------------
-- 5. FACT TABLE: SALES (fact_sales)
-- ----------------------------------------------------------------------------
CREATE TABLE fact_sales (
    transaction_id VARCHAR(20) PRIMARY KEY,
    order_id VARCHAR(20) NOT NULL,
    order_date DATE NOT NULL,
    customer_id VARCHAR(20) NOT NULL,
    product_id VARCHAR(20) NOT NULL,
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    unit_price NUMERIC(10, 2) NOT NULL CHECK (unit_price > 0),
    discount NUMERIC(4, 2) NOT NULL DEFAULT 0.00 CHECK (discount >= 0.00 AND discount <= 1.00),
    sales_amount NUMERIC(12, 2) NOT NULL CHECK (sales_amount >= 0),
    cost_amount NUMERIC(12, 2) NOT NULL CHECK (cost_amount >= 0),
    profit NUMERIC(12, 2) NOT NULL,
    payment_method VARCHAR(30) NOT NULL,
    region_id VARCHAR(10) NOT NULL,
    
    -- Foreign Key Constraints
    CONSTRAINT fk_sales_date FOREIGN KEY (order_date) REFERENCES dim_date (date),
    CONSTRAINT fk_sales_customer FOREIGN KEY (customer_id) REFERENCES dim_customer (customer_id),
    CONSTRAINT fk_sales_product FOREIGN KEY (product_id) REFERENCES dim_product (product_id),
    CONSTRAINT fk_sales_region FOREIGN KEY (region_id) REFERENCES dim_region (region_id)
);

-- ----------------------------------------------------------------------------
-- 6. PERFORMANCE OPTIMIZATION INDEXES
-- ----------------------------------------------------------------------------
CREATE INDEX idx_fact_sales_order_id ON fact_sales (order_id);
CREATE INDEX idx_fact_sales_order_date ON fact_sales (order_date);
CREATE INDEX idx_fact_sales_customer_id ON fact_sales (customer_id);
CREATE INDEX idx_fact_sales_product_id ON fact_sales (product_id);
CREATE INDEX idx_fact_sales_region_id ON fact_sales (region_id);
CREATE INDEX idx_dim_product_category ON dim_product (category);
CREATE INDEX idx_dim_customer_segment ON dim_customer (customer_segment);
