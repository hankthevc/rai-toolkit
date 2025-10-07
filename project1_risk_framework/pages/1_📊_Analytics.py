"""Analytics dashboard for governance metrics and trend analysis."""

import json
import sys
from collections import Counter
from datetime import datetime
from pathlib import Path

import altair as alt
import pandas as pd
import streamlit as st

# Add repo root to path for imports
REPO_ROOT = Path(__file__).resolve().parent.parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.append(str(REPO_ROOT))

st.set_page_config(
    page_title="Risk Analytics Dashboard",
    page_icon="📊",
    layout="wide",
)

st.title("Risk Analytics Dashboard")
st.caption(
    "Governance metrics and trends from historical assessments. Demo data only—production deployments should integrate with your ticketing system."
)


@st.cache_data
def load_assessment_data():
    """Load sample assessment data."""
    data_path = REPO_ROOT / "data" / "sample_assessments.json"

    if not data_path.exists():
        st.warning(
            f"Sample data not found at {data_path}. Run `python scripts/generate_sample_data.py` to create demo data."
        )
        return pd.DataFrame()

    with data_path.open() as f:
        data = json.load(f)

    df = pd.DataFrame(data)
    df["date"] = pd.to_datetime(df["date"])
    return df


df = load_assessment_data()

if df.empty:
    st.stop()

# Summary metrics row
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Assessments", len(df))

with col2:
    critical_count = len(df[df["tier"] == "Critical"])
    critical_pct = critical_count / len(df) * 100
    st.metric("Critical Tier", f"{critical_count} ({critical_pct:.1f}%)")

with col3:
    avg_score = df["score"].mean()
    st.metric("Average Risk Score", f"{avg_score:.1f}")

with col4:
    recent_count = len(df[df["date"] >= (datetime.now() - pd.Timedelta(days=30))])
    st.metric("Assessments (Last 30d)", recent_count)

st.markdown("---")

# Risk tier distribution
st.subheader("Risk Tier Distribution")

tier_counts = df["tier"].value_counts().reindex(["Low", "Medium", "High", "Critical"], fill_value=0)
tier_df = tier_counts.reset_index()
tier_df.columns = ["Tier", "Count"]

tier_colors = {
    "Low": "#10b981",  # green
    "Medium": "#f59e0b",  # yellow
    "High": "#f97316",  # orange
    "Critical": "#ef4444",  # red
}

chart1 = (
    alt.Chart(tier_df)
    .mark_bar()
    .encode(
        x=alt.X("Tier:N", sort=["Low", "Medium", "High", "Critical"], axis=alt.Axis(labelAngle=0)),
        y=alt.Y("Count:Q", title="Number of Assessments"),
        color=alt.Color(
            "Tier:N",
            scale=alt.Scale(
                domain=["Low", "Medium", "High", "Critical"],
                range=[tier_colors[t] for t in ["Low", "Medium", "High", "Critical"]],
            ),
            legend=None,
        ),
        tooltip=["Tier", "Count"],
    )
    .properties(height=400)
)

st.altair_chart(chart1, use_container_width=True)

# Two-column layout for additional charts
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("Risk Score Distribution")

    score_chart = (
        alt.Chart(df)
        .mark_bar()
        .encode(
            x=alt.X("score:Q", bin=alt.Bin(maxbins=15), title="Risk Score"),
            y=alt.Y("count():Q", title="Count"),
            color=alt.value("#6366f1"),
            tooltip=["score:Q", "count()"],
        )
        .properties(height=300)
    )

    st.altair_chart(score_chart, use_container_width=True)

with col_right:
    st.subheader("Assessments Over Time")

    # Group by month
    df_monthly = df.copy()
    df_monthly["month"] = df_monthly["date"].dt.to_period("M").dt.to_timestamp()
    monthly_counts = df_monthly.groupby("month").size().reset_index(name="count")

    time_chart = (
        alt.Chart(monthly_counts)
        .mark_line(point=True)
        .encode(
            x=alt.X("month:T", title="Month"),
            y=alt.Y("count:Q", title="Assessments"),
            tooltip=["month:T", "count:Q"],
        )
        .properties(height=300)
    )

    st.altair_chart(time_chart, use_container_width=True)

st.markdown("---")

# Sector analysis
st.subheader("Risk by Sector")

sector_tier = (
    df.groupby(["sector", "tier"])
    .size()
    .reset_index(name="count")
)

sector_chart = (
    alt.Chart(sector_tier)
    .mark_bar()
    .encode(
        x=alt.X("sector:N", title="Sector"),
        y=alt.Y("count:Q", title="Assessments"),
        color=alt.Color(
            "tier:N",
            scale=alt.Scale(
                domain=["Low", "Medium", "High", "Critical"],
                range=[tier_colors[t] for t in ["Low", "Medium", "High", "Critical"]],
            ),
            legend=alt.Legend(title="Risk Tier"),
        ),
        tooltip=["sector", "tier", "count"],
    )
    .properties(height=400)
)

st.altair_chart(sector_chart, use_container_width=True)

# Modifier analysis
st.markdown("---")
st.subheader("Most Common Risk Modifiers")

all_modifiers = []
for modifiers in df["modifiers"]:
    all_modifiers.extend(modifiers)

if all_modifiers:
    modifier_counts = Counter(all_modifiers).most_common()
    modifier_df = pd.DataFrame(modifier_counts, columns=["Modifier", "Count"])

    modifier_chart = (
        alt.Chart(modifier_df)
        .mark_bar()
        .encode(
            x=alt.X("Count:Q"),
            y=alt.Y("Modifier:N", sort="-x"),
            color=alt.value("#8b5cf6"),
            tooltip=["Modifier", "Count"],
        )
        .properties(height=200)
    )

    st.altair_chart(modifier_chart, use_container_width=True)
else:
    st.info("No modifiers recorded in sample data.")

# Control coverage heatmap
st.markdown("---")
st.subheader("Scenario Characteristics Heatmap")

st.caption(
    "Frequency of key risk attributes across all assessments. Helps identify common patterns and coverage gaps."
)

characteristics = pd.DataFrame({
    "Contains PII": [df["contains_pii"].sum(), len(df) - df["contains_pii"].sum()],
    "Customer-Facing": [df["customer_facing"].sum(), len(df) - df["customer_facing"].sum()],
    "High-Stakes": [df["high_stakes"].sum(), len(df) - df["high_stakes"].sum()],
}, index=["Yes", "No"])

st.bar_chart(characteristics)

# Recent assessments table
st.markdown("---")
st.subheader("Recent Assessments")

recent_df = df.nlargest(10, "date")[
    ["date", "scenario", "tier", "score", "owner", "sector"]
].copy()
recent_df["date"] = recent_df["date"].dt.strftime("%Y-%m-%d")

st.dataframe(
    recent_df,
    use_container_width=True,
    hide_index=True,
    column_config={
        "date": "Date",
        "scenario": "Scenario",
        "tier": st.column_config.Column("Risk Tier", width="small"),
        "score": st.column_config.Column("Score", width="small"),
        "owner": "Owner",
        "sector": st.column_config.Column("Sector", width="medium"),
    },
)

# Export option
st.markdown("---")
st.subheader("Data Export")

csv_data = df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="Download Full Dataset (CSV)",
    data=csv_data,
    file_name="risk_assessments.csv",
    mime="text/csv",
    use_container_width=True,
)

st.caption(
    "This dashboard uses sample data for demonstration. Production deployments should connect to your risk management system of record."
)

