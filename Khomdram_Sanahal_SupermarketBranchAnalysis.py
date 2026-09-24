"""Supermarket Branch Performance Analysis dashboard.
Run: streamlit run Khomdram_Sanahal_SupermarketBranchAnalysis.py
"""
from pathlib import Path
import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Supermarket Branch Performance Analysis", page_icon="🛒", layout="wide")
DATA_PATH = Path(__file__).resolve().parent / "data" / "supermarket_sales_500_rows.csv"
@st.cache_data
def load_data():
    data = pd.read_csv(DATA_PATH)
    data["Date"] = pd.to_datetime(data["Date"])
    data["Month"] = data["Date"].dt.to_period("M").astype(str)
    return data
df = load_data()
st.title("Supermarket Branch Performance Analysis")
st.caption("Data Analytics Project | 500 supplied supermarket transactions")
st.header("Branch and City Performance")
branch = st.multiselect("Branch", sorted(df.Branch.unique()), default=sorted(df.Branch.unique()))
if not branch:
    st.warning("Select at least one branch to see the analysis.")
    st.stop()
view = df[df.Branch.isin(branch)]
summary = view.groupby(["Branch", "City"], as_index=False).Sales.sum().sort_values("Sales", ascending=False)
monthly = view.groupby(["Month", "Branch"], as_index=False).Sales.sum()
c1,c2,c3,c4=st.columns(4)
c1.metric("Total Sales", f"₹{view.Sales.sum():,.2f}")
c2.metric("Orders", len(view))
c3.metric("Best Branch", summary.iloc[0].Branch)
c4.metric("Best City", summary.iloc[0].City)
left,right=st.columns(2)
left.plotly_chart(px.bar(summary,x="City",y="Sales",color="Branch",title="Sales by Branch"),use_container_width=True)
right.plotly_chart(px.line(monthly,x="Month",y="Sales",color="Branch",markers=True,title="Monthly Sales by Branch"),use_container_width=True)
st.subheader("Recommended Actions")
st.markdown("- Study Branch C Mumbai's product mix and operations.\n- Set improvement targets for lower-sales branches.\n- Plan inventory and staffing around monthly sales patterns.")
