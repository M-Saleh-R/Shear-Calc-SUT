import streamlit as st
import base64

# تنظیمات پیکربندی صفحه
st.set_page_config(
    page_title="محاسبه ظرفیت برشی تیر بتنی", 
    page_icon="🏗️", 
    layout="centered"
)

# تابع برای اعمال تصویر پس‌زمینه از فایل لوکال
def set_background(image_file):
    try:
        with open(image_file, "rb") as f:
            encoded_string = base64.b64encode(f.read()).decode()
        st.markdown(
            f"""
            <style>
            .stApp {{
                background-image: url(data:image/jpeg;base64,{encoded_string});
                background-size: cover;
                background-position: center;
                background-attachment: fixed;
            }}
            /* برای خوانایی بهتر متن‌ها روی بک‌گراند */
            .main .block-container {{
                background-color: rgba(255, 255, 255, 0.85);
                border-radius: 10px;
                padding: 2rem;
            }}
            </style>
            """,
            unsafe_allow_html=True
        )
    except FileNotFoundError:
        st.warning("فایل تصویر background.jpeg در مخزن یافت نشد. لطفاً نام و مسیر آن را بررسی کنید.")

# فراخوانی تصویر پس‌زمینه
set_background("background.jpeg")

# عنوان و توضیحات علمی
st.title("محاسبه مقاومت برشی تیر بتنی بدون خاموت")
st.markdown("""
این ابزار بر اساس روابط تجربی وارد شده، ظرفیت برشی نهایی ($V_u$) و فاصله ترک مورب از بر تکیه‌گاه ($a_{cr}$) را ارزیابی می‌کند.
""")
st.latex(r"\frac{V_u}{bd} = 21.7 \rho^{0.363} (f'_c)^{0.249} d^{-0.314} (a/d)^{-0.352}")
st.latex(r"a_{cr} = 0.521 a")

st.markdown("---")
st.subheader("پارامترهای هندسی و مصالح")

# دریافت متغیرها از کاربر
col1, col2 = st.columns(2)

with col1:
    b = st.number_input("عرض مقطع (b) - میلی‌متر", min_value=10.0, value=300.0, step=10.0)
    d = st.number_input("عمق موثر (d) - میلی‌متر", min_value=10.0, value=400.0, step=10.0)
    a = st.number_input("دهانه برشی (a) - میلی‌متر", min_value=10.0, value=1000.0, step=50.0)

with col2:
    fc = st.number_input("مقاومت فشاری بتن (f'c) - مگاپاسکال", min_value=1.0, value=25.0, step=1.0)
    rho = st.number_input("نسبت آرماتور طولی (ρ)", min_value=0.0001, max_value=0.0500, value=0.0150, format="%.4f")

st.markdown("---")

# بلوک محاسبات
if st.button("محاسبه نتایج", type="primary"):
    # محاسبه ترم تنش برشی (Vu / bd)
    # توجه: پارامتر (a/d) باید بدون بعد باشد. 
    a_over_d = a / d
    
    vu_over_bd = (21.7 
                  * (rho ** 0.363) 
                  * (fc ** 0.249) 
                  * (d ** -0.314) 
                  * (a_over_d ** -0.352))
    
    # محاسبه نیروی برشی نهایی (نیوتن) و تبدیل به کیلونیوتن
    # Vu = [Vu/(bd)] * b * d
    vu_newtons = vu_over_bd * b * d
    vu_kn = vu_newtons / 1000.0
    
    # محاسبه فاصله ترک
    a_cr = 0.521 * a
    
    # نمایش خروجی‌ها
    st.subheader("گزارش نتایج:")
    
    col_res1, col_res2 = st.columns(2)
    col_res1.metric(label="ظرفیت برشی نهایی (Vu)", value=f"{vu_kn:.2f} kN")
    col_res2.metric(label="فاصله ترک از تکیه‌گاه (a_cr)", value=f"{a_cr:.2f} mm")
    
    st.info(f"مقدار تنش برشی اسمی محاسبه شده: {vu_over_bd:.3f} MPa")
