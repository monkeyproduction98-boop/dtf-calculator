import streamlit as st
import pandas as pd

st.set_page_config(page_title="DTF Cost Calculator", layout="wide")

st.title("🎨 DTF Printing Cost Calculator")

# --- Sidebar pricing ---
st.sidebar.header("⚙️ Pricing Settings")

materials_data = {
    "Material": ["Film", "Ink", "Powder"],
    "Cost per m² ($)": [0.5, 1.2, 0.3],
}
materials_df = pd.DataFrame(materials_data)
materials = st.sidebar.data_editor(materials_df, num_rows="dynamic")

monthly_data = {
    "Item": ["Labor", "Electricity", "Monthly Output (m²)"],
    "Value": [300, 200, 500],
}
monthly_df = pd.DataFrame(monthly_data)
monthly = st.sidebar.data_editor(monthly_df, num_rows="dynamic")

# --- Upload file ---
st.header("📂 Upload Design File")
uploaded_file = st.file_uploader("Upload your design file", type=["png", "jpg", "jpeg", "pdf"])

manual_height_cm = st.number_input("Enter design height (cm)", min_value=10, max_value=500, value=100)
design_width_cm = 60  # fixed width
coverage = st.slider("Estimated coverage (%)", 10, 100, 80)

# --- Calculations ---
if manual_height_cm:
    # total design area (m²)
    total_area_m2 = (design_width_cm / 100) * (manual_height_cm / 100)

    # effective printed area (m²)
    effective_area_m2 = total_area_m2 * (coverage / 100)

    # print coverage %
    print_percentage = (effective_area_m2 / total_area_m2) * 100

    # material costs
    material_cost = 0
    for _, row in materials.iterrows():
        material_cost += row["Cost per m² ($)"] * effective_area_m2

    # monthly costs
    labor_cost = float(monthly.loc[monthly["Item"] == "Labor", "Value"])
    electricity_cost = float(monthly.loc[monthly["Item"] == "Electricity", "Value"])
    monthly_output = float(monthly.loc[monthly["Item"] == "Monthly Output (m²)", "Value"])

    overhead_per_m2 = (labor_cost + electricity_cost) / monthly_output
    total_cost = material_cost + (overhead_per_m2 * effective_area_m2)

    # --- Results ---
    st.header("📊 Results")
    st.write(f"**Total design area:** {total_area_m2:.2f} m²")
    st.write(f"**Effective print area:** {effective_area_m2:.2f} m²")
    st.write(f"**Print coverage:** {print_percentage:.1f}%")
    st.write(f"**Material cost:** ${material_cost:.2f}")
    st.write(f"**Overhead per m²:** ${overhead_per_m2:.2f}")
    st.write(f"**Total cost for this file:** ${total_cost:.2f}")
