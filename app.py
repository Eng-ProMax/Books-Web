import streamlit as st
import requests
from bs4 import BeautifulSoup
import csv
import io
import time
import json
import openpyxl
from openpyxl import Workbook
import streamlit.components.v1 as components
pip install streamlit

# ==============================================================================
# 1. إعدادات المفتاح وتفاعل الشخصية (الربط الذكي)
# ==============================================================================
# جلب المفتاح تلقائياً من الـ Secrets بأمان
GEMINI_API_KEY = st.secrets.get("GEMINI_API_KEY", "")

# رابط صورة/أيقونة رائد الفضاء ثلاثي الأبعاد
astronaut_img_url = "https://id-preview--b1d3c5f8-fd99-40cc-a15b-c95e2aa643f1.lovable.app/__l5e/documents/astronaut.png"

# الحفاظ على حالة تفاعل وحركة الشخصية
if "astronaut_status" not in st.session_state:
    st.session_state.astronaut_status = "👋 هلو عيوني! أنا جاهز أساعدك بسحب البيانات."
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# دالة بناء توجيهات الشخصية (السيستم برومبت العراقي)
def build_system_prompt(action_context=""):
    return (
        f"أنت شخصية ثلاثية الأبعاد لطيفة ومرحة اسمها (رائد الفضاء) داخل تطبيق سحب بيانات كتب. "
        f"تتحدث اللهجة العراقية العامية حصراً. خفيف الظل، ردودك قصيرة جداً ومختصرة (جملة أو جملتين). "
        f"الآن المستخدم قام بـ: ({action_context}). علّق على هذا الإجراء بطريقتك الفكاهية والودودة دون أي رموز تعبيرية."
    )

# دالة استدعاء Gemini ليتكلم رائد الفضاء بناءً على الحدث
def astronaut_speak(action_context):
    if not GEMINI_API_KEY:
        return "المفتاح ماكو! ضيف GEMINI_API_KEY بالـ Secrets حتى أقدر أتفاعل وياك."
    
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"
    headers = {"x-goog-api-key": GEMINI_API_KEY, "Content-Type": "application/json"}
    
    system_prompt = build_system_prompt(action_context)
    payload = {
        "contents": [{"role": "user", "parts": [{"text": f"تفاعل مع هذا الإجراء: {action_context}"}]}],
        "systemInstruction": {"parts": [{"text": system_prompt}]},
        "generationConfig": {"maxOutputTokens": 150},
    }
    try:
        resp = requests.post(url, headers=headers, json=payload, timeout=10)
        if resp.status_code == 200:
            return resp.json().get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "..." )
    except:
        pass
    return "صاروخي واكف حالياً، بس أنا وياك!"

# ==============================================================================
# 2. كود موقعك الأصلي (مع حقن تفاعل الشخصية عند الضغط)
# ==============================================================================
st.set_page_config(page_title="Book Scraper", layout="wide")

# القائمة الجانبية (Sidebar) الأصلية كما هي
st.sidebar.title("Settings / الاعدادات")
lang = st.sidebar.selectbox("Language / اللغة", ["العربية","English"])
AR = lang == "العربية"

font = st.sidebar.selectbox("الخط / Font", ["Cairo","Tajawal","Arial"])
font_size = st.sidebar.slider("حجم الخط / Font Size", 12, 24, 16)

# --- عرض شخصية رائد الفضاء وتفاعلها الحركي واللفظي في أعلى الواجهة ---
st.markdown("### 🧑‍🚀 المساعد الذكي المتفاعل")
col_ast, col_speech = st.columns([1, 5])
with col_ast:
    # الصورة هنا تمثل مجسم الشخصية الذي يتحدث
    st.image(astronaut_img_url, width=90)
with col_speech:
    st.info(st.session_state.astronaut_status)

st.title("📚 واجهة سحب بيانات الكتب")

# الأزرار وتفاعلها الذكي:
url_input = st.text_input("أدخل رابط موقع الكتب:", "https://books.toscrape.com/")

col_buttons = st.columns(3)

with col_buttons[0]:
    if st.button("🚀 ابدأ السحب والتجميع"):
        # الشخصية تتعرف على الزر وتتكلم فوراً
        st.session_state.astronaut_status = astronaut_speak("المستخدم ضغط على زر بدء سحب البيانات وينتظر النتيجة")
        st.toast("جاري تشغيل محركات السحب...")
        # (هنا يوضع كود السحب الخاص بك بالكامل دون تغيير)
        st.success("تم السحب بنجاح!")
        st.rerun()

with col_buttons[1]:
    if st.button("📥 تحميل ملف CSV"):
        st.session_state.astronaut_status = astronaut_speak("المستخدم قام بالضغط على زر تحميل البيانات بصيغة CSV")
        # (هنا كود التحميل الأصلي الخاص بك)
        st.rerun()

with col_buttons[2]:
    if st.button("🧹 مسح البيانات المكتشفة"):
        st.session_state.astronaut_status = astronaut_speak("المستخدم ضغط على زر مسح وتصفية البيانات وإعادة التعيين")
        st.rerun()

# --- قسم المحادثة المباشرة مع الشخصية بالأسفل ---
st.markdown("---")
st.subheader("💬 تكلم مباشرة مع رائد الفضاء")

for msg in st.session_state.chat_history:
    avatar = None if msg["role"] == "user" else astronaut_img_url
    with st.chat_message(msg["role"], avatar=avatar):
        st.write(msg["content"])

if user_msg := st.chat_input("قول شيء لرائد الفضاء..."):
    with st.chat_message("user"):
        st.write(user_msg)
    st.session_state.chat_history.append({"role": "user", "content": user_msg})
    
    # استجابة الشات من Gemini بروح الشخصية
    reply = astronaut_speak(f"المستخدم يدردش معك ويقول لك: {user_msg}")
    
    with st.chat_message("assistant", avatar=astronaut_img_url):
        st.write(reply)
    st.session_state.chat_history.append({"role": "assistant", "content": reply})
    st.session_state.astronaut_status = reply  # تحديث الحالة العلوية أيضاً ليتحرك ويتفاعل
