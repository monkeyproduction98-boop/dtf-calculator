import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# --- Title ---
st.title("DTF Printing Cost Calculator")

# --- Inputs ---
st.header("Design Dimensions")
x = st.number_input("Enter design height (cm):", min_value=1.0, value=100.0, step=1.0)
width = 60.0  # fixed
st.write(f"Width is fixed: {width} cm")

y = st.number_input("Enter printed area (cm²):", min_value=1.0, value=1000.0, step=10.0)

# --- Area Calculations ---
total_area = x * width
printed_percent = (y / total_area) * 100
remaining_area = total_area - y

st.metric("Total Area (cm²)", f"{total_area:.2f}")
st.metric("Printed Area %", f"{printed_percent:.2f}%")

# --- Chart ---
labels = ['Printed Area', 'Remaining']
sizes = [y, remaining_area]
colors = ['red', '#00FF00']  # bright green
fig, ax = plt.subplots()
ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=colors)
ax.axis('equal')
st.pyplot(fig)

# --- Editable Costs Tables ---
st.header("Material & Consumables Prices")
default_materials = {
    "Item": ["Ink", "Film", "Powder"],
    "Price per m²": [2.0, 1.5, 1.0]
}
materials_df = st.data_editor(pd.DataFrame(default_materials), num_rows="dynamic")

st.header("Monthly Fixed Costs")
default_monthly = {
    "Item": ["Labor", "Electricity", "Monthly Meters"],
    "Value": [500.0, 200.0, 1000.0]  # Monthly meters = productivity
}
monthly_df = st.data_editor(pd.DataFrame(default_monthly), num_rows="dynamic")

# --- Cost Calculation ---
st.header("Cost Calculation per 1 Meter")
meters_to_calculate = st.number_input("Meters to calculate (default 1):", min_value=1, value=1)

# Material costs per m²
material_cost_per_m2 = materials_df["Price per m²"].sum()

# Monthly costs distributed per meter
monthly_costs = dict(zip(monthly_df["Item"], monthly_df["Value"]))
labor_cost = monthly_costs.get("Labor", 0)
electricity_cost = monthly_costs.get("Electricity", 0)
monthly_meters = monthly_costs.get("Monthly Meters", 1000)

monthly_cost_per_meter = (labor_cost + electricity_cost) / monthly_meters

# Final cost
cost_per_meter = material_cost_per_m2 + monthly_cost_per_meter
total_cost = cost_per_meter * meters_to_calculate

st.success(f"💰 Cost per meter: {cost_per_meter:.2f}")
st.success(f"💰 Total cost for {meters_to_calculate} meter(s): {total_cost:.2f}")
