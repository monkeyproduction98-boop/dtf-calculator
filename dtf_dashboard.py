import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="DTF Printing Calculator", layout="wide")

st.title("🖨️ DTF Printing Cost Calculator")

# --- Sidebar settings ---
st.sidebar.header("⚙️ Settings")

# Materials cost table
materials_df = pd.DataFrame({
    "Material": ["Film", "Ink", "Powder"],
    "Cost per meter (EGP)": [30, 50, 20]
})
materials = st.sidebar.data_editor(materials_df, num_rows="dynamic")

# Monthly fixed costs
monthly_df = pd.DataFrame({
    "Item": ["Labor", "Electricity", "Monthly Production"],
    "Value": [6000, 2000, 3000]  # EGP and meters
})
monthly = st.sidebar.data_editor(monthly_df, num_rows="dynamic")

# --- User input for design ---
st.subheader("Design Parameters")

x = st.number_input("Enter the design height (meters)", min_value=0.1, step=0.1)
width = 0.6  # fixed 60 cm

# Calculate design area
y = x * width
st.write(f"**Design Area (Y):** {y:.2f} m²")

# Percent of full area (60 * x)
full_area = 60 * x
percent_y = (y / full_area) * 100 if full_area > 0 else 0
st.write(f"**Y percentage of (60 × X):** {percent_y:.2f}%")

# --- Pie chart ---
fig, ax = plt.subplots()
sizes = [y, full_area - y]
colors = ['red', 'limegreen']
labels = ['Design Area (Y)', 'Remaining']

ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
ax.axis('equal')
st.pyplot(fig)

# --- Cost calculations ---
# Materials cost per meter
material_cost_per_m = materials["Cost per meter (EGP)"].sum()

# Monthly costs
labor_cost = float(monthly.loc[monthly["Item"] == "Labor", "Value"])
electricity_cost = float(monthly.loc[monthly["Item"] == "Electricity", "Value"])
monthly_production = float(monthly.loc[monthly["Item"] == "Monthly Production", "Value"])

# Monthly fixed cost per meter
monthly_cost_per_m = (labor_cost + electricity_cost) / monthly_production

# Total cost per meter (standard)
cost_per_m = material_cost_per_m + monthly_cost_per_m

# Cost for the entered design (normalized to 2.5m height)
normalized_design_m = x / 2.5
design_cost = normalized_design_m * cost_per_m

# Cost per real meter for THIS design
cost_per_real_meter = cost_per_m

# --- Display results ---
st.subheader("💰 Cost Results")
st.write(f"**Material cost per meter:** {material_cost_per_m:.2f} EGP")
st.write(f"**Fixed monthly cost per meter:** {monthly_cost_per_m:.2f} EGP")
st.write(f"**Total cost per meter (standard 2.5m):** {cost_per_m:.2f} EGP")
st.write(f"**Total cost for this design (x={x}m):** {design_cost:.2f} EGP")
st.write(f"**Cost per real meter (based on this design):** {cost_per_real_meter:.2f} EGP")
