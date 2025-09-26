import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np

st.set_page_config(page_title="DTF Cost Calculator", layout="wide")

st.title("🎨 DTF Printing Cost Calculator")

# --- Sidebar tables ---
st.sidebar.header("⚙️ Settings")

# Default material costs
materials_default = {
    "Item": ["Ink (per liter)", "Film roll", "Powder (per kg)"],
    "Price (EGP)": [1350, 1800, 450]
}
materials_df = pd.DataFrame(materials_default)
materials = st.sidebar.data_editor(materials_df, num_rows="dynamic")

# Default monthly costs
monthly_default = {
    "Item": ["Labor (per month)", "Electricity (per month)", "Monthly output (m)"],
    "Value": [85000, 15000, 4000]
}
monthly_df = pd.DataFrame(monthly_default)
monthly = st.sidebar.data_editor(monthly_df, num_rows="dynamic")

# --- File upload ---
st.subheader("📂 Upload your design file")
uploaded_file = st.file_uploader("Choose a PNG/TIF file", type=["png", "tif", "tiff"])

# --- Inputs ---
col1, col2 = st.columns(2)
with col1:
    x = st.number_input("Design height (cm)", min_value=1.0, value=100.0)
with col2:
    y = st.number_input("Printed area (cm²)", min_value=1.0, value=2000.0)

width = 60.0  # fixed width
total_area = width * x
coverage_pct = (y / total_area) * 100

# --- Pie chart ---
st.subheader("📊 Coverage Chart")
fig, ax = plt.subplots()
sizes = [y, total_area - y]
colors = ['red', 'lime']  # red for printed, bright green for empty
labels = ['Printed area', 'Empty area']
ax.pie(sizes, labels=labels, autopct='%1.1f%%', colors=colors, startangle=90)
ax.axis('equal')
st.pyplot(fig)

# --- Cost calculation ---
st.subheader("💰 Cost Calculation")

# Extract values
ink_price = float(materials.loc[materials["Item"] == "Ink (per liter)", "Price (EGP)"].values[0])
film_price = float(materials.loc[materials["Item"] == "Film roll", "Price (EGP)"].values[0])
powder_price = float(materials.loc[materials["Item"] == "Powder (per kg)", "Price (EGP)"].values[0])

labor_cost = float(monthly.loc[monthly["Item"] == "Labor (per month)", "Value"].values[0])
electricity_cost = float(monthly.loc[monthly["Item"] == "Electricity (per month)", "Value"].values[0])
monthly_output = float(monthly.loc[monthly["Item"] == "Monthly output (m)", "Value"].values[0])

# Base material cost (rough assumption per meter full coverage)
ink_cost_per_m = ink_price / 1000 * 10  # assume 10 ml/m
film_cost_per_m = film_price / 100  # assume 100m roll
powder_cost_per_m = powder_price / 50  # assume 50m/kg

material_cost_per_m = ink_cost_per_m + film_cost_per_m + powder_cost_per_m

# Monthly costs per meter
monthly_cost_per_m = (labor_cost + electricity_cost) / monthly_output

# Adjusted cost per design
factor = x / 250  # because x=2.5m considered 1 full meter
final_cost = (material_cost_per_m + monthly_cost_per_m) * factor

st.write(f"**Coverage %:** {coverage_pct:.2f}%")
st.write(f"**Material cost per meter:** {material_cost_per_m:.2f} EGP")
st.write(f"**Monthly cost per meter:** {monthly_cost_per_m:.2f} EGP")
st.write(f"**Total cost for this design (x={x}cm):** {final_cost:.2f} EGP")
