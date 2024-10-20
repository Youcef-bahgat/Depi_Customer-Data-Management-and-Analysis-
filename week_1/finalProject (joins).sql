use final_project;
select * from Customers;
select * from Interactions ;
select * from OrderDetails;
select * from Orders;
select * from Products;

-- Join Customers with Orders (To retrieve each customer's orders)
SELECT 
    c.CustomerID,
    c.FirstName,
    c.LastName,
    c.Email,
    o.OrderID,
    o.OrderDate,
    o.OrderStatus,
    o.PaymentMethod
FROM 
    Customers c
JOIN 
    Orders o ON c.CustomerID = o.CustomerID;

GO


--Join Orders with OrderDetails and Products(shows detailed information about each order, including each product in the order, quantity, and computed total)
SELECT 
    o.OrderID,
    o.OrderDate,
    p.ProductName,
    od.Quantity,
    od.Price,
    od.Total  -- Computed as Quantity * Price
FROM 
    Orders o
JOIN 
    OrderDetails od ON o.OrderID = od.OrderID
JOIN 
    Products p ON od.ProductID = p.ProductID;

GO


--Join Customers with Interactions(to analyze customer interactions)
SELECT 
    c.CustomerID,
    c.FirstName,
    c.LastName,
    i.InteractionType,
    i.InteractionDate
FROM 
    Customers c
JOIN 
    Interactions i ON c.CustomerID = i.CustomerID;

GO


--Total Spend per Customer( calculates each customer's total expenditure across all orders)
SELECT 
    c.CustomerID,
    c.FirstName,
    c.LastName,
    SUM(od.Total) AS TotalSpend
FROM 
    Customers c
JOIN 
    Orders o ON c.CustomerID = o.CustomerID
JOIN 
    OrderDetails od ON o.OrderID = od.OrderID
GROUP BY 
    c.CustomerID, c.FirstName, c.LastName;
 -- „‘ ﬂ· «·ﬂ«” Ê„—“ ⁄«„·Ì‰ «Ê—œ—“

 GO

 --Top-Selling Products
 SELECT 
    p.ProductID,
    p.ProductName,
    SUM(od.Quantity) AS TotalQuantitySold
FROM 
    Products p
JOIN 
    OrderDetails od ON p.ProductID = od.ProductID
GROUP BY 
    p.ProductID, p.ProductName
ORDER BY 
    TotalQuantitySold DESC;

GO

--Customer Order Frequency and Recency(provides information on the number of orders and the most recent order date for each customer)
SELECT 
    c.CustomerID,
    c.FirstName,
    c.LastName,
    COUNT(o.OrderID) AS OrderCount,
    MAX(o.OrderDate) AS LastOrderDate
FROM 
    Customers c
LEFT JOIN 
    Orders o ON c.CustomerID = o.CustomerID
GROUP BY 
    c.CustomerID, c.FirstName, c.LastName;

GO

--Product Revenue Contribution(To see the revenue contribution of each product, this join multiplies Quantity and Price to get total revenue per product)
SELECT 
    p.ProductID,
    p.ProductName,
    SUM(od.Total) AS TotalRevenue
FROM 
    Products p
JOIN 
    OrderDetails od ON p.ProductID = od.ProductID
GROUP BY 
    p.ProductID, p.ProductName
ORDER BY 
    TotalRevenue DESC;

GO
 
 --Customer Purchase History with Last Interaction Date(shows each customer's purchase details along with their most recent interaction date)
 SELECT 
    c.CustomerID,
    c.FirstName,
    c.LastName,
    o.OrderID,
    o.OrderDate,
    MAX(i.InteractionDate) AS LastInteractionDate
FROM 
    Customers c
LEFT JOIN 
    Orders o ON c.CustomerID = o.CustomerID
LEFT JOIN 
    Interactions i ON c.CustomerID = i.CustomerID
GROUP BY 
    c.CustomerID, c.FirstName, c.LastName, o.OrderID, o.OrderDate;

GO

--Products with Low Stock
SELECT 
    p.ProductID,
    p.ProductName,
    p.StockQuantity
FROM 
    Products p
WHERE 
    p.StockQuantity < 10
ORDER BY 
    p.StockQuantity ASC;

GO

-- Full Join for Customer Orders with Products and Interactions 
--To create a complete report including customer details, orders, products, and interaction history
SELECT 
    c.CustomerID,
    c.FirstName,
    c.LastName,
    o.OrderID,
    o.OrderDate,
    o.OrderStatus,
    p.ProductName,
    od.Quantity,
    od.Total,
    i.InteractionType,
    i.InteractionDate
FROM 
    Customers c
LEFT JOIN 
    Orders o ON c.CustomerID = o.CustomerID
LEFT JOIN 
    OrderDetails od ON o.OrderID = od.OrderID
LEFT JOIN 
    Products p ON od.ProductID = p.ProductID
LEFT JOIN 
    Interactions i ON c.CustomerID = i.CustomerID;


