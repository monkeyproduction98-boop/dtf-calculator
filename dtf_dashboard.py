import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

# -----------------------------
# 1) Inputs
# -----------------------------
st.title("🖨️ DTF Print Cost Calculator")

# Upload design
uploaded_file = st.file_uploader("📂 Upload your design (PNG / TIF / JPG)", type=["png", "tif", "jpg", "jpeg"])

# Material prices (editable)
st.sidebar.header("⚙️ Material Prices")
ink_price = st.sidebar.number_input("💧 Ink price per liter", value=1350)
film_price = st.sidebar.number_input("📜 Film roll price", value=1800)
powder_price = st.sidebar.number_input("✨ Powder price per kg", value=450)

# Constants
fixed_width_cm = 60  # fixed width = 60 cm
meter_length_cm = 100  # 1 meter = 100 cm

# -----------------------------
# 2) Process image & calculate area
# -----------------------------
if uploaded_file is not None:
    image = Image.open(uploaded_file).convert("RGBA")

    # Estimate height (cm) assuming DPI = 100 px/inch → 39.37 px/cm
    dpi = 100
    px_per_cm = dpi / 2.54
    height_cm = image.height / px_per_cm
    width_cm = image.width / px_per_cm

    # Printed area = non-transparent pixels
    data = np.array(image)
    alpha_channel = data[:, :, 3]  # transparency channel
    printed_pixels = np.sum(alpha_channel > 0)
    total_pixels = alpha_channel.size
    printed_area_cm2 = (printed_pixels / total_pixels) * (fixed_width_cm * height_cm)

    # Coverage ratio
    coverage_ratio = (printed_area_cm2 / (fixed_width_cm * height_cm)) * 100

    # -----------------------------
    # 3) Pie Chart
    # -----------------------------
    labels = ['Printed Area', 'Empty Area']
    values = [printed_area_cm2, (fixed_width_cm * height_cm) - printed_area_cm2]
    colors = ['red', 'green']

    fig, ax = plt.subplots()
    ax.pie(values, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')
    st.pyplot(fig)

    # -----------------------------
    # 4) Cost calculation
    # -----------------------------
    # Film cost per meter (assuming roll = 100m)
    film_cost_per_meter = film_price / 100

    # Powder cost per meter (assume 10g per meter)
    powder_cost_per_meter = powder_price / (1000 / 10)

    base_cost_per_meter = film_cost_per_meter + powder_cost_per_meter

    # Design cost based on reference length = 2.5m
    ref_length_m = 2.5
    ref_area_cm2 = fixed_width_cm * (ref_length_m * 100)  # 2.5m → cm
    design_cost = (printed_area_cm2 / ref_area_cm2) * base_cost_per_meter

    # -----------------------------
    # 5) Results table
    # -----------------------------
    results = pd.DataFrame({
        "Item": ["Design height (cm)", "Printed area (cm²)", "Coverage (%)", "Base cost per meter (EGP)", "Design cost (EGP)"],
        "Value": [round(height_cm, 2), round(printed_area_cm2, 2), round(coverage_ratio, 2), round(base_cost_per_meter, 2), round(design_cost, 2)]
    })

    st.table(results)
