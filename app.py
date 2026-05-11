import streamlit as st
import google.generativeai as genai

# 1. إعدادات الصفحة الأساسية
st.set_page_config(
    page_title="Smart Queue Time Estimator",
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
        font-size: 40px;
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

    /* تنسيق وقت الانتظار ليكون منظماً وبحجم معتدل ولون أسود */
    .analysis-container h1 {
        font-size: 28px !important;
        color: #000000 !important;
        margin-bottom: 15px !important;
        font-weight: 700 !important;
        border-bottom: none !important;
        padding-bottom: 0px;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. القاموس (Translations Dictionary)
texts = {
    'English': {
        'title_text': "⏳ Smart Queue Time Estimator",
        'place_label': "Location Name",
        'service_label': "Service Type",
        'people_label': "People Ahead",
        'day_label': "Day",
        'obs_label': "📝 Observations",
        'btn_text': "Analyze Queue Status",
        'services_list': ["General", "Doctor Appointment", "Transaction", "Food/Coffee"],
        'days_list': ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
    },
    'العربية': {
        'title_text': "⏳ نظام تقدير وقت الانتظار الذكي",
        'place_label': "اسم الموقع",
        'service_label': "نوع الخدمة",
        'people_label': "الأشخاص أمامك",
        'day_label': "اليوم",
        'obs_label': "📝 ملاحظات",
        'btn_text': "بدء التحليل الذكي",
        'services_list': ["عام", "موعد طبي", "معاملة بنكية", "طعام/قهوة"],
        'days_list': ["الأحد", "الأثنين", "الثلاثاء", "الأربعاء", "الخميس", "الجمعة", "السبت"]
    }
}

# 4. الشريط الجانبي (Sidebar)
with st.sidebar:
    st.markdown("### 🌐 Settings")
    lang = st.radio("Language / اللغة", ["English", "العربية"])
    st.divider()
    api_key = st.text_input("Enter Gemini API Key", type="password")
    st.info("Project for HIS491 | Almaarefa University")

st.markdown(f'<h1 class="main-title">{texts[lang]["title_text"]}</h1>', unsafe_allow_html=True)

# 5. الواجهة المعدلة (Interface)
col1, col2 = st.columns(2)
with col1:
    place = st.text_input(texts[lang]['place_label'])
    service = st.selectbox(texts[lang]['service_label'], texts[lang]['services_list'])
with col2:
    people = st.number_input(texts[lang]['people_label'], min_value=1, value=5)
    day = st.selectbox(texts[lang]['day_label'], texts[lang]['days_list'])

obs = st.text_area(texts[lang]['obs_label'])

# 6. زر التشغيل ومنطق الـ AI
if st.button(texts[lang]['btn_text']):
    if not api_key:
        st.error("Please enter your API Key." if lang == "English" else "الرجاء إدخال مفتاح الـ API")
    else:
        try:
            genai.configure(api_key=api_key)
            models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
            model_to_use = next((m for m in models if "1.5-flash" in m), models[0])
            model = genai.GenerativeModel(model_to_use)
            
            if lang == "العربية":
                prompt = f"""
                المكان: {place}، الخدمة: {service}، العدد: {people}، اليوم: {day}.
                الملاحظات: {obs}.
                
                المطلوب:
                1. ابدأ فوراً بـ <h1>وقت الانتظار المتوقع: [ضع رقماً تقديرياً بالدقائق هنا]</h1>
                (ملاحظة: حتى لو كان اليوم إجازة، افترض أن الفرع يعمل وأعطِ وقتاً بناءً على عدد الأشخاص فقط).
                
                2. ثم أكمل: ### 📊 التحليل الذكي، ### 📋 الجدول، و ### 💡 النصائح.
                ابدأ بـ <h1> مباشرة ولا تكتب أي جمل ترحيبية.
                """
            else:
                prompt = f"""
                Location: {place}, Service: {service}, People: {people}, Day: {day}.
                Notes: {obs}.
                
                Task:
                1. Start immediately with: <h1>Estimate wait time: [Insert estimated minutes here]</h1>
                (Note: Even if the location is normally closed, assume it is open and provide a numeric estimate based on the number of people).
                
                2. Then continue with ### 📊 Situation Analysis, ### 📋 Scenario Table, and ### 💡 Smart Tips.
                Strict Rule: No introductory text. Start with <h1> immediately.
                """
            loading_msg = "🧠 AI is processing..." if lang == "English" else "🧠 جاري التحليل..."
            with st.spinner(loading_msg):
                response = model.generate_content(prompt)
                
                direction = "rtl" if lang == "العربية" else "ltr"
                alignment = "right" if lang == "العربية" else "left"
                
                st.markdown(f"""
                    <div class="analysis-container" style="direction: {direction}; text-align: {alignment};">
                        {response.text}
                    </div>
                """, unsafe_allow_html=True)
                
        except Exception as e:
            if "429" in str(e):
                st.error("Quota exceeded. Please wait 1 minute." if lang == "English" else "تجاوزت الحد المسموح، انتظر دقيقة.")
            else:
                st.error(f"Error: {e}")