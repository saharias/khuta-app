import streamlit as st
import math

# إعدادات الصفحة (استبدلنا إيموجي الرافعة باسم ملف الشعار عشان يطلع في علامة التبويب فوق)
st.set_page_config(page_title="تسعير خطى العزم", page_icon="logo.jpeg", layout="centered")

# 1. قسم الترويسة والشعار (بتوسيط احترافي)
try:
    # استخدمنا الأعمدة عشان نوسط الشعار في نص الشاشة بالضبط
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        st.image("logo.jpeg", use_container_width=True)
except:
    st.warning("⚠️ لم يتم العثور على صورة الشعار. تأكد من تسميتها 'logo.jpeg' ووضعها في سطح المكتب.")

# العنوان بدون الإيموجي وبتوسيط فخم
st.markdown("<h1 style='text-align: center;'>مؤسسة خطى العزم للمقاولات</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center; color: gray;'>النظام الذكي لتسعير مشاريع العزل</h4>", unsafe_allow_html=True)
st.markdown("---")

# 2. بيانات المشروع
st.header("📋 1. بيانات المشروع")
col1, col2 = st.columns(2)
client_name = col1.text_input("اسم العميل:", "عميل جديد")
profit_margin = col2.number_input("نسبة هامش الربح %:", value=25.0, step=1.0)

col3, col4 = st.columns(2)
shape = col3.radio("شكل الخزان:", ["مستطيل", "دائري"])
kashfiya = col4.number_input("رسوم المعاينة والكشفية:", value=100.0, step=10.0)

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

# 3. التكاليف والمراحل
st.header("🛠️ 2. المراحل المطلوبة والتكاليف")

stage1 = st.checkbox("☑ التنظيف والتعقيم", value=True)
if stage1:
    c1, c2 = st.columns(2)
    clean_mat = c1.number_input("مواد التنظيف (مقطوعية):", value=150.0, step=10.0)
    clean_lab = c2.number_input("عمالة التنظيف:", value=200.0, step=10.0)

stage2 = st.checkbox("☑ الترميم والتعشيش", value=True)
if stage2:
    c1, c2, c3 = st.columns(3)
    sika_cov = c1.number_input("تغطية كيس السيكا (م2):", value=20.0)
    sika_pr = c2.number_input("سعر كيس السيكا:", value=45.0)
    sika_lab = c3.number_input("عمالة التعشيش:", value=300.0)

stage3 = st.checkbox("☑ التلييس", value=True)
if stage3:
    c1, c2, c3, c4 = st.columns(4)
    cem_cov = c1.number_input("تغطية كيس الأسمنت (م2):", value=5.0)
    cem_pr = c2.number_input("سعر كيس الأسمنت:", value=17.0)
    sand_cost = c3.number_input("تكلفة البطحاء:", value=150.0)
    cem_lab = c4.number_input("عمالة التلييس:", value=400.0)

stage4 = st.checkbox("☑ العزل الإيبوكسي", value=True)
if stage4:
    c1, c2, c3, c4 = st.columns(4)
    epoxy_cov = c1.number_input("تغطية البرميل (م2):", value=35.0)
    epoxy_pr = c2.number_input("سعر البرميل:", value=350.0)
    epoxy_lab = c3.number_input("عمالة العزل:", value=500.0)
    tools = c4.number_input("أدوات أخرى:", value=100.0)

st.markdown("---")

# 4. الحسابات
if st.button("احسب التسعيرة النهائية 🚀", type="primary", use_container_width=True):
    total_cost = 0
    profit_factor = 1 + (profit_margin / 100)
    client_report = ""
    internal_report = ""

    if stage1:
        cost1 = clean_mat + clean_lab
        total_cost += cost1
        client_report += f"- التنظيف والتعقيم: {cost1 * profit_factor:.2f} ريال\n"
        internal_report += f"- تنظيف: التكلفة الفعلية {cost1:.2f} ريال\n"
        
    if stage2:
        qty_sika = math.ceil(area / sika_cov) if sika_cov > 0 else 0
        cost2 = (qty_sika * sika_pr) + sika_lab
        total_cost += cost2
        client_report += f"- معالجة التشققات والتعشيش: {cost2 * profit_factor:.2f} ريال\n"
        internal_report += f"- تعشيش ({qty_sika} كيس): التكلفة الفعلية {cost2:.2f} ريال\n"
        
    if stage3:
        qty_cem = math.ceil(area / cem_cov) if cem_cov > 0 else 0
        cost3 = (qty_cem * cem_pr) + sand_cost + cem_lab
        total_cost += cost3
        client_report += f"- طبقة التلييس والترميم: {cost3 * profit_factor:.2f} ريال\n"
        internal_report += f"- تلييس ({qty_cem} كيس): التكلفة الفعلية {cost3:.2f} ريال\n"
        
    if stage4:
        qty_epoxy = math.ceil(area / epoxy_cov) if epoxy_cov > 0 else 0
        cost4 = (qty_epoxy * epoxy_pr) + tools + epoxy_lab
        total_cost += cost4
        client_report += f"- العزل الأساسي (إيبوكسي): {cost4 * profit_factor:.2f} ريال\n"
        internal_report += f"- عزل ({qty_epoxy} برميل): التكلفة الفعلية {cost4:.2f} ريال\n"

    suggested_price = (total_cost * profit_factor) + kashfiya
    net_profit = suggested_price - total_cost - kashfiya
    price_per_meter = suggested_price / area if area > 0 else 0

    # عرض النتائج في شكل تبويبات (Tabs)
    tab1, tab2 = st.tabs(["⭐⭐⭐ عرض سعر العميل", "🔒 تقرير الإدارة السري"])
    
    with tab1:
        st.success("جاهز للنسخ والمشاركة مع العميل")
        st.code(f"""مؤسسة خطى العزم للمقاولات
عناية العميل المكرّم: {client_name}

بناءً على المعاينة، نرفق لكم تفاصيل تسعيرة أعمال العزل:
- المساحة الإجمالية للخزان: {area:.2f} متر مربع

تفصيل تكلفة المراحل المطلوبة:
--------------------------------
{client_report}- رسوم المعاينة والكشفية: {kashfiya:.2f} ريال
--------------------------------
💎 الإجمالي الكلي المطلوب: {suggested_price:.2f} ريال
💰 تكلفة المتر المربع: {price_per_meter:.2f} ريال/م2
================================""", language="text")
        
    with tab2:
        st.warning("هذا التقرير لك فقط ولا يشارك مع العميل")
        st.write(f"**إجمالي التكلفة التشغيلية:** {total_cost:.2f} ريال")
        st.write(f"**صافي الربح المتوقع:** {net_profit:.2f} ريال")
        st.code(internal_report, language="text")