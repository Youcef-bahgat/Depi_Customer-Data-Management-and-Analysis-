SELECT 
    t.TransactionDate, 
    t.ProductID, 
    p.ProductName, 
    SUM(t.Quantity) AS total_quantity_sold, 
    SUM(t.FinalAmount) AS total_sales
FROM 
    Transactions t
JOIN 
    Products p ON t.ProductID = p.ProductID
GROUP BY 
    t.TransactionDate, 
    t.ProductID, 
    p.ProductName
ORDER BY 
    t.TransactionDate;



CREATE TABLE SalesForecastingData (
    id INT PRIMARY KEY IDENTITY(1,1),
    transaction_date DATE,
    product_id INT,
    product_name VARCHAR(255),
    total_quantity_sold INT,
    total_sales DECIMAL(10, 2)
);


INSERT INTO SalesForecastingData (transaction_date, product_id, product_name, total_quantity_sold, total_sales)
SELECT 
    t.TransactionDate, 
    t.ProductID, 
    p.ProductName, 
    SUM(t.Quantity) AS total_quantity_sold, 
    SUM(t.FinalAmount) AS total_sales
FROM 
    Transactions t
JOIN 
    Products p ON t.ProductID = p.ProductID
GROUP BY 
    t.TransactionDate, 
    t.ProductID, 
    p.ProductName
ORDER BY 
    t.TransactionDate;

select * from SalesForecastingData


