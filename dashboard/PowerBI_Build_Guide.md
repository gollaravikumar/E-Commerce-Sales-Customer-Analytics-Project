# Power BI Dashboard Build Guide

The Power BI page is a planned deliverable, not a finished dashboard. This guide records the steps and measures to use when building the `.pbix` in Power BI Desktop. No placeholder dashboard file is included.

## 1. Import the CSV

1. Open Power BI Desktop and select **Get data > Text/CSV**.
2. Select `data/ecommerce_sales.csv` and choose **Transform Data**.
3. In Power Query, rename the query to `ecommerce_sales`.
4. Set `Order_Date` to **Date**; `Quantity` to **Whole Number**; `Unit_Price`, `Discount`, and `Sales` to **Decimal Number**. Keep the ID, product, category, region, payment, and segment columns as text.
5. Keep all source rows and use the CSV as the data source. Select **Close & Apply**.

## 2. Add the measures

Create these measures on the `ecommerce_sales` table:

```DAX
Total Sales = SUM(ecommerce_sales[Sales])

Total Orders = DISTINCTCOUNT(ecommerce_sales[Order_ID])

Unique Customers = DISTINCTCOUNT(ecommerce_sales[Customer_ID])

Average Order Value = DIVIDE([Total Sales], [Total Orders])
```

Format **Total Sales** and **Average Order Value** as decimal numbers with two decimal places. The dataset does not specify a currency, so do not add a currency symbol.

## 3. Add a month field

Create this calculated column so the line chart uses real chronological months:

```DAX
Order Month = DATE(
    YEAR(ecommerce_sales[Order_Date]),
    MONTH(ecommerce_sales[Order_Date]),
    1
)
```

Set its data type to **Date** and display format to `MMM yyyy`. Use ascending date order.

## 4. Build one dashboard page

Use a single page named **Sales Overview**. Suggested placement:

- Top row: four Card visuals for **Total Sales**, **Total Orders**, **Unique Customers**, and **Average Order Value**.
- Middle row: **Monthly Sales Trend** line chart and **Sales by Category** clustered bar chart.
- Bottom row: **Sales by Region** clustered bar chart, **Top 10 Products** horizontal bar chart, and **Sales by Customer Segment** clustered bar chart.
- Place the slicers in a narrow column or strip so they filter the page without crowding the visuals.

Field placement:

| Visual | Fields |
|---|---|
| Monthly Sales Trend | X-axis: `Order Month`; Y-axis: `[Total Sales]` |
| Sales by Category | Y-axis: `Category`; X-axis: `[Total Sales]` |
| Sales by Region | Y-axis: `Region`; X-axis: `[Total Sales]` |
| Top 10 Products | Y-axis: `Product`; X-axis: `[Total Sales]`; visual filter: **Top N**, 10, by `[Total Sales]` |
| Sales by Customer Segment | Y-axis: `Customer_Segment`; X-axis: `[Total Sales]` |
| KPI Cards | One card each for the four measures above |

Add slicers for `Order_Date`, `Category`, `Region`, `Customer_Segment`, and `Payment_Method`. Use a date range slicer for `Order_Date`.

## 5. Keep the design simple

- Use a light background and a restrained blue/teal accent palette.
- Use clear chart titles and readable labels; avoid 3D visuals and decorative clutter.
- Keep the products chart sorted by `[Total Sales]` descending.
- Confirm all slicers affect the intended visuals.

## 6. Validate and save

With no slicers selected, the KPI cards should show:

- Total Sales: **5,763,218.70**
- Total Orders: **1,500**
- Unique Customers: **348**
- Average Order Value: **3,842.15**

Compare those values with the Excel workbook and Python output before saving as `dashboard/E-Commerce_Sales_Dashboard.pbix`. Once built, capture the page with **Win+Shift+S** and save the genuine screen capture as `screenshots/powerbi_dashboard.png`. Do not use a mockup in place of the Power BI screen.
