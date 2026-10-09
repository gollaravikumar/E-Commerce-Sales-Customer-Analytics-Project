# Project validation

This report records checks run against the files in this repository during review. There is no automated test suite in the project.

| Check | Result | Details |
|---|---|---|
| Python syntax | Passed | The analysis script compiles without syntax errors. |
| Python analysis | Passed | The script ran against the supplied CSV and generated six charts in `screenshots/`. |
| CSV integrity | Passed | 1,500 rows, 12 expected columns, no missing values or duplicate order IDs, and no sales-calculation mismatches. Quantities and prices are positive, discounts are between 0 and 1, and sales are non-negative. |
| Headline metrics | Passed | CSV results: sales 5,763,218.70; 1,500 orders; 348 customers; average order value 3,842.15. These agree with the workbook's cached summary values. |
| Excel file structure | Passed | The workbook contains 10 sheets, 73 formulas, five embedded charts, and five PivotTables. No stored formula-error cells were found. |
| Excel recalculation and PivotTable refresh | Not run | Excel Desktop was not available. Formula and PivotTable behavior after refresh was not tested in Excel. |
| SQL execution | Not run | MySQL and `mysqld` were unavailable. The SQL is written for MySQL and still needs to be run against an imported copy of the CSV. |
| Power BI dashboard | Not run | Power BI Desktop was unavailable; there is no `.pbix` file in the project. |
| Markdown file links | Passed | Relative file links in the Markdown documentation point to existing project files. |
| Secret-pattern scan | Passed | No likely credentials or private-key patterns were found in tracked text files. This scan is not a guarantee that every possible secret format is absent. |

## Reproduce the Python checks

Install the packages listed in [`requirements.txt`](requirements.txt), then run:

```powershell
python python/ecommerce_sales_analysis.py
```

The script prints the row count, missing-value counts, duplicate order count, sales-calculation mismatches, date range, and summary tables. It stops with an error if the source data fails its validation checks.

## SQL and Power BI follow-up

In MySQL Workbench, create the database and table using the first statements in [`ecommerce_sales_analysis.sql`](sql/ecommerce_sales_analysis.sql), import the CSV into `ecommerce_sales`, and then run the remaining queries. Do not treat those query results as verified until they have been executed.

Build the Power BI page using [`PowerBI_Build_Guide.md`](dashboard/PowerBI_Build_Guide.md). Compare its KPI cards with the verified CSV metrics before describing the dashboard as complete.
