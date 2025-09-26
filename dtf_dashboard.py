import streamlit as st
import pandas as pd
from PIL import Image
import numpy as np

st.set_page_config(page_title="DTF Ink Usage Calculator", layout="wide")

st.title("🎨 DTF Ink Usage Calculator")

# --- Upload image ---
uploaded_file = st.file_uploader("📂 Upload your design (PNG or JPG)", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    # فتح الصورة
    image = Image.open(uploaded_file).convert("CMYK")
    st.image(image, caption="Your uploaded design", use_container_width=True)

    # تحويل الصورة لمصفوفة
    img_array = np.array(image)

    # فصل القنوات (C, M, Y, K)
    C, M, Y, K = img_array[:,:,0], img_array[:,:,1], img_array[:,:,2], img_array[:,:,3]

    # حساب المتوسط لكل قناة
    coverage = {
        "Cyan (C)": np.mean(C) / 255 * 100,
        "Magenta (M)": np.mean(M) / 255 * 100,
        "Yellow (Y)": np.mean(Y) / 255 * 100,
        "Black (K)": np.mean(K) / 255 * 100,
    }

    df = pd.DataFrame(list(coverage.items()), columns=["Ink", "Coverage %"])
    st.subheader("📊 Ink Coverage Results")
    st.dataframe(df, use_container_width=True)

    # زرار حفظ النتائج
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button("💾 Download results (CSV)", csv, "ink_coverage.csv", "text/csv")
else:
    st.info("⬆️ Please upload a design image to start calculation.")
