import streamlit as st
from PIL import Image
import pandas as pd

# إعدادات الصفحة
st.set_page_config(page_title="DTF Cost Calculator", page_icon="🎨", layout="wide")

st.title("🎨 DTF Printing Cost Calculator")

# --- إدخال البيانات من المستخدم ---
st.sidebar.header("⚙️ الإعدادات")

ink_price = st.sidebar.number_input("💧 سعر لتر الحبر (جنيه)", value=1350.0, step=50.0)
powder_price = st.sidebar.number_input("🧂 سعر كيلو البودرة (جنيه)", value=450.0, step=10.0)
roll_price = st.sidebar.number_input("📜 سعر رول 100 متر (جنيه)", value=1800.0, step=50.0)
salary_cost = st.sidebar.number_input("👷 المرتبات الشهرية (جنيه)", value=85000.0, step=1000.0)
electricity_cost = st.sidebar.number_input("⚡ تكلفة الكهرباء الشهرية (جنيه)", value=15000.0, step=500.0)
monthly_output = st.sidebar.number_input("🖨️ الإنتاج الشهري (متر)", value=4000, step=100)

coverage = st.sidebar.slider("📏 نسبة التغطية (%)", min_value=1, max_value=100, value=100)

# --- حساب التكلفة ---
ink_cost_per_m = (ink_price / 1000) * (coverage / 100) * 10   # تقدير 10ml لكل متر full cover
powder_cost_per_m = (powder_price / 1000) * 20 * (coverage / 100)  # تقدير 20g لكل متر full cover
roll_cost_per_m = roll_price / 100

fixed_costs_per_m = (salary_cost + electricity_cost) / monthly_output

total_cost_per_m = ink_cost_per_m + powder_cost_per_m + roll_cost_per_m + fixed_costs_per_m

# --- عرض النتائج ---
data = {
    "العنصر": ["🎨 حبر", "🧂 بودرة", "📜 رول", "👷 مرتبات/كهربا", "💰 الإجمالي"],
    "تكلفة للمتر (جنيه)": [
        round(ink_cost_per_m, 2),
        round(powder_cost_per_m, 2),
        round(roll_cost_per_m, 2),
        round(fixed_costs_per_m, 2),
        round(total_cost_per_m, 2)
    ]
}
df = pd.DataFrame(data)

st.subheader("📊 تفاصيل التكلفة")
st.table(df)

st.success(f"✅ التكلفة النهائية للمتر: **{round(total_cost_per_m, 2)} جنيه**")
