# Project discussion notes

### What does the project analyze?

It summarizes sales across months, products, regions, payment methods, and customer segments using a synthetic dataset of 1,500 orders from 2025.

### What was the business question?

The analysis compares sales across business groups and notes what other information would be needed before acting on those differences.

### Where did the data come from?

It is synthetic data supplied for portfolio practice, not a real company's sales records.

### What checks did you perform?

I checked for missing values and duplicate order IDs, compared `Sales` with quantity times unit price after discount, reviewed the date and numeric ranges, and compared summary results across the CSV and workbook.

### How is average order value calculated?

It is total sales divided by the number of distinct order IDs. Each row in this dataset represents one order.

### Why use PivotTables?

They let me compare the same source rows by category, region, product, customer, and segment without building separate formulas for each group.

### What does the SQL file contain?

It has a MySQL table definition, data checks, and queries for overall metrics and grouped results. The queries still need to be run in MySQL Workbench.

### Why include Python?

The script repeats the checks and grouped calculations from the CSV and saves charts that are easy to share separately from the workbook.

### What is one result worth discussing?

Home & Kitchen has the highest category sales at 1,860,988.10, followed by Electronics at 1,792,523.15. These are sales totals, not profit figures.

### What is one important limitation?

The data covers only one synthetic year and has no cost or margin fields. It cannot establish a recurring seasonal pattern or identify the most profitable category.

### Is the Power BI dashboard finished?

No. The repository contains a build guide, but the `.pbix` file has not been created or tested.

### What would you do next?

I would run the SQL queries against an imported CSV, build and validate the Power BI page, and look for additional years and cost data before making broader recommendations.
