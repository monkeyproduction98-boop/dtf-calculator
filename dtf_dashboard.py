import streamlit as st
import pandas as pd
from PIL import Image

st.set_page_config(page_title="DTF File Cost Calculator", layout="wide")

st.title("🎨 DTF File Cost Calculator")

# --- Sidebar for costs ---
st.sidebar.header("💰 Cost Settings")

materials_data = {
    "Item": ["Film Roll (per meter)", "Ink (per liter)", "Powder (per kg)"],
    "Cost": [1800 / 100, 1350, 450]
}
materials_df = pd.DataFrame(materials_data)
materials = st.sidebar.data_editor(materials_df, num_rows="dynamic")

st.sidebar.markdown("---")
st.sidebar.header("⚡ Fixed Monthly Costs")

monthly_costs = {
    "Item": ["Labor", "Electricity", "Monthly Production (meters)"],
    "Cost": [85000, 15000, 4000]
}
monthly_df = pd.DataFrame(monthly_costs)
monthly = st.sidebar.data_editor(monthly_df, num_rows="dynamic")

st.sidebar.markdown("---")
st.sidebar.header("🖨️ Consumption Settings (per m²)")
ink_consumption = st.sidebar.number_input("Ink consumption (ml/m²)", value=20.0)
powder_consumption = st.sidebar.number_input("Powder consumption (g/m²)", value=15.0)

# --- Upload file ---
st.header("📂 Upload Your Design")
uploaded_file = st.file_uploader("Choose an image file", type=["png", "jpg", "jpeg", "tif", "tiff"])

if uploaded_file:
    image = Image.open(uploaded_file)
    width, height = image.size  # pixels
    dpi = image.info.get("dpi", (300, 300))[0]

    # Calculate height from DPI
    design_width_cm = 60  # fixed width
    auto_height_cm = (height / dpi) * 2.54  # pixels/dpi → inches → cm

    # Manual override
    manual_height_cm = st.number_input("Manual height (cm)", value=float(auto_height_cm))

    # Coverage input
    coverage = st.slider("Printing coverage (%)", 0, 100, 50)

    # Effective area (m²)
    effective_area_m2 = (design_width_cm / 100) * (manual_height_cm / 100) * (coverage / 100)

    # --- Costs ---
    film_cost = (manual_height_cm / 100) * float(materials.loc[0, "Cost"])  # film cost per meter
    ink_cost = effective_area_m2 * ink_consumption * (materials.loc[1, "Cost"] / 1000)  # convert L → ml
    powder_cost = effective_area_m2 * powder_consumption * (materials.loc[2, "Cost"] / 1000)  # convert kg → g

    labor_cost = (float(monthly.loc[0, "Cost"]) / float(monthly.loc[2, "Cost"])) * (manual_height_cm / 100)
    electricity_cost = (float(monthly.loc[1, "Cost"]) / float(monthly.loc[2, "Cost"])) * (manual_height_cm / 100)

    total_cost = film_cost + ink_cost + powder_cost + labor_cost + electricity_cost

    # --- Show results ---
    st.success("✅ File processed successfully!")
    st.write(f"**Auto height from file:** {auto_height_cm:.2f} cm")
    st.write(f"**Manual height used:** {manual_height_cm:.2f} cm")
    st.write(f"**Effective print area:** {effective_area_m2:.2f} m²")

    st.subheader("📊 Cost Breakdown")
    breakdown = pd.DataFrame({
        "Cost Item": ["Film", "Ink", "Powder", "Labor", "Electricity", "TOTAL"],
        "Value (EGP)": [film_cost, ink_cost, powder_cost, labor_cost, electricity_cost, total_cost]
    })
    st.table(breakdown)
