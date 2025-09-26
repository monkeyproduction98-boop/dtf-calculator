import streamlit as st
import pandas as pd
from PIL import Image

# ---------------- Sidebar: Editable costs ---------------- #
st.sidebar.header("Cost Settings")

materials_cost = st.sidebar.number_input("Material cost per meter (EGP)", value=18.0, step=0.5)
ink_cost = st.sidebar.number_input("Ink cost per ml (EGP)", value=1.35, step=0.05)
powder_cost = st.sidebar.number_input("Powder cost per gram (EGP)", value=0.45, step=0.05)

labor_monthly = st.sidebar.number_input("Labor monthly cost (EGP)", value=85000.0, step=1000.0)
electricity_monthly = st.sidebar.number_input("Electricity monthly cost (EGP)", value=15000.0, step=1000.0)
monthly_output = st.sidebar.number_input("Monthly production (meters)", value=4000.0, step=100.0)

# ---------------- File Upload ---------------- #
st.title("DTF Printing Cost Calculator")

uploaded_file = st.file_uploader("Upload your design (PNG/TIFF)", type=["png", "tif", "tiff"])
design_height_cm = st.number_input("Enter design height (cm)", value=100.0, step=1.0)
fixed_width_cm = 60.0

if uploaded_file:
    # Open file
    img = Image.open(uploaded_file)

    # Simulate coverage = ratio of non-transparent pixels
    img_rgb = img.convert("RGBA")
    pixels = img_rgb.getdata()
    filled_pixels = sum(1 for p in pixels if p[3] > 0)  # alpha > 0
    coverage_ratio = filled_pixels / len(pixels)
else:
    coverage_ratio = 1.0  # assume full coverage if no file uploaded

# ---------------- Calculations ---------------- #
total_area_cm2 = fixed_width_cm * design_height_cm
printed_area_cm2 = total_area_cm2 * coverage_ratio

# Material cost
material_cost_total = (design_height_cm / 100) * materials_cost

# Ink cost (very simplified: proportional to coverage)
ink_usage_ml = (printed_area_cm2 / 10000) * 2  # 2 ml per 100 cm²
ink_cost_total = ink_usage_ml * ink_cost

# Powder cost
powder_usage_g = (printed_area_cm2 / 10000) * 1.5  # 1.5 g per 100 cm²
powder_cost_total = powder_usage_g * powder_cost

# Labor + electricity (distributed per meter)
overhead_per_meter = (labor_monthly + electricity_monthly) / monthly_output
overhead_total = overhead_per_meter * (design_height_cm / 100)

# Final total
total_cost = material_cost_total + ink_cost_total + powder_cost_total + overhead_total

# ---------------- Display Results ---------------- #
st.subheader("Design Information")
st.write(f"**Design height:** {design_height_cm:.2f} cm")
st.write(f"**Design width (fixed):** {fixed_width_cm} cm")
st.write(f"**Coverage:** {coverage_ratio*100:.1f} %")

st.subheader("Cost Breakdown (EGP)")
cost_data = {
    "Material": [material_cost_total],
    "Ink": [ink_cost_total],
    "Powder": [powder_cost_total],
    "Labor + Electricity": [overhead_total],
    "Total": [total_cost]
}
cost_df = pd.DataFrame(cost_data, index=["Cost"])
st.table(cost_df.style.format("{:.2f}"))
