import streamlit as st
import math

# إعدادات الصفحة
st.set_page_config(page_title="تسعير خطى العزم", page_icon="logo.jpeg", layout="centered")

# 1. قسم الترويسة والشعار
try:
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        st.image("logo.jpeg", use_container_width=True)
except:
    pass

st.markdown("<h1 style='text-align: center;'>مؤسسة خطى العزم للمقاولات</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center; color: gray;'>النظام الذكي لتسعير مشاريع العزل</h4>", unsafe_allow_html=True)
st.markdown("---")

# 2. بيانات المشروع والمقاسات
st.header("📋 1. بيانات المشروع والمقاسات")
client_name = st.text_input("اسم العميل:", "عميل جديد")

shape = st.radio("شكل الخزان:", ["مستطيل", "دائري"])

st.write("**📐 مقاسات الخزان (بالمتر):**")
c_depth, c_length, c_width = st.columns(3)
depth = c_depth.number_input("العمق:", value=3.0, step=0.1)
length_dia = c_length.number_input("الطول / القطر:", value=4.0, step=0.1)

if shape == "مستطيل":
    width = c_width.number_input("العرض:", value=4.0, step=0.1)
    area = 2 * (length_dia * depth) + 2 * (width * depth) + (length_dia * width)
else:
    radius = length_dia / 2
    area = (2 * 3.14159 * radius * depth) + (3.14159 * radius**2)

st.info(f"المساحة الإجمالية المحسوبة للخزان: **{area:.2f} متر مربع**")
st.markdown("---")

# 3. المراحل والتكاليف
st.header("🛠️ 2. اختيار المراحل وتفصيل التكاليف")
total_cost = 0  # إجمالي التكلفة المبدئي
client_report = ""
internal_report = ""

# --- المرحلة 1: احسبها صح ---
st.subheader("📏👀 مرحلة 'احسبها صح' (المعاينة والرفع المساحي)")
stage
