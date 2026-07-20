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

# ============== جلب مفتاح Gemini تلقائياً من الإعدادات السرية ==============
# يبحث التطبيق عن المفتاح في st.secrets تلقائياً دون تدخل المستخدم
GEMINI_API_KEY = st.secrets.get("GEMINI_API_KEY", "")

# ============== المساعد الذكي (Gemini) ==============
def build_system_prompt(character_name, user_name, ar):
    if ar:
        return (
            f"انت شخصية اسمها {character_name}، مساعد ودود ومرح جوه تطبيق ويب لسحب بيانات الكتب. "
            f"احچي باللهجة العراقية العامية، خفيف الظل ومختصر (جملتين لثلاث كحد اقصى). "
            f"صاحبك اسمه {user_name}. لا تستخدم اي رموز تعبيرية بالرد."
        )
    return (
        f"You are a friendly, playful assistant character named {character_name} inside a book-scraper web app. "
        f"Keep replies short (max 2-3 sentences), warm, and conversational. "
        f"The user's name is {user_name}. Do not use emojis in your replies."
    )

def call_gemini(api_key, system_prompt, history, user_msg):
    # استخدام موديل gemini-2.5-flash كونه الأحدث والمستقر
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"
    headers = {
        "x-goog-api-key": api_key,
        "Content-Type": "application/json",
    }
    contents = []
    for m in history:
        role = "user" if m["role"] == "user" else "model"
        contents.append({"role": role, "parts": [{"text": m["content"]}]})
    contents.append({"role": "user", "parts": [{"text": user_msg}]})
    payload = {
        "contents": contents,
        "systemInstruction": {"parts": [{"text": system_prompt}]},
        "generationConfig": {"maxOutputTokens": 300},
    }
    resp = requests.post(url, headers=headers, json=payload, timeout=30)
    if resp.status_code >= 400:
        try:
            err_detail = resp.json().get("error", {}).get("message", resp.text)
        except Exception:
            err_detail = resp.text
        raise RuntimeError(f"Gemini {resp.status_code}: {err_detail}")
    data = resp.json()
    candidates = data.get("candidates", [{}])
    cand = candidates[0] if candidates else {}
    parts = cand.get("content", {}).get("parts", [])
    text = "".join(p.get("text", "") for p in parts).strip()
    return text or "..."

def get_ai_reply(user_msg, character_name, user_name, ar, history):
    if not GEMINI_API_KEY:
        return "مفتاح Gemini غير معرف في إعدادات التطبيق السرية (Secrets)!" if ar else "Gemini API Key missing in Secrets!"
    
    system_prompt = build_system_prompt(character_name, user_name, ar)
    try:
        return call_gemini(GEMINI_API_KEY, system_prompt, history, user_msg)
    except requests.exceptions.RequestException as e:
        return f"صار خطأ بالاتصال: {e}" if ar else f"Connection error: {e}"
    except Exception as e:
        return f"صار خطأ: {e}" if ar else f"Error: {e}"

# إعدادات الصفحة الأساسية
st.set_page_config(page_title="Book Scraper", layout="wide")

# حفظ تاريخ المحادثة
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ============== الشريط الجانبي (Sidebar) ==============
st.sidebar.title("Settings / الاعدادات")

lang = st.sidebar.selectbox("Language / اللغة", ["العربية","English"])
AR = lang == "العربية"

# رابط صورة رائد الفضاء 
astronaut_img_url = "https://id-preview--b1d3c5f8-fd99-40cc-a15b-c95e2aa643f1.lovable.app/__l5e/documents/astronaut.png"

font = st.sidebar.selectbox("الخط / Font", ["Cairo","Tajawal","Arial"])
font_size = st.sidebar.slider("حجم الخط / Font Size", 12, 24, 16)

# ============== واجهة الشات ==============
st.title("🤖 مساعد سحب بيانات الكتب الذكي")
st.image(astronaut_img_url, caption="رائد الفضاء - المساعد الذكي", width=120)
st.markdown("---")

# عرض المحادثة
for message in st.session_state.chat_history:
    if message["role"] == "user":
        with st.chat_message("user"):
            st.write(message["content"])
    else:
        with st.chat_message("assistant", avatar=astronaut_img_url):
            st.write(message["content"])

# صندوق إرسال الرسائل
if user_query := st.chat_input("اسأل المساعد الذكي شيئاً..."):
    with st.chat_message("user"):
        st.write(user_query)
    
    st.session_state.chat_history.append({"role": "user", "content": user_query})
    
    with st.chat_message("assistant", avatar=astronaut_img_url):
        with st.spinner("جايك الرد..."):
            reply = get_ai_reply(
                user_msg=user_query,
                character_name="رائد الفضاء",
                user_name="صاحبي",
                ar=AR,
                history=st.session_state.chat_history[:-1]
            )
            st.write(reply)
            
    st.session_state.chat_history.append({"role": "assistant", "content": reply})
