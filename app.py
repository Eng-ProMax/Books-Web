import streamlit as st
import requests
from bs4 import BeautifulSoup
import csv
import io
import time
import json
import openpyxl
from openpyxl import Workbook

# ============== جلب مفتاح Gemini تلقائياً ==============
GEMINI_API_KEY = st.secrets.get("GEMINI_API_KEY", "")

# ============== إعدادات الصفحة الأساسية ==============
st.set_page_config(page_title="Book Scraper & AI Assistant", layout="wide")

# حفظ تاريخ المحادثة في الذاكرة
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ============== دالة الذكاء الاصطناعي (Gemini) ==============
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
    try:
        resp = requests.post(url, headers=headers, json=payload, timeout=30)
        if resp.status_code >= 400:
            return "عذراً عيوني، واجهت مشكلة بالاتصال بالسيرفر حالياً."
        data = resp.json()
        parts = data.get("candidates", [{}])[0].get("content", {}).get("parts", [])
        text = "".join(p.get("text", "") for p in parts).strip()
        return text or "..."
    except:
        return "صار خطأ بالشبكة، جرب مرة ثانية بعد شوي."

# ============== دالة سحب بيانات الكتب (Scraper) ==============
def scrape_books(target_url):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    try:
        response = requests.get(target_url, headers=headers, timeout=15)
        if response.status_code != 200:
            return None, f"فشل الاتصال بالموقع (Status Code: {response.status_code})"
        
        soup = BeautifulSoup(response.content, "html.parser")
        books_data = []
        
        # هذا السكرابر مهيأ افتراضياً لموقع Books to Scrape كمثال شهير
        # يمكنك تعديلSelectors بناءً على بنية موقع الكتب المستهدف
        articles = soup.find_all("article", class_="product_pod")
        if not articles:
            # محاولة عامة إذا لم يكن الموقع الافتراضي
            articles = soup.find_all(["div", "li"], class_=["book", "product"])
            
        for article in articles:
            title = ""
            price = ""
            availability = "Available"
            
            # محاولة جلب العنوان
            h3 = article.find("h3")
            if h3 and h3.find("a"):
                title = h3.find("a").get("title") or h3.find("a").text.strip()
            
            # محاولة جلب السعر
            price_tag = article.find("p", class_="price_color")
            if price_tag:
                price = price_tag.text.strip()
                
            if title:
                books_data.append({"العنوان / Title": title, "السعر / Price": price})
                
        return books_data, None
    except Exception as e:
        return None, str(e)


# ============== الشريط الجانبي (الشخصية اللطيفة والشات) ==============
astronaut_img_url = "https://id-preview--b1d3c5f8-fd99-40cc-a15b-c95e2aa643f1.lovable.app/__l5e/documents/astronaut.png"

with st.sidebar:
    st.image(astronaut_img_url, width=100)
    st.title("🤖 رائد الفضاء اللطيف")
    st.caption("مساعدك الرقمي الشخصي العراقي 🧑‍🚀")
    
    lang = st.selectbox("Language / اللغة", ["العربية", "English"])
    AR = lang == "العربية"
    
    st.markdown("---")
    st.subheader("💬 دردش مع رائد الفضاء")
    
    # عرض صندوق المحادثة المصغر داخل السايدبار
    chat_container = st.container(height=300)
    with chat_container:
        for message in st.session_state.chat_history:
            avatar_img = None if message["role"] == "user" else astronaut_img_url
            with st.chat_message(message["role"], avatar=avatar_img):
                st.write(message["content"])
                
    if user_query := st.chat_input("اكتب شيئاً لرائد الفضاء..."):
        st.session_state.chat_history.append({"role": "user", "content": user_query})
        
        # جلب رد الذكاء الاصطناعي
        system_prompt = build_system_prompt("رائد الفضاء", "صاحبي", AR)
        if GEMINI_API_KEY:
            reply = call_gemini(GEMINI_API_KEY, system_prompt, st.session_state.chat_history[:-1], user_query)
        else:
            reply = "أنا هنا وموجود! بس يرجى إضافة الـ GEMINI_API_KEY في الـ Secrets حتى أقدر أحلل وأجاوبك بدقة." if AR else "I'm here! But please add GEMINI_API_KEY to Secrets so I can chat properly."
            
        st.session_state.chat_history.append({"role": "assistant", "content": reply})
        st.rerun()

# ============== الواجهة الرئيسية (تفاصيل موقع الكتب وسحب البيانات) ==============
st.title("📚 نظام سحب بيانات الكتب الذكي (Book Scraper)")
st.write("أدخل رابط موقع الكتب بالأسفل واستخرج البيانات بضغطة زر واحدة.")

# خانة إدخال رابط موقع الكتب
url_input = st.text_input(
    "رابط موقع الكتب المستهدف (Target URL)", 
    value="https://books.toscrape.com/"
)

col1, col2 = st.columns([1, 4])
with col1:
    start_scrape = st.button("🚀 ابدأ السحب (Scrape)", use_container_width=True)

if start_scrape:
    with st.spinner("جاري الاتصال بالموقع وسحب البيانات..."):
        data, error = scrape_books(url_input)
        
        if error:
            st.error(f"❌ حدث خطأ أثناء جلب البيانات: {error}")
        elif not data:
            st.warning("⚠️ لم يتم العثور على أي كتب في هذا الرابط. تأكد من صحة الرابط أو هيكلية الـ HTML.")
        else:
            st.success(f"✅ تم سحب بيانات {len(data)} كتاب بنجاح!")
            
            # عرض البيانات في جدول
            st.dataframe(data, use_container_width=True)
            
            # تحويل البيانات إلى CSV للتحميل
            output = io.StringIO()
            writer = csv.DictWriter(output, fieldnames=data[0].keys())
            writer.writeheader()
            writer.writerows(data)
            csv_data = output.getvalue()
            
            st.download_button(
                label="📥 تحميل البيانات كملف CSV",
                data=csv_data,
                file_name="scraped_books.csv",
                mime="text/csv"
            )
