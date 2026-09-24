-- Tredence-style SQL analysis for AdventureWorks retail demand
-- Compatible with SQL Server syntax with minor adaptation for other databases.

-- 1) Weekly SKU demand
WITH weekly_demand AS (
    SELECT
        ProductKey,
        DATEADD(day, 1 - DATEPART(weekday, OrderDate), CAST(OrderDate AS date)) AS WeekStart,
        SUM(OrderQuantity) AS WeeklyDemand
    FROM Sales
    GROUP BY ProductKey,
             DATEADD(day, 1 - DATEPART(weekday, OrderDate), CAST(OrderDate AS date))
)
SELECT *
FROM weekly_demand
ORDER BY ProductKey, WeekStart;

-- 2) Lag and rolling-demand features using window functions
WITH weekly_demand AS (
    SELECT ProductKey, CAST(OrderDate AS date) AS OrderDate, SUM(OrderQuantity) AS Demand
    FROM Sales
    GROUP BY ProductKey, CAST(OrderDate AS date)
)
SELECT
    ProductKey,
    OrderDate,
    Demand,
    LAG(Demand, 1) OVER (PARTITION BY ProductKey ORDER BY OrderDate) AS Lag1,
    LAG(Demand, 7) OVER (PARTITION BY ProductKey ORDER BY OrderDate) AS Lag7,
    AVG(CAST(Demand AS float)) OVER (
        PARTITION BY ProductKey ORDER BY OrderDate
        ROWS BETWEEN 28 PRECEDING AND 1 PRECEDING
    ) AS RollingAvg28
FROM weekly_demand;

-- 3) Product profitability context
SELECT
    s.ProductKey,
    p.ProductName,
    SUM(s.OrderQuantity) AS UnitsSold,
    SUM(s.OrderQuantity * p.ProductPrice) AS Revenue,
    SUM(s.OrderQuantity * p.ProductCost) AS EstimatedCost,
    SUM(s.OrderQuantity * (p.ProductPrice - p.ProductCost)) AS GrossMargin
FROM Sales s
JOIN Products p ON s.ProductKey = p.ProductKey
GROUP BY s.ProductKey, p.ProductName
ORDER BY GrossMargin DESC;
