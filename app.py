import streamlit as st
import pandas as pd
import plotly.express as px

from database import create_table, insert_data, fetch_data
from forecasting import forecast_sales

st.set_page_config(page_title="Sales Analytics Dashboard", layout="wide")

st.title("📊 Sales Analytics & Forecasting System")

create_table()

uploaded_file = st.file_uploader("Upload Sales File", type=["csv", "xlsx"])

if uploaded_file is not None:

    try:

        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)

        # Column names clean karna
        df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

        st.write("Detected Columns:")
        st.write(df.columns.tolist())

        required_columns = [
            "order_id",
            "order_date",
            "product",
            "category",
            "region",
            "quantity",
            "unit_price",
            "revenue",
        ]

        missing = [col for col in required_columns if col not in df.columns]

        if missing:
            st.error(f"Missing Columns: {missing}")
            st.stop()

        insert_data(df)

        st.success("Data Uploaded Successfully")

        data = fetch_data()

        data["order_date"] = pd.to_datetime(data["order_date"])

        # KPI SECTION

        total_revenue = data["revenue"].sum()

        total_orders = data["order_id"].nunique()

        avg_order_value = total_revenue / total_orders

        total_quantity = data["quantity"].sum()

        col1, col2, col3, col4 = st.columns(4)

        col1.metric("Revenue", f"₹{total_revenue:,.0f}")

        col2.metric("Orders", total_orders)

        col3.metric("Avg Order Value", f"₹{avg_order_value:,.0f}")

        col4.metric("Units Sold", total_quantity)

        st.divider()

        # MONTHLY REVENUE

        st.subheader("Monthly Revenue Trend")

        monthly = (
            data.groupby(pd.Grouper(key="order_date", freq="ME"))["revenue"]
            .sum()
            .reset_index()
        )

        fig1 = px.line(monthly, x="order_date", y="revenue", markers=True)

        st.plotly_chart(fig1, use_container_width=True)

        # TOP PRODUCTS

        st.subheader("Top Products")

        top_products = (
            data.groupby("product")["revenue"]
            .sum()
            .sort_values(ascending=False)
            .head(10)
            .reset_index()
        )

        fig2 = px.bar(top_products, x="product", y="revenue")

        st.plotly_chart(fig2, use_container_width=True)

        # REGION ANALYSIS

        st.subheader("Region-wise Revenue")

        region_sales = data.groupby("region")["revenue"].sum().reset_index()

        fig3 = px.pie(region_sales, names="region", values="revenue")

        st.plotly_chart(fig3, use_container_width=True)

        # FORECAST

        st.subheader("Sales Forecast")

        predictions = forecast_sales(data)

        forecast_df = pd.DataFrame(
            {
                "Month": ["Month 1", "Month 2", "Month 3"],
                "Predicted Revenue": predictions,
            }
        )

        fig4 = px.bar(forecast_df, x="Month", y="Predicted Revenue")

        st.plotly_chart(fig4, use_container_width=True)

        # RAW DATA

        st.subheader("Raw Data")

        st.dataframe(data)

    except Exception as e:

        st.error(str(e))
