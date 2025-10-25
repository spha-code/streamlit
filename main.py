import streamlit as st
import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
import plotly.express as px

#Comment

st.set_page_config(page_title="📊 Cryptocurrency Dashboard", page_icon="💰", layout="wide")

# ---------- Load CSV ----------
csv_path = os.path.join("csv", "cryptocurrency.csv")

try:
    df = pd.read_csv(csv_path)
    st.sidebar.success("✅ CSV file loaded successfully!")

    # ---------- Clean and convert numeric columns ----------
    for col in df.columns:
        # Remove commas, $, %, and spaces
        df[col] = (
            df[col]
            .astype(str)
            .str.replace(",", "", regex=False)
            .str.replace("$", "", regex=False)
            .str.replace("%", "", regex=False)
            .str.strip()
        )

        # Try to convert to numeric where possible
        df[col] = pd.to_numeric(df[col], errors="ignore")

    # ---------- Detect numeric columns ----------
    numeric_cols = df.select_dtypes(include=["float64", "int64"]).columns.tolist()

    st.title("💹 Cryptocurrency Analytics Dashboard")

    st.subheader("Hourly crypto & stock data, updated hourly — unlock insights, trends & forecasts")
    st.subheader("source: https://www.kaggle.com/datasets/adrianjuliusaluoch/hourly-crypto-stocks-market-data")

    # ---------- Summary Metrics ----------
    col1, col2, col3 = st.columns(3)

    # Average Price
    if "price" in df.columns and pd.api.types.is_numeric_dtype(df["price"]):
        col1.metric("Average Price", f"${df['price'].mean():,.2f}")
    else:
        col1.metric("Average Price", "N/A")

    # Total Market Cap
    if "market_cap" in df.columns and pd.api.types.is_numeric_dtype(df["market_cap"]):
        col2.metric("Total Market Cap", f"${df['market_cap'].sum():,.0f}")
    else:
        col2.metric("Total Market Cap", "N/A")

    # 24h Volume
    if "volume_24h" in df.columns and pd.api.types.is_numeric_dtype(df["volume_24h"]):
        col3.metric("Total 24h Volume", f"${df['volume_24h'].sum():,.0f}")
    else:
        col3.metric("Total 24h Volume", "N/A")

    st.markdown("---")

    # ---------- Data Table ----------
    st.subheader("📄 Data Preview")
    # Pandas df
    st.dataframe(df, use_container_width=True)

    st.write("### Columns:")
    st.write(df.columns.tolist())  # as a list

    # Or display one per line
    st.text("Columns:")
    for col in df.columns:
        st.text(f"- {col}")

    # ---------- Example Visualization ----------
    if "market_cap" in df.columns and "name" in df.columns and pd.api.types.is_numeric_dtype(df["market_cap"]):
        fig = px.bar(
            df.sort_values("market_cap", ascending=False).head(20),
            x="name",
            y="market_cap",
            color="market_cap",
            title="Top 20 Cryptocurrencies by Market Cap",
            height=500
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # ---------- Metrics ----------
    st.subheader("Metrics")
    st.metric(label="Total Rows", value=len(df))

    # ---------- Charts ----------
    st.subheader("Area Chart")
    
    chart_data = pd.DataFrame(
        np.random.randn(20,3),
        columns  =['name','symbol','price_usd']
    ) 

    st.subheader("Bar Chart")
    st.bar_chart(chart_data)

    st.subheader("Line Chart")
    st.line_chart(chart_data)

    #st.subheader("PyPlot Chart")
    #st.pyplot(fig)

except FileNotFoundError:
    st.error(f"❌ File not found at: {csv_path}")
