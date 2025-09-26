import streamlit as st
import pandas as pd
from PIL import Image

st.set_page_config(page_title="DTF File Cost Calculator", layout="wide")

st.title("🎨 DTF File Cost Calculator")

# --- Sidebar for costs ---
st.sidebar.header("💰 Cost Settings")

materials_data = {
    "Item": ["Film Roll (per meter)", "Ink (per ml)", "Powder (per gram)"],
    "Cost": [2.0, 0.05, 0.03]
}
materials_df = pd.DataFrame(materials_data)
materials = st.sidebar.data_editor(materials_df, num_rows="dynamic")

st.sidebar.markdown("---")
st.sidebar.header("⚡ Fixed Monthly Costs")

monthly_costs = {
    "Item": ["Labor", "Electricity", "Monthly Production (meters)"],
    "Cost": [500, 300, 2000]
}
monthly_df = pd.DataFrame(monthly_costs)
monthly = st.sidebar.data_editor(monthly_df, num_rows="dynamic")

# --- Upload file ---
st.header("📂 Upload Your Design")
uploaded_file = st.file_uploader("Choose an image file", type=["png", "jpg", "jpeg", "tif", "tiff"])

if uploaded_file:
    image = Image.open(uploaded_file)
    width, height = image.size  # pixels
    dpi = image.info.get("dpi", (300, 300))[0]

    # Convert to cm (assuming width fixed = 60 cm)
    design_width_cm = 60
    design_height_cm = (height / dpi) * 2.54  # pixels/dpi → inches → cm

    st.success(f"✅ File loaded successfully!")
    st.write(f"**Design height:** {design_height_cm:.2f} cm")
    st.write(f"**Fixed width:** {design_width_cm} cm")

    # --- Coverage input ---
    coverage = st.slider("Printing coverage (%)", 0, 100, 50)
    coverage_area = (coverage / 100) * (design_width_cm * design_height_cm)

    # --- Cost Calculation ---
    film_cost = (design_height_cm / 100) * float(materials.loc[0, "Cost"])  # per meter
    ink_cost = coverage_area * float(materials.loc[1, "Cost"])
    powder_cost = coverage_area * float(materials.loc[2, "Cost"])

    labor_cost = (float(monthly.loc[0, "Cost"]) / float(monthly.loc[2, "Cost"])) * (design_height_cm / 100)
    electricity_cost = (float(monthly.loc[1, "Cost"]) / float(monthly.loc[2, "Cost"])) * (design_height_cm / 100)

    total_cost = film_cost + ink_cost + powder_cost + labor_cost + electricity_cost

    # --- Show table ---
    st.subheader("📊 Cost Breakdown")
    breakdown = pd.DataFrame({
        "Cost Item": ["Film", "Ink", "Powder", "Labor", "Electricity", "TOTAL"],
        "Value ($)": [film_cost, ink_cost, powder_cost, labor_cost, electricity_cost, total_cost]
    })
    st.table(breakdown)
