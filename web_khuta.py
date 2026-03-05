import streamlit as st
import math

# إعدادات الصفحة
st.set_page_config(page_title="تسعير خطى العزم", page_icon="logo.jpeg", layout="centered")

# عرض الشعار
try:
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        st.image("logo.jpeg", use_container_width=True)
except:
    pass

st.markdown("<h1 style='text-align: center;'>مؤسسة خطى العزم للمقاولات</h1>", unsafe_allow_html=True)
st.markdown("---")

# 1. بيانات المشروع
st.header("📋 1. بيانات المشروع")
col1, col2 = st.columns(2)
client_name = col1.text_input("اسم العميل:", "عميل جديد")
profit_margin = col2.number_input("نسبة الربح %:", value=25.0)

shape = st.radio("شكل الخزان:", ["مستطيل", "دائري"])
kashfiya = st.number_input("رسوم المعاينة:", value=100.0)

st.write("**📐 المقاسات:**")
c_depth, c_length, c_width = st.columns(3)
depth = c_depth.number_input("العمق:", value=3.0)
length_dia = c_length.number_input("الطول/القطر:", value=4.0)

if shape == "مستطيل":
    width = c_width.number_input("العرض:", value=4.0)
    area = 2 * (length_dia * depth) + 2 * (width * depth) + (length_dia * width)
else:
    radius = length_dia / 2
    area = (2 * 3.14159 * radius * depth) + (3.14159 * radius**2)

st.info(f"المساحة الإجمالية: {area:.2f} متر مربع")
st.markdown("---")

# 2. التكاليف (التعديل الجديد هنا)
st.header("🛠️ 2. المراحل والتكاليف")

# التنظيف محسوب بالمتر تلقائياً
st.subheader("🧹 مرحلة التنظيف")
clean_m2 = st.number_input("سعر تنظيف المتر الواحد (ريال):", value=7.0)
clean_total = clean_m2 * area

st.subheader("🧪 مرحلة العزل والترميم")
epoxy_m2 = st.number_input("سعر عزل المتر شامل المواد (ريال):", value=45.0)
epoxy_total = epoxy_m2 * area

st.markdown("---")

# 3. الحسابات النهائية
if st.button("احسب التسعيرة النهائية 🚀", type="primary", use_container_width=True):
    total_cost = clean_total + epoxy_total
    profit_factor = 1 + (profit_margin / 100)
    suggested_price = (total_cost * profit_factor) + kashfiya
    
    st.success(f"إجمالي السعر للعميل: {suggested_price:.2f} ريال")
    
    st.code(f"""مؤسسة خطى العزم للمقاولات
عناية العميل: {client_name}
المساحة: {area:.2f} م2
--------------------------------
- التنظيف والتعقيم: {clean_total * profit_factor:.2f} ريال
- أعمال العزل والترميم: {epoxy_total * profit_factor:.2f} ريال
- رسوم المعاينة: {kashfiya:.2f} ريال
--------------------------------
الإجمالي المطلوب: {suggested_price:.2f} ريال""", language="text")
