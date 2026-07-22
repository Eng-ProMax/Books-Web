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

# ============== page config ==============
st.set_page_config(page_title="Book Scraper", layout="wide")

# ============== sidebar ==============
st.sidebar.title("Settings / الاعدادات")

lang = st.sidebar.selectbox("Language / اللغة", ["العربية", "English"])
AR = lang == "العربية"

theme = st.sidebar.selectbox(
    "القالب / Theme",
    ["داكن / Dark", "فاتح / Light", "أزرق / Blue", "أخضر / Green"]
)
font = st.sidebar.selectbox("الخط / Font", ["Cairo", "Tajawal", "Arial", "Courier New"])
font_size = st.sidebar.slider("حجم الخط / Font Size", 12, 24, 16)
text_color = st.sidebar.color_picker("لون النص / Text Color", "#ffffff")

# ============== اعدادات الشخصية المساعدة ==============
st.sidebar.markdown("---")
st.sidebar.subheader("الشخصية المساعدة / Assistant")

# 6 شخصيات كتكوتة ثلاثية الأبعاد (SVG) — كل واحدة عبارة عن دالة ترجع الـ SVG
def svg_astronaut():
    return """
    <svg viewBox="0 0 200 220" xmlns="http://www.w3.org/2000/svg">
      <defs>
        <radialGradient id="body" cx="50%" cy="35%" r="65%">
          <stop offset="0%" stop-color="#ffffff"/><stop offset="100%" stop-color="#cfd6e4"/>
        </radialGradient>
        <radialGradient id="helm" cx="50%" cy="40%" r="60%">
          <stop offset="0%" stop-color="#bfe9ff" stop-opacity="0.9"/>
          <stop offset="100%" stop-color="#4aa8d8" stop-opacity="0.6"/>
        </radialGradient>
      </defs>
      <ellipse cx="100" cy="205" rx="55" ry="8" fill="#000" opacity="0.15"/>
      <ellipse cx="100" cy="140" rx="60" ry="55" fill="url(#body)"/>
      <circle cx="100" cy="90" r="60" fill="url(#helm)" stroke="#ffffff" stroke-width="3"/>
      <circle cx="100" cy="95" r="42" fill="#2a4a6b"/>
      <ellipse cx="85" cy="95" rx="4" ry="6" fill="#fff"/>
      <ellipse cx="115" cy="95" rx="4" ry="6" fill="#fff"/>
      <ellipse cx="78" cy="108" rx="6" ry="3" fill="#ff9ab0" opacity="0.8"/>
      <ellipse cx="122" cy="108" rx="6" ry="3" fill="#ff9ab0" opacity="0.8"/>
      <path d="M92 108 Q100 115 108 108" stroke="#fff" stroke-width="2" fill="none" stroke-linecap="round"/>
      <line x1="100" y1="30" x2="100" y2="18" stroke="#ddd" stroke-width="2"/>
      <circle cx="100" cy="15" r="4" fill="#ff5a5a"/>
      <circle cx="70" cy="70" r="10" fill="#fff" opacity="0.4"/>
    </svg>"""

def svg_cat_shark():
    return """
    <svg viewBox="0 0 200 220" xmlns="http://www.w3.org/2000/svg">
      <ellipse cx="100" cy="205" rx="55" ry="8" fill="#000" opacity="0.15"/>
      <ellipse cx="100" cy="150" rx="55" ry="50" fill="#f8f8f8"/>
      <circle cx="100" cy="100" r="55" fill="#fafafa"/>
      <path d="M45 100 Q40 40 100 45 Q160 40 155 100 Q155 60 130 55 L100 90 L70 55 Q45 60 45 100Z" fill="#5aa4d0"/>
      <path d="M60 70 L75 55 L80 75Z" fill="#fff"/>
      <path d="M140 70 L125 55 L120 75Z" fill="#fff"/>
      <ellipse cx="82" cy="105" rx="5" ry="7" fill="#111"/>
      <ellipse cx="118" cy="105" rx="5" ry="7" fill="#111"/>
      <circle cx="83" cy="103" r="1.5" fill="#fff"/>
      <circle cx="119" cy="103" r="1.5" fill="#fff"/>
      <ellipse cx="75" cy="120" rx="6" ry="3" fill="#ffb3c1" opacity="0.7"/>
      <ellipse cx="125" cy="120" rx="6" ry="3" fill="#ffb3c1" opacity="0.7"/>
      <path d="M95 118 L100 122 L105 118" stroke="#333" stroke-width="1.5" fill="none"/>
      <path d="M92 125 Q100 132 108 125" stroke="#333" stroke-width="1.5" fill="none"/>
    </svg>"""

def svg_cat_frog():
    return """
    <svg viewBox="0 0 200 220" xmlns="http://www.w3.org/2000/svg">
      <ellipse cx="100" cy="205" rx="55" ry="8" fill="#000" opacity="0.15"/>
      <ellipse cx="100" cy="150" rx="55" ry="50" fill="#f8f8f8"/>
      <circle cx="100" cy="100" r="55" fill="#fafafa"/>
      <path d="M45 95 Q45 45 100 45 Q155 45 155 95 Q155 70 100 70 Q45 70 45 95Z" fill="#7ac074"/>
      <circle cx="65" cy="65" r="14" fill="#7ac074"/>
      <circle cx="135" cy="65" r="14" fill="#7ac074"/>
      <circle cx="65" cy="63" r="7" fill="#fff"/><circle cx="135" cy="63" r="7" fill="#fff"/>
      <circle cx="65" cy="63" r="3" fill="#111"/><circle cx="135" cy="63" r="3" fill="#111"/>
      <ellipse cx="85" cy="108" rx="4" ry="6" fill="#111"/>
      <ellipse cx="115" cy="108" rx="4" ry="6" fill="#111"/>
      <ellipse cx="78" cy="122" rx="6" ry="3" fill="#ffb3c1" opacity="0.7"/>
      <ellipse cx="122" cy="122" rx="6" ry="3" fill="#ffb3c1" opacity="0.7"/>
      <path d="M95 120 L100 124 L105 120" stroke="#333" stroke-width="1.5" fill="none"/>
    </svg>"""

def svg_chick():
    return """
    <svg viewBox="0 0 200 220" xmlns="http://www.w3.org/2000/svg">
      <ellipse cx="100" cy="205" rx="55" ry="8" fill="#000" opacity="0.15"/>
      <defs><radialGradient id="ck" cx="50%" cy="40%" r="60%">
        <stop offset="0%" stop-color="#fff59a"/><stop offset="100%" stop-color="#f2c14e"/>
      </radialGradient></defs>
      <circle cx="100" cy="115" r="80" fill="url(#ck)"/>
      <path d="M95 60 Q100 45 105 60Z" fill="#e08a2b"/>
      <ellipse cx="80" cy="110" rx="6" ry="9" fill="#111"/>
      <ellipse cx="120" cy="110" rx="6" ry="9" fill="#111"/>
      <circle cx="82" cy="107" r="2" fill="#fff"/><circle cx="122" cy="107" r="2" fill="#fff"/>
      <path d="M88 130 L100 140 L112 130 Z" fill="#e08a2b"/>
      <ellipse cx="70" cy="135" rx="8" ry="4" fill="#ff9ab0" opacity="0.7"/>
      <ellipse cx="130" cy="135" rx="8" ry="4" fill="#ff9ab0" opacity="0.7"/>
    </svg>"""

def svg_puppy():
    return """
    <svg viewBox="0 0 200 220" xmlns="http://www.w3.org/2000/svg">
      <ellipse cx="100" cy="205" rx="55" ry="8" fill="#000" opacity="0.15"/>
      <ellipse cx="100" cy="160" rx="55" ry="45" fill="#5b8fd6"/>
      <circle cx="100" cy="100" r="58" fill="#fafafa"/>
      <ellipse cx="55" cy="90" rx="18" ry="28" fill="#e6e6e6"/>
      <ellipse cx="145" cy="90" rx="18" ry="28" fill="#e6e6e6"/>
      <ellipse cx="82" cy="105" rx="6" ry="8" fill="#111"/>
      <ellipse cx="118" cy="105" rx="6" ry="8" fill="#111"/>
      <circle cx="84" cy="102" r="2" fill="#fff"/><circle cx="120" cy="102" r="2" fill="#fff"/>
      <ellipse cx="100" cy="125" rx="6" ry="4" fill="#333"/>
      <path d="M92 132 Q100 140 108 132" stroke="#333" stroke-width="2" fill="none"/>
      <ellipse cx="72" cy="122" rx="7" ry="3" fill="#ffb3c1" opacity="0.7"/>
      <ellipse cx="128" cy="122" rx="7" ry="3" fill="#ffb3c1" opacity="0.7"/>
    </svg>"""

def svg_robot():
    return """
    <svg viewBox="0 0 200 220" xmlns="http://www.w3.org/2000/svg">
      <defs><radialGradient id="rb" cx="50%" cy="35%" r="65%">
        <stop offset="0%" stop-color="#e9f3ff"/><stop offset="100%" stop-color="#8fb8de"/>
      </radialGradient></defs>
      <ellipse cx="100" cy="205" rx="55" ry="8" fill="#000" opacity="0.15"/>
      <rect x="55" y="90" width="90" height="90" rx="30" fill="url(#rb)"/>
      <rect x="60" y="120" width="80" height="45" rx="15" fill="#4a7ab0"/>
      <circle cx="82" cy="140" r="6" fill="#8ff"/>
      <circle cx="118" cy="140" r="6" fill="#8ff"/>
      <ellipse cx="72" cy="150" rx="5" ry="2" fill="#ffb3c1"/>
      <ellipse cx="128" cy="150" rx="5" ry="2" fill="#ffb3c1"/>
      <line x1="100" y1="90" x2="100" y2="70" stroke="#8fb8de" stroke-width="3"/>
      <circle cx="100" cy="65" r="6" fill="#ff5a5a"/>
    </svg>"""

CHARACTERS = {
    "Astro":  ("رائد فضاء 🚀" if AR else "Astronaut 🚀", svg_astronaut()),
    "Shark":  ("قط القرش 🦈" if AR else "Shark Cat 🦈", svg_cat_shark()),
    "Frog":   ("قط الضفدع 🐸" if AR else "Frog Cat 🐸", svg_cat_frog()),
    "Chick":  ("الكتكوت 🐥" if AR else "Chick 🐥", svg_chick()),
    "Puppy":  ("الجرو 🐶" if AR else "Puppy 🐶", svg_puppy()),
    "Robot":  ("الروبوت 🤖" if AR else "Robot 🤖", svg_robot()),
}

char_pick_label = "اختر الشخصية" if AR else "Choose Character"
character_key = st.sidebar.selectbox(char_pick_label, list(CHARACTERS.keys()),
                                     format_func=lambda k: CHARACTERS[k][0])

character_name = st.sidebar.text_input("اسم الشخصية" if AR else "Character Name",
                                       "كتكوت" if AR else "Buddy")
user_name = st.sidebar.text_input("شسمك؟" if AR else "Your Name",
                                  "صديقي" if AR else "Friend")

# ============== theme ==============
themes = {
    "داكن / Dark":  {"bg": "#1e1e2e", "card": "#2a2a3e", "accent": "#7c6af7"},
    "فاتح / Light": {"bg": "#f0f2f6", "card": "#ffffff",  "accent": "#4a90d9"},
    "أزرق / Blue":  {"bg": "#0d1b2a", "card": "#1b2a3b",  "accent": "#00b4d8"},
    "أخضر / Green": {"bg": "#0d2b1e", "card": "#1a3a2a",  "accent": "#2ecc71"},
}
t = themes[theme]

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cairo&family=Tajawal&display=swap');
html, body, [class*="css"] {{
    font-family: '{font}', sans-serif;
    font-size: {font_size}px;
    background-color: {t['bg']};
    color: {text_color};
}}
.main {{ background-color: {t['bg']}; }}
.block-container {{ padding-bottom: 220px !important; }}  /* مساحة تحت للشخصية */
.book-card {{
    background-color: {t['card']};
    border-left: 4px solid {t['accent']};
    border-radius: 10px;
    padding: 12px 16px;
    margin-bottom: 10px;
    font-size: {font_size}px;
    color: {text_color};
}}
.title-bar {{
    font-size: {font_size + 6}px;
    font-weight: bold;
    color: {t['accent']};
    margin-bottom: 20px;
}}
.count-badge {{
    background-color: {t['accent']};
    color: white; padding: 4px 12px; border-radius: 20px;
    font-size: {font_size - 2}px;
}}
</style>
""", unsafe_allow_html=True)

# ============== نصوص ==============
LBL_URL     = "رابط الموقع" if AR else "Website URL"
LBL_REFRESH = "تحديث تلقائي (ثانية، 0=إيقاف)" if AR else "Auto Refresh (sec, 0=off)"
LBL_PAGES   = "عدد الصفحات" if AR else "Number of Pages"
LBL_SEARCH  = "بحث باسم الكتاب" if AR else "Search by Title"
LBL_PRICE   = "الحد الاقصى للسعر" if AR else "Max Price"
LBL_SORT    = "ترتيب حسب" if AR else "Sort By"
BTN_START   = "ابدأ السحب" if AR else "Start Scraping"
BTN_CSV     = "تنزيل CSV" if AR else "Download CSV"
BTN_EXCEL   = "تنزيل Excel" if AR else "Download Excel"

FIELD_HINTS = {
    LBL_URL: (f"اكتب رابط الموقع هنا يا {user_name} 🌐" if AR else f"Type the website URL, {user_name} 🌐"),
    LBL_SEARCH: (f"دور عن اسم الكتاب يا {user_name} 🔍" if AR else f"Search for a title, {user_name} 🔍"),
    LBL_PRICE: ("حدد اعلى سعر تقبل بيه 💰" if AR else "Set your max price 💰"),
    LBL_SORT: ("شلون تريد ترتب الكتب؟ 📊" if AR else "How to sort? 📊"),
    LBL_REFRESH: ("تريد تحديث تلقائي؟ ⏱️" if AR else "Auto refresh? ⏱️"),
    LBL_PAGES: ("كم صفحة تسحب؟ 📄" if AR else "How many pages? 📄"),
}

BUTTON_REACTIONS = {
    BTN_START: [
        f"يالله يا {user_name}، جاري السحب! 🚀" if AR else f"Let's go, {user_name}! 🚀",
        f"خلي نشوف شنو الكتب الحلوة!" if AR else "Let's see the good books!",
    ],
    BTN_CSV: [
        f"احتفظ بالملف يا {user_name} 📥" if AR else f"Keep it safe, {user_name} 📥",
    ],
    BTN_EXCEL: [
        f"اكسل جاهز يا {user_name} 😎" if AR else f"Excel is ready, {user_name} 😎",
    ],
}

GREETING = (f"هلا {user_name}! انا {character_name} 👋" if AR else f"Hi {user_name}! I'm {character_name} 👋")

# ============== الشخصية الكتكوتة (Overlay ثابت بأعلى zIndex) ==============
mascot_svg = CHARACTERS[character_key][1]

mascot_html = f"""
<style>
  #mascot-wrap {{
    position: fixed; right: 20px; bottom: 90px;
    width: 180px; z-index: 2147483647; pointer-events: none;
    font-family: 'Cairo','Tajawal',sans-serif;
  }}
  #mascot-body {{
    width: 140px; height: 155px; margin: 0 auto;
    filter: drop-shadow(0 12px 14px rgba(0,0,0,0.35));
    animation: floaty 3.2s ease-in-out infinite;
    transform-origin: center bottom;
  }}
  @keyframes floaty {{
    0%,100% {{ transform: translateY(0) rotate(-2deg); }}
    50%     {{ transform: translateY(-10px) rotate(2deg); }}
  }}
  #mascot-bubble {{
    position: absolute; bottom: 150px; right: 10px;
    max-width: 240px; min-width: 120px;
    background: #fff; color: #222;
    border: 2px solid #333;
    border-radius: 16px; padding: 10px 14px;
    box-shadow: 0 8px 20px rgba(0,0,0,0.3);
    font-size: 15px; line-height: 1.35;
    opacity: 0; transform: translateY(6px); transition: all .25s ease;
  }}
  #mascot-bubble.show {{ opacity: 1; transform: translateY(0); }}
  #mascot-bubble::after {{
    content: ""; position: absolute; bottom: -10px; right: 30px;
    width: 0; height: 0; border: 10px solid transparent;
    border-top-color: #fff; border-bottom: 0;
    filter: drop-shadow(0 2px 0 #333);
  }}
</style>

<div id="mascot-wrap">
  <div id="mascot-bubble"></div>
  <div id="mascot-body">{mascot_svg}</div>
</div>

<script>
(function(){{
  const doc = window.parent.document;
  // نظف اي نسخة سابقة
  const prev = doc.getElementById('__mascot_overlay__');
  if (prev) prev.remove();

  const holder = doc.createElement('div');
  holder.id = '__mascot_overlay__';
  holder.innerHTML = document.getElementById('mascot-wrap').outerHTML +
                     '<style>' + document.querySelector('style').innerHTML + '</style>';
  doc.body.appendChild(holder);

  const bubble = doc.getElementById('mascot-bubble');
  const body   = doc.getElementById('mascot-body');
  let hideTimer = null;

  const HINTS   = {json.dumps(FIELD_HINTS, ensure_ascii=False)};
  const REACTS  = {json.dumps(BUTTON_REACTIONS, ensure_ascii=False)};
  const GENERIC = {json.dumps([f"احسنت يا {user_name}! 👍" if AR else f"Nice job, {user_name}! 👍", f"استمر يا {user_name} 💪" if AR else f"Keep going, {user_name} 💪"], ensure_ascii=False)};
  const GREETING = {json.dumps(GREETING)};

  function say(text, ms){{
    if (!text) return;
    bubble.textContent = text;
    bubble.classList.add('show');
    body.style.animationDuration = '1.2s';
    clearTimeout(hideTimer);
    hideTimer = setTimeout(() => {{
      bubble.classList.remove('show');
      body.style.animationDuration = '3.2s';
    }}, ms || 3500);
  }}

  // ترحيب مرة واحدة لكل تركيبة
  const combo = {json.dumps(character_key + '|' + character_name + '|' + user_name)};
  if (sessionStorage.getItem('mascot_combo') !== combo) {{
    sessionStorage.setItem('mascot_combo', combo);
    setTimeout(() => say(GREETING, 4000), 400);
  }} else {{
    setTimeout(() => say(GREETING, 2500), 400);
  }}

  doc.addEventListener('click', function(e){{
    const btn = e.target.closest('button, [role="button"], a');
    if (!btn) return;
    const txt = (btn.innerText || '').trim();
    let pool = REACTS[txt];
    if (!pool || !pool.length) pool = GENERIC;
    say(pool[Math.floor(Math.random()*pool.length)], 3200);
  }}, true);

  doc.addEventListener('focusin', function(e){{
    const el = e.target;
    if (!el || !(el.tagName === 'INPUT' || el.tagName === 'TEXTAREA' || el.getAttribute('role')==='combobox')) return;
    const cont = el.closest('[data-testid]') || el.parentElement?.parentElement;
    const lab  = cont ? cont.querySelector('label') : null;
    const key  = lab ? lab.innerText.trim() : '';
    if (HINTS[key]) say(HINTS[key], 3000);
  }}, true);
}})();
</script>
"""
components.html(mascot_html, height=0)

# ============== title ==============
title_text = "أداة استخراج بيانات الكتب" if AR else "Book Data Scraper"
st.markdown(f'<div class="title-bar">{title_text}</div>', unsafe_allow_html=True)

# ============== inputs ==============
col1, col2, col3_main = st.columns([2, 1, 1])
with col1:
    url = st.text_input(LBL_URL, "https://books.toscrape.com")
with col2:
    auto_refresh = st.number_input(LBL_REFRESH, min_value=0, value=0, step=10)
with col3_main:
    max_pages = st.number_input(LBL_PAGES, min_value=1, max_value=50, value=1)

col3, col4, col5 = st.columns(3)
with col3:
    search_query = st.text_input(LBL_SEARCH)
with col4:
    max_price = st.slider(LBL_PRICE, 0, 100, 100)
with col5:
    sort_options = (["بدون ترتيب", "السعر تصاعدي", "السعر تنازلي", "الاسم", "التقييم"]
                    if AR else ["No Sort", "Price Low to High", "Price High to Low", "Title", "Rating"])
    sort_by = st.selectbox(LBL_SORT, sort_options)

button = st.button(BTN_START)

rating_map = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}

def scrape_books(base_url, max_pages):
    data = []
    progress = st.progress(0, text="جاري السحب..." if AR else "Scraping...")
    for page in range(1, max_pages + 1):
        try:
            page_url = base_url if page == 1 else base_url.rstrip("/") + f"/catalogue/page-{page}.html"
            response = requests.get(page_url, timeout=10)
            if response.status_code != 200:
                st.warning(f"الصفحة {page} غير موجودة." if AR else f"Page {page} not found.")
                break
            soup = BeautifulSoup(response.text, "html.parser")
            books = soup.find_all("article", class_="product_pod")
            if not books:
                st.warning(f"لا توجد كتب بالصفحة {page}." if AR else f"No books on page {page}.")
                break
            for book in books:
                title = book.h3.a["title"]
                price_text = book.find("p", class_="price_color").text
                price_num = float(price_text.replace("£", "").replace("Â", "").strip())
                rating_word = book.p["class"][1]
                rating_num = rating_map.get(rating_word, 0)
                rating_stars = "★" * rating_num + "☆" * (5 - rating_num)
                img_tag = book.find("img")
                img_url = ""
                if img_tag:
                    img_src = img_tag["src"].replace("../../", "")
                    img_url = "https://books.toscrape.com/" + img_src
                data.append({"title": title, "price": price_num, "price_text": price_text,
                             "rating": rating_num, "rating_stars": rating_stars, "img_url": img_url})
            progress.progress(page / max_pages,
                              text=(f"صفحة {page} من {max_pages}" if AR else f"Page {page} of {max_pages}"))
        except Exception as e:
            st.error(f"خطأ بالصفحة {page}: {e}" if AR else f"Error on page {page}: {e}")
            break
    progress.empty()
    return data

def filter_sort(data, search, max_p, sort):
    if search:
        data = [b for b in data if search.lower() in b["title"].lower()]
    data = [b for b in data if b["price"] <= max_p]
    if sort in ["السعر تصاعدي", "Price Low to High"]:
        data = sorted(data, key=lambda x: x["price"])
    elif sort in ["السعر تنازلي", "Price High to Low"]:
        data = sorted(data, key=lambda x: x["price"], reverse=True)
    elif sort in ["الاسم", "Title"]:
        data = sorted(data, key=lambda x: x["title"])
    elif sort in ["التقييم", "Rating"]:
        data = sorted(data, key=lambda x: x["rating"], reverse=True)
    return data

def export_excel(data):
    wb = Workbook()
    ws = wb.active
    ws.title = "Books"
    ws.append(["Title", "Price", "Rating"])
    for b in data:
        ws.append([b["title"], b["price_text"], b["rating_stars"]])
    output = io.BytesIO()
    wb.save(output)
    return output.getvalue()

if button or auto_refresh > 0:
    placeholder = st.empty()
    while True:
        with placeholder.container():
            data = scrape_books(url, max_pages)
            if not data:
                st.error("لم يتم ايجاد بيانات." if AR else "No data found.")
            else:
                filtered = filter_sort(data, search_query, max_price, sort_by)
                count_msg = f"تم ايجاد {len(filtered)} كتاب" if AR else f"Found {len(filtered)} books"
                st.markdown(f'<span class="count-badge">{count_msg}</span>', unsafe_allow_html=True)
                st.write("")
                cols = st.columns(4)
                for i, book in enumerate(filtered):
                    with cols[i % 4]:
                        if book["img_url"]:
                            st.image(book["img_url"], use_column_width=True)
                        price_label = "السعر" if AR else "Price"
                        rating_label = "التقييم" if AR else "Rating"
                        st.markdown(f"""
                        <div class="book-card">
                            <b>{book['title']}</b><br>
                            {price_label}: {book['price_text']}<br>
                            {rating_label}: {book['rating_stars']}
                        </div>
                        """, unsafe_allow_html=True)
                csv_output = io.StringIO()
                writer = csv.writer(csv_output)
                writer.writerow(["Title", "Price", "Rating"])
                writer.writerows([[b["title"], b["price_text"], b["rating_stars"]] for b in filtered])
                col_csv, col_excel = st.columns(2)
                with col_csv:
                    st.download_button(BTN_CSV, csv_output.getvalue(), "books.csv", "text/csv")
                with col_excel:
                    st.download_button(BTN_EXCEL, export_excel(filtered), "books.xlsx",
                                       "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        if auto_refresh == 0:
            break
        time.sleep(auto_refresh)
        st.rerun()
