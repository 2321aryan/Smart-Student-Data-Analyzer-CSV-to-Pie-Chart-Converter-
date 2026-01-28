import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import io

# -------------------------------------------------
# Page Config
# -------------------------------------------------
st.set_page_config(
    page_title="Smart Student Analyzer",
    layout="centered"
)

st.title("Smart Student Data Analyzer with Pie Charts")

# -------------------------------------------------
# Session State
# -------------------------------------------------
if "df" not in st.session_state:
    st.session_state.df = None

# -------------------------------------------------
# Safe CSV Reader
# -------------------------------------------------
def read_csv_safe(file):
    for enc in ("utf-8", "latin1", "cp1252"):
        try:
            return pd.read_csv(file, encoding=enc)
        except Exception:
            continue
    return None

# -------------------------------------------------
# SMART COLUMN DETECTION
# -------------------------------------------------
def detect_name_column(df):
    keywords = ["name", "student", "candidate", "learner", "person"]
    for col in df.columns:
        if df[col].dtype == "object":
            col_l = col.lower()
            if any(k in col_l for k in keywords):
                return col
    return None

def detect_subject_columns(df):
    ignore_keywords = ["total", "percent", "percentage", "rank", "id", "roll"]
    subjects = []

    for col in df.columns:
        if pd.api.types.is_numeric_dtype(df[col]):
            col_l = col.lower()
            if not any(k in col_l for k in ignore_keywords):
                subjects.append(col)

    return subjects

# -------------------------------------------------
# SMART PIE CHART (Top N + Others)
# -------------------------------------------------
def smart_pie(df, label_col, value_col, top_n, title):
    temp = df[[label_col, value_col]].dropna()
    temp = temp.sort_values(value_col, ascending=False)

    top = temp.head(top_n)
    others_sum = temp.iloc[top_n:][value_col].sum()

    labels = list(top[label_col])
    values = list(top[value_col])

    if others_sum > 0:
        labels.append("Others")
        values.append(others_sum)

    fig, ax = plt.subplots()
    ax.pie(values, labels=labels, autopct="%1.1f%%", startangle=140)
    ax.set_title(title)
    return fig

# -------------------------------------------------
# Upload CSVs
# -------------------------------------------------
files = st.file_uploader(
    "Upload CSV file(s)",
    type=["csv"],
    accept_multiple_files=True
)

if files:
    dfs = []
    for f in files:
        df = read_csv_safe(f)
        if df is not None:
            dfs.append(df)

    if dfs:
        merged = pd.concat(dfs, ignore_index=True, sort=False)
        st.session_state.df = merged
        st.success("Files uploaded & merged successfully")
        st.dataframe(merged.head(10))

# -------------------------------------------------
# MAIN LOGIC
# -------------------------------------------------
if st.session_state.df is not None:
    df = st.session_state.df.copy()

    st.subheader("🔍 Column Detection")

    # ---------- Name Column ----------
    name_col = detect_name_column(df)

    if name_col:
        st.success(f"Detected Student Name Column: {name_col}")
    else:
        st.warning("Student name column not auto-detected")
        name_col = st.selectbox(
            "Select Student Name Column Manually",
            df.columns
        )

    # ---------- Subject Columns ----------
    subject_cols = detect_subject_columns(df)

    if not subject_cols:
        st.error("No subject (numeric) columns detected.")
        st.stop()

    st.success(f"Detected Subject Columns: {', '.join(subject_cols)}")

    # -------------------------------------------------
    # Ranking Logic
    # -------------------------------------------------
    df["Total_Marks"] = df[subject_cols].sum(axis=1)
    max_total = 100 * len(subject_cols)
    df["Percentage"] = (df["Total_Marks"] / max_total) * 100
    df["Percentage"] = df["Percentage"].round(2)
    df["Rank"] = df["Percentage"].rank(ascending=False, method="dense").astype(int)

    # -------------------------------------------------
    # Controls
    # -------------------------------------------------
    st.subheader("🎛 Chart Controls")

    metric_col = st.selectbox(
        "Select Metric for Pie Chart",
        ["Total_Marks"] + subject_cols
    )

    top_n = st.slider("Top N Students", 3, 15, 5)

    # -------------------------------------------------
    # PIE CHART
    # -------------------------------------------------
    st.subheader("🥧 Smart Pie Chart")

    fig = smart_pie(
        df=df,
        label_col=name_col,
        value_col=metric_col,
        top_n=top_n,
        title=f"Top {top_n} Students by {metric_col}"
    )

    st.pyplot(fig)

    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight")
    st.download_button(
        "⬇️ Download Pie Chart",
        buf.getvalue(),
        file_name=f"{metric_col}_pie.png",
        mime="image/png"
    )

    # -------------------------------------------------
    # PASS vs FAIL
    # -------------------------------------------------
    st.subheader("✅ Pass vs ❌ Fail")

    df["Result"] = df["Percentage"].apply(
        lambda x: "Pass" if x >= 40 else "Fail"
    )

    result_count = df["Result"].value_counts()

    fig2, ax2 = plt.subplots()
    ax2.pie(
        result_count,
        labels=result_count.index,
        autopct="%1.1f%%",
        startangle=90
    )
    ax2.set_title("Pass vs Fail Distribution")

    st.pyplot(fig2)

    buf = io.BytesIO()
    fig2.savefig(buf, format="png", bbox_inches="tight")
    st.download_button(
        "⬇️ Download Pass/Fail Chart",
        buf.getvalue(),
        file_name="pass_fail.png",
        mime="image/png"
    )

    # -------------------------------------------------
    # TOP 10 TABLE
    # -------------------------------------------------
    st.subheader("🏆 Top 10 Students")

    top10 = df.sort_values("Rank").head(10)
    st.dataframe(top10[[ "Rank", name_col, "Total_Marks", "Percentage" ] + subject_cols])
