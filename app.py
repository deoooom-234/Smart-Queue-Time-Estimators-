import streamlit as st
import google.generativeai as genai

# 1. إعدادات الصفحة الأساسية
st.set_page_config(
    page_title=" Smart Queue Time Estimator",
    page_icon="⏳",
    layout="centered"
)

# 2. كود التصميم الإبداعي (Advanced CSS)
st.markdown("""
    <style>
    .block-container { padding-top: 1rem !important; }
    header { visibility: hidden; }
    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }
    
    .stApp {
        background: linear-gradient(135deg, #FFF9F2 0%, #FFE0B2 100%);
    }
    
    .main-title {
        text-align: center;
        background: linear-gradient(to right, #D4AC0D, #F1C40F);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-family: 'Segoe UI', sans-serif;
        font-size: 50px;
        font-weight: 900;
        margin-bottom: 30px !important;
    }

    div.stButton > button:first-child {
        background: linear-gradient(45deg, #D4AC0D, #F1C40F) !important;
        color: white !important;
        border: none !important;
        padding: 15px 30px !important;
        font-size: 20px !important;
        font-weight: bold !important;
        border-radius: 15px !important;
        transition: all 0.3s ease !important;
        width: 100%;
    }
    
    div.stButton > button:first-child:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(212, 172, 13, 0.4) !important;
    }

    .analysis-container {
        background: rgba(255, 255, 255, 0.75);
        backdrop-filter: blur(12px);
        padding: 30px;
        border-radius: 25px;
        border: 1px solid rgba(255, 255, 255, 0.5);
        box-shadow: 0 10px 40px rgba(0,0,0,0.08);
        margin-top: 30px;
        color: #2C3E50;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. الشريط الجانبي
with st.sidebar:
    st.markdown("### 🌐 Settings")
    lang = st.radio("Language / اللغة", ["English", "العربية"])
    st.divider()
    api_key = st.text_input("Enter Gemini API Key", type="password")
    st.info("Project for HIS491 | Almaarefa University")

# 4. النصوص
if lang == "English":
    title_text = "⏳ Smart Queue Time Estimator"
    place_label = " Location Name"
    service_label = " Service Type"
    people_label = " People Ahead"
    day_label = " Day"
    obs_label = "📝 Observations"
    btn_text = "Analyze Queue Status"
else:
    title_text = "⏳ نظام تقدير وقت الانتظار الذكي"
    place_label = "اسم الموقع"
    service_label = " نوع الخدمة"
    people_label = " الأشخاص أمامك"
    day_label = "اليوم"
    obs_label = "📝 ملاحظات"
    btn_text = "بدء التحليل الذكي"

st.markdown(f'<h1 class="main-title">{title_text}</h1>', unsafe_allow_html=True)

# 5. الواجهة
col1, col2 = st.columns(2)
with col1:
    place = st.text_input(place_label)
    service = st.selectbox(service_label, ["General", "Doctor Appointment", "Transaction", "Food/Coffee"])
with col2:
    people = st.number_input(people_label, min_value=1, value=5)
    day = st.selectbox(day_label, ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"])

obs = st.text_area(obs_label)

#6. زر التشغيل ومنطق الـ AI (النسخة الأصلية المفضلة)
if st.button(btn_text):
    if not api_key:
        st.error("Please enter your API Key.")
    else:
        try:
            genai.configure(api_key=api_key)
            
            # لضمان عمل الكود على أي نسخة مكتبة ومنع خطأ 404
            models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
            model_to_use = next((m for m in models if "1.5-flash" in m), models[0])
            model = genai.GenerativeModel(model_to_use)
            
            # البرومبت الأصلي الذي يعطي نتائج احترافية ومتكاملة
            prompt = f"""
            Analyze the queue for {people} people at {place} ({service}) on {day}. 
            Context: {obs}. Language: {lang}.
            
            Please provide:
            1. **ESTIMATED WAIT TIME** (Bold and large)
            2. A brief analysis of the situation.
            3. A structured table showing: Scenario, Estimated Time, and Recommendation.
            4. 2-3 Quick tips to save time.
            """
            
            # رسالة التحميل التي طلبتها
            with st.spinner("🧠 AI is processing..."):
                response = model.generate_content(prompt)
                # عرض النتيجة النهائية مباشرة داخل التصميم الزجاجي
                st.markdown(f'<div class="analysis-container">{response.text}</div>', unsafe_allow_html=True)
                
        except Exception as e:
            st.error(f"Error: {e}")