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

# حصالات لتجميع التكاليف وتصنيفها للإدارة
total_cost = 0
total_materials = 0
total_labor = 0
total_other = 0

# --- المرحلة 1: احسبها صح ---
st.subheader("📏👀 مرحلة 'احسبها صح' (المعاينة والرفع المساحي)")
stage1 = st.checkbox("تفعيل رسوم المعاينة", value=True)
cost_stage1 = 0
if stage1:
    kashfiya = st.number_input("رسوم المعاينة والكشفية:", value=100.0, step=10.0)
    cost_stage1 = kashfiya
    total_cost += cost_stage1
st.markdown("---")

# --- المرحلة 2: التصفية ---
st.subheader("🧼🫧 مرحلة 'التصفية' (الغسيل والتعقيم وإزالة الرواسب)")
stage2 = st.checkbox("تفعيل مرحلة التصفية", value=True)
cost_stage2 = 0
if stage2:
    st.write("خيارات التكلفة:")
    c1, c2, c3 = st.columns(3)
    opt_cl_m2 = c1.checkbox("حساب بالمتر", value=True)
    opt_cl_lab = c2.checkbox("عمالة مقطوعة")
    opt_cl_tool = c3.checkbox("أدوات ومواد")
    
    cl_m2_cost = cl_lab_cost = cl_tool_cost = 0
    if opt_cl_m2: 
        cl_m2_cost = st.number_input("سعر تنظيف المتر:", value=7.0) * area
        total_other += cl_m2_cost
    if opt_cl_lab: 
        cl_lab_cost = st.number_input("تكلفة عمالة التنظيف:", value=150.0)
        total_labor += cl_lab_cost
    if opt_cl_tool: 
        cl_tool_cost = st.number_input("تكلفة مواد التنظيف:", value=100.0)
        total_materials += cl_tool_cost
        
    cost_stage2 = cl_m2_cost + cl_lab_cost + cl_tool_cost
    total_cost += cost_stage2
    st.caption(f"إجمالي تكلفة هذه المرحلة: {cost_stage2:.2f} ريال")
st.markdown("---")

# --- المرحلة 3: التجديد ---
st.subheader("🧱🩹 مرحلة 'التجديد' (معالجة التعشيش والترميم)")
stage3 = st.checkbox("تفعيل مرحلة التجديد", value=True)
cost_stage3 = 0
if stage3:
    st.write("**التعشيش:**")
    c1, c2 = st.columns(2)
    opt_sika = c1.checkbox("مواد السيكا", value=True)
    opt_sika_lab = c2.checkbox("عمالة التعشيش", value=True)
    
    sika_cost = sika_lab_cost = 0
    if opt_sika:
        c_cov, c_pr = st.columns(2)
        sika_cov = c_cov.number_input("تغطية كيس السيكا (م2):", value=20.0)
        sika_pr = c_pr.number_input("سعر كيس السيكا:", value=45.0)
        qty_sika = math.ceil(area / sika_cov) if sika_cov > 0 else 0
        sika_cost = qty_sika * sika_pr
        st.info(f"📦 عدد أكياس السيكا المطلوبة: **{qty_sika} كيس**")
        total_materials += sika_cost
    if opt_sika_lab:
        sika_lab_cost = st.number_input("حساب عمالة التعشيش:", value=300.0)
        total_labor += sika_lab_cost
        
    st.write("**التلييس:**")
    c3, c4 = st.columns(2)
    opt_cem = c3.checkbox("أسمنت وبطحاء", value=True)
    opt_cem_lab = c4.checkbox("عمالة التلييس", value=True)
    
    cem_cost = cem_lab_cost = 0
    if opt_cem:
        c_cov2, c_pr2, c_sand = st.columns(3)
        cem_cov = c_cov2.number_input("تغطية كيس الأسمنت (م2):", value=5.0)
        cem_pr = c_pr2.number_input("سعر كيس الأسمنت:", value=17.0)
        sand_cost = c_sand.number_input("تكلفة البطحاء:", value=150.0)
        qty_cem = math.ceil(area / cem_cov) if cem_cov > 0 else 0
        cem_cost = (qty_cem * cem_pr) + sand_cost
        st.info(f"📦 عدد أكياس الأسمنت المطلوبة: **{qty_cem} كيس**")
        total_materials += cem_cost
    if opt_cem_lab:
        cem_lab_cost = st.number_input("حساب عمالة التلييس:", value=400.0)
        total_labor += cem_lab_cost
        
    cost_stage3 = sika_cost + sika_lab_cost + cem_cost + cem_lab_cost
    total_cost += cost_stage3
    st.caption(f"إجمالي تكلفة هذه المرحلة: {cost_stage3:.2f} ريال")
st.markdown("---")

# --- المرحلة 4: ازهلها ---
st.subheader("🛡️🔑 مرحلة 'ازهلها' (الحل المتكامل - توريد وتنفيذ)")
stage4 = st.checkbox("تفعيل مرحلة ازهلها", value=True)
cost_stage4 = 0
if stage4:
    c1, c2, c3 = st.columns(3)
    opt_epoxy = c1.checkbox("مواد العزل", value=True)
    opt_epoxy_lab = c2.checkbox("عمالة العزل", value=True)
    opt_epoxy_tool = c3.checkbox("أدوات أخرى")
    
    epoxy_cost = epoxy_lab_cost = epoxy_tool_cost = 0
    if opt_epoxy:
        c_cov3, c_pr3 = st.columns(2)
        epoxy_cov = c_cov3.number_input("تغطية البرميل (م2):", value=35.0)
        epoxy_pr = c_pr3.number_input("سعر البرميل:", value=350.0)
        qty_epoxy = math.ceil(area / epoxy_cov) if epoxy_cov > 0 else 0
        epoxy_cost = qty_epoxy * epoxy_pr
        st.info(f"🛢️ عدد براميل العزل المطلوبة: **{qty_epoxy} برميل**")
        total_materials += epoxy_cost
    if opt_epoxy_lab:
        epoxy_lab_cost = st.number_input("حساب عمالة العزل:", value=500.0)
        total_labor += epoxy_lab_cost
    if opt_epoxy_tool:
        epoxy_tool_cost = st.number_input("تكلفة أدوات العزل:", value=100.0)
        total_materials += epoxy_tool_cost
        
    cost_stage4 = epoxy_cost + epoxy_lab_cost + epoxy_tool_cost
    total_cost += cost_stage4
    st.caption(f"إجمالي تكلفة هذه المرحلة: {cost_stage4:.2f} ريال")
st.markdown("---")

# --- المرحلة 5: الفزعة ---
st.subheader("👷‍♂️💪 مرحلة 'الفزعة' (تنفيذ بمواد العميل - مصنعية)")
stage5 = st.checkbox("تفعيل مرحلة الفزعة", value=False)
cost_stage5 = 0
if stage5:
    st.write("خيارات المصنعية:")
    c1, c2, c3 = st.columns(3)
    opt_faz_m2 = c1.checkbox("مصنعية بالمتر")
    opt_faz_lab = c2.checkbox("مصنعية مقطوعة", value=True)
    opt_faz_tool = c3.checkbox("أدوات ومعدات")
    
    faz_m2_cost = faz_lab_cost = faz_tool_cost = 0
    if opt_faz_m2: 
        faz_m2_cost = st.number_input("سعر مصنعية المتر:", value=15.0) * area
        total_labor += faz_m2_cost
    if opt_faz_lab: 
        faz_lab_cost = st.number_input("حساب العمالة (مقطوعة):", value=600.0)
        total_labor += faz_lab_cost
    if opt_faz_tool: 
        faz_tool_cost = st.number_input("تكلفة أدوات الفزعة:", value=100.0)
        total_materials += faz_tool_cost
        
    cost_stage5 = faz_m2_cost + faz_lab_cost + faz_tool_cost
    total_cost += cost_stage5
    st.caption(f"إجمالي تكلفة هذه المرحلة: {cost_stage5:.2f} ريال")
st.markdown("---")

# 4. النتيجة النهائية
st.header("💰 3. هامش الربح والنتيجة النهائية")
profit_margin = st.number_input("نسبة هامش الربح % (شاملة للطوارئ):", value=25.0, step=1.0)

if st.button("احسب التسعيرة النهائية 🚀", type="primary", use_container_width=True):
    profit_factor = 1 + (profit_margin / 100)
    
    final_client_report = ""
    if stage1 and cost_stage1 > 0:
        final_client_report += f"- 📏👀 مرحلة 'احسبها صح' (المعاينة): {cost_stage1:.2f} ريال\n"
    if stage2 and cost_stage2 > 0:
        final_client_report += f"- 🧼🫧 مرحلة 'التصفية': {cost_stage2 * profit_factor:.2f} ريال\n"
    if stage3 and cost_stage3 > 0:
        final_client_report += f"- 🧱🩹 مرحلة 'التجديد': {cost_stage3 * profit_factor:.2f} ريال\n"
    if stage4 and cost_stage4 > 0:
        final_client_report += f"- 🛡️🔑 مرحلة 'ازهلها': {cost_stage4 * profit_factor:.2f} ريال\n"
    if stage5 and cost_stage5 > 0:
        final_client_report += f"- 👷‍♂️💪 مرحلة 'الفزعة': {cost_stage5 * profit_factor:.2f} ريال\n"

    operational_cost = cost_stage2 + cost_stage3 + cost_stage4 + cost_stage5
    suggested_price = (operational_cost * profit_factor) + cost_stage1
    net_profit = suggested_price - total_cost
    price_per_meter = suggested_price / area if area > 0 else 0

    tab1, tab2 = st.tabs(["⭐⭐⭐ عرض سعر العميل", "🔒 تقرير الإدارة السري"])
    
    with tab1:
        st.success("جاهز للنسخ والمشاركة مع العميل")
        st.code(f"""مؤسسة خطى العزم للمقاولات
عناية العميل المكرّم: {client_name}

بناءً على المعاينة، نرفق لكم تفاصيل تسعيرة أعمال العزل:
- المساحة الإجمالية للخزان: {area:.2f} متر مربع

تفصيل تكلفة المراحل المطلوبة:
--------------------------------
{final_client_report}--------------------------------
💎 الإجمالي الكلي المطلوب: {suggested_price:.2f} ريال
💰 تكلفة المتر المربع للعميل: {price_per_meter:.2f} ريال/م2
================================""", language="text")
        
    with tab2:
        st.warning("تقرير الإدارة الخاص (لوحة التحكم المالية)")
        st.write(f"**💵 إجمالي ما سيدفعه العميل:** {suggested_price:.2f} ريال")
        st.markdown("---")
        st.write("**تفصيل المصروفات:**")
        st.write(f"🧱 **حساب المواد والأدوات:** {total_materials:.2f} ريال")
        st.write(f"👷‍♂️ **حساب العمالة والمصنعيات:** {total_labor:.2f} ريال")
        if total_other > 0:
            st.write(f"🔄 **تكاليف أخرى (مثل التنظيف بالمتر):** {total_other:.2f} ريال")
        st.markdown("---")
        st.success(f"**💰 صافي الربح المتوقع:** {net_profit:.2f} ريال")
