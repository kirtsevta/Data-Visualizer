import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title=" Interactive Data Visualizer", layout="wide")

st.markdown(
    """
    <style>
    .main { background-color: #f4f7fa; }
    h1, h2, h3 { color: #2c3e50; }
    </style>
    """, unsafe_allow_html=True
)

# Title
st.title("Interactive Data Visualizer")
st.markdown("Upload a CSV and visualize your data in various chart formats.")

# Sidebar
st.sidebar.title("⚙️ Controls")

# File Upload
uploaded_file = st.sidebar.file_uploader(" Upload your CSV file", type=["csv"])

# Chart Options
chart_type = st.sidebar.selectbox(" Select Chart Type", [
    "Bar Chart", "Line Plot", "Pie Chart", "Scatter Plot", "Histogram"
])

marker_style = st.sidebar.selectbox(" Marker Style (Line/Scatter)", [
    "o (Circle)", "s (Square)", "^ (Triangle)", "* (Star)", "x (Cross)", "d (Diamond)"
])
marker_style = marker_style.split()[0]

marker_color = st.sidebar.selectbox("Default Marker Color", [
    "blue", "red", "green", "orange", "purple", "black", "brown"
])

# DataFrame preview
if uploaded_file:
    try:
        df = pd.read_csv(uploaded_file)
        st.success(" File uploaded successfully!")

        st.subheader(" Data Preview")
        st.dataframe(df.head(), use_container_width=True)

        numeric_cols = df.select_dtypes(include='number').columns.tolist()
        all_cols = df.columns.tolist()

        selected_columns = st.multiselect(" Select Columns for Visualization", all_cols)

        if st.button(" Generate Chart"):
            if chart_type in ["Bar Chart", "Line Plot", "Histogram"] and not selected_columns:
                st.warning("Please select at least one column.")
            elif chart_type == "Scatter Plot" and len(selected_columns) != 2:
                st.warning(" Scatter plot needs exactly 2 numeric columns.")
            elif chart_type == "Pie Chart" and len(selected_columns) != 1:
                st.warning(" Pie chart needs exactly 1 column.")
            else:
                fig, ax = plt.subplots(figsize=(10, 5))

                if chart_type == "Bar Chart":
                    df[selected_columns].sum().plot(kind="bar", ax=ax, color="skyblue", edgecolor="black")
                    ax.set_title("Bar Chart")
                    ax.set_ylabel("Sum")
                    for p in ax.patches:
                        ax.annotate(f'{p.get_height():.2f}', (p.get_x() + p.get_width() / 2, p.get_height()),
                                    ha='center', va='bottom')

                elif chart_type == "Line Plot":
                    colors = plt.cm.tab10.colors  # 10 different colors
                    for i, col in enumerate(selected_columns):
                        color = colors[i % len(colors)]
                        ax.plot(df[col], marker=marker_style, label=col, color=color)
                    ax.set_title("Line Plot")
                    ax.legend()

                elif chart_type == "Pie Chart":
                    counts = df[selected_columns[0]].value_counts()
                    top_counts = counts[:10]
                    others = counts[10:].sum()
                    if others > 0:
                        top_counts["Others"] = others
                    top_counts.plot(kind='pie', autopct='%1.1f%%', ax=ax, label="")
                    ax.set_ylabel("")
                    ax.set_title(f"Pie Chart of {selected_columns[0]}")

                elif chart_type == "Scatter Plot":
                    x, y = selected_columns
                    ax.scatter(df[x], df[y], marker=marker_style, color=marker_color, edgecolors='black')
                    ax.set_xlabel(x)
                    ax.set_ylabel(y)
                    ax.set_title("Scatter Plot")

                elif chart_type == "Histogram":
                    df[selected_columns].plot(kind='hist', bins=30, alpha=0.7, ax=ax, edgecolor='black')
                    ax.set_title("Histogram")
                    ax.legend(title="Columns")

                ax.grid(True, linestyle="--", alpha=0.6)
                st.pyplot(fig)
    except Exception as e:
        st.error(f"Failed to read file: {e}")
else:
    st.info("Please upload a CSV file to begin.")


