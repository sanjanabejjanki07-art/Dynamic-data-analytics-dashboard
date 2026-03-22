import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

st.set_page_config(page_title="Dynamic Data Analytics Dashboard", layout="wide")

# ---------------------------
# TITLE
# ---------------------------
st.title("📊 Dynamic Data Analytics Dashboard")

# ---------------------------
# FILE UPLOAD
# ---------------------------
st.sidebar.header("📂 Upload Dataset")

uploaded_file = st.sidebar.file_uploader("Upload CSV", type=["csv"])

# ---------------------------
# LOAD DEFAULT DATA
# ---------------------------
def load_default_data():
    try:
        return pd.read_csv("data.csv")
    except:
        st.error("No default dataset found. Please upload a CSV file.")
        st.stop()

# ---------------------------
# LOAD DATA
# ---------------------------
if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.sidebar.success("✅ Using Uploaded Dataset")
else:
    df = load_default_data()
    st.sidebar.info("📁 Using Default Dataset")

# ---------------------------
# SHOW COLUMNS
# ---------------------------
st.subheader("📄 Dataset Preview")
st.write("Columns:", df.columns.tolist())
st.dataframe(df)

# ---------------------------
# DATA CLEANING
# ---------------------------
st.sidebar.header("⚙ Data Cleaning")

if st.sidebar.checkbox("Remove Null Values"):
    df = df.dropna()

if st.sidebar.checkbox("Remove Duplicates"):
    df = df.drop_duplicates()

# ---------------------------
# COLUMN TYPES
# ---------------------------
numeric_cols = df.select_dtypes(include=np.number).columns.tolist()
categorical_cols = df.select_dtypes(include="object").columns.tolist()

# ---------------------------
# FILTERS
# ---------------------------
st.sidebar.header("🔍 Filters")

if categorical_cols:
    filter_col = st.sidebar.selectbox("Select Column to Filter", categorical_cols)
    values = df[filter_col].dropna().unique()

    selected_values = st.sidebar.multiselect(
        "Select Values", values, default=values[:5]
    )

    filtered_df = df[df[filter_col].isin(selected_values)]
else:
    filtered_df = df

# ---------------------------
# KPI SECTION
# ---------------------------
st.subheader("📊 Key Metrics")

if numeric_cols:
    metric_col = st.selectbox("Select Metric", numeric_cols)

    col1, col2, col3 = st.columns(3)

    col1.metric("Mean", round(filtered_df[metric_col].mean(), 2))
    col2.metric("Max", filtered_df[metric_col].max())
    col3.metric("Min", filtered_df[metric_col].min())
else:
    st.warning("No numeric columns available")

# ---------------------------
# VISUALIZATION SECTION
# ---------------------------
st.subheader("📈 Visualizations")

# Histogram
if numeric_cols:
    selected_num = st.selectbox("Select Numeric Column", numeric_cols)

    fig, ax = plt.subplots()
    sns.histplot(filtered_df[selected_num], kde=True, ax=ax)
    ax.set_title(f"Distribution of {selected_num}")
    st.pyplot(fig)

# Scatter Plot
if len(numeric_cols) >= 2:
    st.subheader("🔹 Scatter Plot")

    x_axis = st.selectbox("X-axis", numeric_cols, key="x")
    y_axis = st.selectbox("Y-axis", numeric_cols, key="y")

    fig, ax = plt.subplots()
    sns.scatterplot(data=filtered_df, x=x_axis, y=y_axis, ax=ax)
    st.pyplot(fig)

# Bar Chart
if categorical_cols:
    st.subheader("🔹 Category Count")

    cat_col = st.selectbox("Categorical Column", categorical_cols)

    fig, ax = plt.subplots()
    filtered_df[cat_col].value_counts().plot(kind="bar", ax=ax)
    st.pyplot(fig)

# Correlation Heatmap
if len(numeric_cols) > 1:
    st.subheader("📊 Correlation Heatmap")

    fig, ax = plt.subplots()
    sns.heatmap(filtered_df[numeric_cols].corr(), annot=True, cmap="coolwarm", ax=ax)
    st.pyplot(fig)

# ---------------------------
# BUSINESS INSIGHTS
# ---------------------------
st.subheader("📌 Insights")

if numeric_cols:
    col = metric_col

    st.write(f"👉 Average {col}: {round(filtered_df[col].mean(),2)}")
    st.write(f"👉 Highest {col}: {filtered_df[col].max()}")
    st.write(f"👉 Lowest {col}: {filtered_df[col].min()}")

    if filtered_df[col].mean() > filtered_df[col].median():
        st.success("Data is slightly skewed towards higher values 📈")
    else:
        st.warning("Data is balanced or skewed lower 📉")

# ---------------------------
# DOWNLOAD
# ---------------------------
st.subheader("⬇ Download Filtered Data")

csv = filtered_df.to_csv(index=False).encode("utf-8")

st.download_button(
    "Download CSV",
    csv,
    "filtered_data.csv",
    "text/csv"
)