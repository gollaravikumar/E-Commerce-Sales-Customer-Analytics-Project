"""Exploratory sales analysis for the e-commerce portfolio project."""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib.ticker import FuncFormatter

# =========================================================
# PROJECT PATHS
# =========================================================

PROJECT_DIR = Path(__file__).resolve().parents[1]

DATA_PATH = PROJECT_DIR / "data" / "ecommerce_sales.csv"
CHART_DIR = PROJECT_DIR / "screenshots"


EXPECTED_COLUMNS = [
    "Order_ID",
    "Order_Date",
    "Customer_ID",
    "Product",
    "Category",
    "Region",
    "Quantity",
    "Unit_Price",
    "Discount",
    "Sales",
    "Payment_Method",
    "Customer_Segment",
]


# =========================================================
# CHART SETTINGS
# =========================================================

sns.set_theme(style="whitegrid")

# Simple consistent font size
plt.rcParams["axes.titlesize"] = 14
plt.rcParams["axes.labelsize"] = 11
plt.rcParams["xtick.labelsize"] = 10
plt.rcParams["ytick.labelsize"] = 10


# =========================================================
# HELPER FUNCTIONS
# =========================================================


def format_lakhs(value, position):
    """Format values in lakhs without assuming a currency."""
    return f"{value / 100000:.1f}L"


def add_bar_labels(ax, values, horizontal=False):
    """Add simple value labels to bar charts."""

    if horizontal:
        for bar, value in zip(ax.patches, values):
            ax.text(
                bar.get_width() + max(values) * 0.01,
                bar.get_y() + bar.get_height() / 2,
                f"{value / 100000:.1f}L",
                va="center",
                fontsize=9,
            )
    else:
        for bar, value in zip(ax.patches, values):
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                bar.get_height() + max(values) * 0.015,
                f"{value / 100000:.1f}L",
                ha="center",
                va="bottom",
                fontsize=9,
            )


def save_chart(fig, filename):
    """Save and display a chart."""

    CHART_DIR.mkdir(parents=True, exist_ok=True)

    output_path = CHART_DIR / filename

    fig.tight_layout()

    fig.savefig(output_path, dpi=160, bbox_inches="tight")

    print(f"Saved chart: " f"{output_path.relative_to(PROJECT_DIR)}")

    if plt.get_backend().lower() not in {
        "agg",
        "cairo",
        "pdf",
        "pgf",
        "ps",
        "svg",
        "template",
    }:
        plt.show()

    plt.close(fig)


# =========================================================
# MAIN PROGRAM
# =========================================================


def main():

    # =====================================================
    # 1. LOAD DATA
    # =====================================================

    if not DATA_PATH.exists():
        raise FileNotFoundError(f"Could not find the source CSV:\n{DATA_PATH}")

    df = pd.read_csv(DATA_PATH, parse_dates=["Order_Date"])

    if df.empty:
        raise ValueError("The source CSV contains no order rows.")

    missing_columns = [
        column for column in EXPECTED_COLUMNS if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(f"The source CSV is missing:\n" f"{missing_columns}")

    # =====================================================
    # 2. INSPECT DATASET
    # =====================================================

    print("=" * 60)
    print("E-COMMERCE SALES ANALYSIS")
    print("=" * 60)

    print("\nDataset shape:")
    print(df.shape)

    print("\nFirst five rows:")
    print(df.head().to_string(index=False))

    print("\nColumns:")
    print(list(df.columns))

    # =====================================================
    # 3. DATA QUALITY CHECKS
    # =====================================================

    missing_values = df.isna().sum()

    duplicate_orders = int(df["Order_ID"].duplicated().sum())

    expected_sales = df["Quantity"] * df["Unit_Price"] * (1 - df["Discount"])

    sales_mismatches = int(
        (~np.isclose(df["Sales"], expected_sales, rtol=1e-9, atol=1e-6)).sum()
    )

    print("\n" + "=" * 60)
    print("DATA QUALITY CHECK")
    print("=" * 60)

    print("\nMissing values:")
    print(missing_values.to_string())

    print(f"\nDuplicate Order_ID values: " f"{duplicate_orders}")

    print("Sales calculation mismatches: " f"{sales_mismatches}")

    print(
        f"Order date range: "
        f"{df['Order_Date'].min().date()} "
        f"to "
        f"{df['Order_Date'].max().date()}"
    )

    if missing_values.any():
        raise ValueError("The source CSV contains missing values.")
    if duplicate_orders:
        raise ValueError("The source CSV contains duplicate Order_ID values.")
    if sales_mismatches:
        raise ValueError("Some Sales values do not match quantity, price, and discount.")

    numeric_columns = ["Quantity", "Unit_Price", "Discount", "Sales"]
    if not np.isfinite(df[numeric_columns].to_numpy()).all():
        raise ValueError("The source CSV contains non-finite numeric values.")
    if (df["Quantity"] <= 0).any():
        raise ValueError("Quantity values must be greater than zero.")
    if (df["Unit_Price"] <= 0).any():
        raise ValueError("Unit_Price values must be greater than zero.")
    if not df["Discount"].between(0, 1).all():
        raise ValueError("Discount values must be between zero and one.")
    if (df["Sales"] < 0).any():
        raise ValueError("Sales values cannot be negative.")

    # =====================================================
    # 4. DESCRIPTIVE STATISTICS
    # =====================================================

    print("\n" + "=" * 60)
    print("DESCRIPTIVE STATISTICS")
    print("=" * 60)

    print(df.select_dtypes(include=np.number).describe().round(2).to_string())

    # =====================================================
    # 5. OVERALL SALES METRICS
    # =====================================================

    total_sales = float(df["Sales"].sum())

    total_orders = int(df["Order_ID"].nunique())

    unique_customers = int(df["Customer_ID"].nunique())

    total_quantity = int(df["Quantity"].sum())

    average_order_value = total_sales / total_orders

    print("\n" + "=" * 60)
    print("OVERALL SALES METRICS")
    print("=" * 60)

    print(f"Total sales: " f"{total_sales:,.2f}")

    print(f"Total orders: " f"{total_orders:,}")

    print(f"Unique customers: " f"{unique_customers:,}")

    print(f"Total quantity sold: " f"{total_quantity:,}")

    print(f"Average order value: " f"{average_order_value:,.2f}")

    # =====================================================
    # 6. CATEGORY ANALYSIS
    # =====================================================

    category_analysis = (
        df.groupby("Category", as_index=False)
        .agg(
            Total_Sales=("Sales", "sum"),
            Total_Quantity=("Quantity", "sum"),
            Order_Count=("Order_ID", "nunique"),
        )
        .sort_values("Total_Sales", ascending=False)
    )

    print("\n" + "=" * 60)
    print("SALES BY CATEGORY")
    print("=" * 60)

    print(category_analysis.round(2).to_string(index=False))

    # =====================================================
    # 7. REGION ANALYSIS
    # =====================================================

    region_analysis = (
        df.groupby("Region", as_index=False)
        .agg(
            Total_Sales=("Sales", "sum"),
            Total_Quantity=("Quantity", "sum"),
            Order_Count=("Order_ID", "nunique"),
        )
        .sort_values("Total_Sales", ascending=False)
    )

    print("\n" + "=" * 60)
    print("SALES BY REGION")
    print("=" * 60)

    print(region_analysis.round(2).to_string(index=False))

    # =====================================================
    # 8. MONTHLY ANALYSIS
    # =====================================================

    df["Month"] = df["Order_Date"].dt.to_period("M").dt.to_timestamp()

    monthly_analysis = (
        df.groupby("Month", as_index=False)
        .agg(
            Total_Sales=("Sales", "sum"),
            Order_Count=("Order_ID", "nunique"),
        )
        .sort_values("Month")
    )

    print("\n" + "=" * 60)
    print("MONTHLY SALES")
    print("=" * 60)

    monthly_display = monthly_analysis.copy()

    monthly_display["Month"] = monthly_display["Month"].dt.strftime("%B %Y")

    print(monthly_display.round(2).to_string(index=False))

    # =====================================================
    # 9. PRODUCT ANALYSIS
    # =====================================================

    product_analysis = (
        df.groupby("Product", as_index=False)
        .agg(
            Total_Sales=("Sales", "sum"),
            Total_Quantity=("Quantity", "sum"),
            Order_Count=("Order_ID", "nunique"),
        )
        .sort_values("Total_Sales", ascending=False)
    )

    top_products_sales = product_analysis.head(10).copy()

    top_products_quantity = (
        product_analysis.sort_values(
            ["Total_Quantity", "Total_Sales"], ascending=[False, False]
        )
        .head(10)
        .copy()
    )

    print("\n" + "=" * 60)
    print("TOP 10 PRODUCTS BY SALES")
    print("=" * 60)

    print(top_products_sales.round(2).to_string(index=False))

    print("\n" + "=" * 60)
    print("TOP 10 PRODUCTS BY QUANTITY")
    print("=" * 60)

    print(top_products_quantity.round(2).to_string(index=False))

    # =====================================================
    # 10. CUSTOMER ANALYSIS
    # =====================================================

    customer_analysis = (
        df.groupby("Customer_ID", as_index=False)
        .agg(
            Total_Sales=("Sales", "sum"),
            Order_Count=("Order_ID", "nunique"),
            Total_Quantity=("Quantity", "sum"),
        )
        .sort_values("Total_Sales", ascending=False)
    )

    print("\n" + "=" * 60)
    print("TOP 10 CUSTOMERS BY SALES")
    print("=" * 60)

    print(customer_analysis.head(10).round(2).to_string(index=False))

    # =====================================================
    # 11. CUSTOMER SEGMENT
    # =====================================================

    segment_analysis = (
        df.groupby("Customer_Segment", as_index=False)
        .agg(
            Total_Sales=("Sales", "sum"),
            Order_Count=("Order_ID", "nunique"),
        )
        .sort_values("Total_Sales", ascending=False)
    )

    print("\n" + "=" * 60)
    print("SALES BY CUSTOMER SEGMENT")
    print("=" * 60)

    print(segment_analysis.round(2).to_string(index=False))

    # =====================================================
    # 12. PAYMENT METHOD
    # =====================================================

    payment_analysis = (
        df.groupby("Payment_Method", as_index=False)
        .agg(
            Order_Count=("Order_ID", "nunique"),
            Total_Sales=("Sales", "sum"),
        )
        .sort_values("Order_Count", ascending=False)
    )

    print("\n" + "=" * 60)
    print("PAYMENT METHOD USAGE")
    print("=" * 60)

    print(payment_analysis.round(2).to_string(index=False))

    # =====================================================
    # 13. CREATE VISUALIZATIONS
    # =====================================================

    print("\n" + "=" * 60)
    print("CREATING CHARTS")
    print("=" * 60)

    # -----------------------------------------------------
    # CHART 1: MONTHLY SALES TREND
    # -----------------------------------------------------

    fig, ax = plt.subplots(figsize=(10, 5.5))

    ax.plot(
        monthly_analysis["Month"],
        monthly_analysis["Total_Sales"],
        marker="o",
        linewidth=2,
    )

    ax.set_title("Monthly Sales Trend — 2025", fontweight="bold")

    ax.set_xlabel("Month")
    ax.set_ylabel("Sales")

    ax.yaxis.set_major_formatter(FuncFormatter(format_lakhs))

    ax.set_xticks(monthly_analysis["Month"])

    ax.set_xticklabels(monthly_analysis["Month"].dt.strftime("%b"))

    # Add labels to monthly points
    for _, row in monthly_analysis.iterrows():

        ax.annotate(
            f"{row['Total_Sales'] / 100000:.1f}L",
            (row["Month"], row["Total_Sales"]),
            xytext=(0, 8),
            textcoords="offset points",
            ha="center",
            fontsize=8,
        )

    save_chart(fig, "monthly_sales.png")

    # -----------------------------------------------------
    # CHART 2: SALES BY CATEGORY
    # -----------------------------------------------------

    fig, ax = plt.subplots(figsize=(9, 5.5))

    sns.barplot(data=category_analysis, x="Category", y="Total_Sales", ax=ax)

    ax.set_title("Sales by Category", fontweight="bold")

    ax.set_xlabel("Category")
    ax.set_ylabel("Sales")

    ax.yaxis.set_major_formatter(FuncFormatter(format_lakhs))

    ax.tick_params(axis="x", rotation=20)

    add_bar_labels(ax, category_analysis["Total_Sales"].values)

    save_chart(fig, "sales_by_category.png")

    # -----------------------------------------------------
    # CHART 3: SALES BY REGION
    # -----------------------------------------------------

    region_plot = region_analysis.sort_values("Total_Sales", ascending=True)

    fig, ax = plt.subplots(figsize=(8, 5.5))

    sns.barplot(data=region_plot, x="Total_Sales", y="Region", ax=ax)

    ax.set_title("Sales by Region", fontweight="bold")

    ax.set_xlabel("Sales")
    ax.set_ylabel("Region")

    ax.xaxis.set_major_formatter(FuncFormatter(format_lakhs))

    add_bar_labels(ax, region_plot["Total_Sales"].values, horizontal=True)

    save_chart(fig, "sales_by_region.png")

    # -----------------------------------------------------
    # CHART 4: TOP 10 PRODUCTS BY SALES
    # -----------------------------------------------------

    product_sales_plot = top_products_sales.sort_values("Total_Sales", ascending=True)

    fig, ax = plt.subplots(figsize=(10, 6))

    sns.barplot(data=product_sales_plot, x="Total_Sales", y="Product", ax=ax)

    ax.set_title("Top 10 Products by Sales", fontweight="bold")

    ax.set_xlabel("Sales")
    ax.set_ylabel("Product")

    ax.xaxis.set_major_formatter(FuncFormatter(format_lakhs))

    add_bar_labels(ax, product_sales_plot["Total_Sales"].values, horizontal=True)

    save_chart(fig, "top_products.png")

    # -----------------------------------------------------
    # CHART 5: TOP 10 PRODUCTS BY QUANTITY
    # -----------------------------------------------------

    quantity_plot = top_products_quantity.sort_values("Total_Quantity", ascending=True)

    fig, ax = plt.subplots(figsize=(10, 6))

    sns.barplot(data=quantity_plot, x="Total_Quantity", y="Product", ax=ax)

    ax.set_title("Top 10 Products by Quantity Sold", fontweight="bold")

    ax.set_xlabel("Quantity Sold")

    ax.set_ylabel("Product")

    # Add quantity labels
    for bar, value in zip(ax.patches, quantity_plot["Total_Quantity"].values):

        ax.text(
            bar.get_width() + 2,
            bar.get_y() + bar.get_height() / 2,
            f"{int(value)}",
            va="center",
            fontsize=9,
        )

    save_chart(fig, "top_products_by_quantity.png")

    # -----------------------------------------------------
    # CHART 6: SALES BY CUSTOMER SEGMENT
    # -----------------------------------------------------

    fig, ax = plt.subplots(figsize=(8, 5.5))

    sns.barplot(data=segment_analysis, x="Customer_Segment", y="Total_Sales", ax=ax)

    ax.set_title("Sales by Customer Segment", fontweight="bold")

    ax.set_xlabel("Customer Segment")

    ax.set_ylabel("Sales")

    ax.yaxis.set_major_formatter(FuncFormatter(format_lakhs))

    add_bar_labels(ax, segment_analysis["Total_Sales"].values)

    save_chart(fig, "sales_by_customer_segment.png")

    # =====================================================
    # 14. KEY FINDINGS
    # =====================================================

    highest_month = monthly_analysis.loc[monthly_analysis["Total_Sales"].idxmax()]

    lowest_month = monthly_analysis.loc[monthly_analysis["Total_Sales"].idxmin()]

    print("\n" + "=" * 60)
    print("KEY FINDINGS")
    print("=" * 60)

    print(
        f"1. {category_analysis.iloc[0]['Category']} "
        f"had the highest sales among categories "
        f"({category_analysis.iloc[0]['Total_Sales']:,.2f})."
    )

    print(
        f"2. {region_analysis.iloc[0]['Region']} "
        f"had the highest sales among regions "
        f"({region_analysis.iloc[0]['Total_Sales']:,.2f})."
    )

    print(
        f"3. Monthly sales were highest in "
        f"{highest_month['Month'].strftime('%B')} "
        f"({highest_month['Total_Sales']:,.2f}) "
        f"and lowest in "
        f"{lowest_month['Month'].strftime('%B')} "
        f"({lowest_month['Total_Sales']:,.2f})."
    )

    print(
        f"4. {top_products_sales.iloc[0]['Product']} "
        f"was the top product by sales "
        f"({top_products_sales.iloc[0]['Total_Sales']:,.2f})."
    )

    print(
        f"5. The "
        f"{segment_analysis.iloc[0]['Customer_Segment']} "
        f"segment contributed the most sales "
        f"({segment_analysis.iloc[0]['Total_Sales']:,.2f})."
    )

    print(
        f"6. {top_products_quantity.iloc[0]['Product']} "
        f"had the highest quantity sold "
        f"({int(top_products_quantity.iloc[0]['Total_Quantity'])} units)."
    )

    # =====================================================
    # 15. COMPLETION MESSAGE
    # =====================================================

    print("\n" + "=" * 60)
    print("ANALYSIS COMPLETED SUCCESSFULLY")
    print("=" * 60)

    print("\nAll charts have been saved to:")

    print(CHART_DIR)

    print("\nGenerated files:")

    chart_files = [
        "monthly_sales.png",
        "sales_by_category.png",
        "sales_by_region.png",
        "top_products.png",
        "top_products_by_quantity.png",
        "sales_by_customer_segment.png",
    ]

    for chart in chart_files:
        print(f"- {chart}")


# =========================================================
# RUN PROGRAM
# =========================================================

if __name__ == "__main__":
    main()
