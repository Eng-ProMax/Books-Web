# -*- coding: utf-8 -*-
"""
📚 مشروع الكتب - مع مساعد شخصية كتكوتة تفاعلية
- بدون أي مفتاح API
- 6 شخصيات لطيفة ثلاثية الأبعاد (CSS 3D)
- المستخدم يختار الشخصية + اسمها + الاسم الذي تناديه به
- الشخصية تتفاعل مع كل زر بتعابير ووضعيات وكلام مختلف
- تعرف كل أزرار المشروع ودليل كامل عنه
"""

import streamlit as st
import random
from datetime import datetime

# ═══════════════════════════════════════════════════════════
# إعدادات الصفحة
# ═══════════════════════════════════════════════════════════
st.set_page_config(
    page_title="📚 مكتبتي الذكية",
    page_icon="🐥",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ═══════════════════════════════════════════════════════════
# الشخصيات (SVG مرسومة يدوياً بأسلوب Chibi ثلاثي الأبعاد)
# ═══════════════════════════════════════════════════════════

def astronaut_svg(mood="happy"):
    eyes = {
        "happy": '<circle cx="80" cy="95" r="6" fill="#1a1a1a"/><circle cx="120" cy="95" r="6" fill="#1a1a1a"/>',
        "excited": '<path d="M74 95 Q80 85 86 95" stroke="#1a1a1a" stroke-width="3" fill="none"/><path d="M114 95 Q120 85 126 95" stroke="#1a1a1a" stroke-width="3" fill="none"/>',
        "thinking": '<circle cx="80" cy="95" r="5" fill="#1a1a1a"/><circle cx="120" cy="98" r="4" fill="#1a1a1a"/>',
        "sad": '<path d="M74 98 Q80 105 86 98" stroke="#1a1a1a" stroke-width="3" fill="none"/><path d="M114 98 Q120 105 126 98" stroke="#1a1a1a" stroke-width="3" fill="none"/>',
        "sleep": '<path d="M74 95 L86 95" stroke="#1a1a1a" stroke-width="3"/><path d="M114 95 L126 95" stroke="#1a1a1a" stroke-width="3"/>',
    }
    mouth = {
        "happy": '<path d="M92 115 Q100 122 108 115" stroke="#1a1a1a" stroke-width="2.5" fill="none"/>',
        "excited": '<ellipse cx="100" cy="118" rx="7" ry="5" fill="#ff6b8a"/>',
        "thinking": '<circle cx="100" cy="118" r="2" fill="#1a1a1a"/>',
        "sad": '<path d="M92 122 Q100 115 108 122" stroke="#1a1a1a" stroke-width="2.5" fill="none"/>',
        "sleep": '<path d="M95 118 Q100 122 105 118" stroke="#1a1a1a" stroke-width="2" fill="none"/>',
    }
    return f'''
    <svg viewBox="0 0 200 220" xmlns="http://www.w3.org/2000/svg">
      <ellipse cx="100" cy="205" rx="55" ry="8" fill="#00000022"/>
      <line x1="100" y1="30" x2="100" y2="45" stroke="#333" stroke-width="2"/>
      <circle cx="100" cy="27" r="5" fill="#e8e8e8" stroke="#333" stroke-width="2"/>
      <ellipse cx="100" cy="100" rx="60" ry="58" fill="white" stroke="#333" stroke-width="3"/>
      <ellipse cx="100" cy="100" rx="48" ry="46" fill="#a8d8f5" opacity="0.9"/>
      <ellipse cx="88" cy="88" rx="14" ry="18" fill="white" opacity="0.5"/>
      {eyes.get(mood, eyes["happy"])}
      <circle cx="75" cy="108" r="6" fill="#ffb3c6" opacity="0.7"/>
      <circle cx="125" cy="108" r="6" fill="#ffb3c6" opacity="0.7"/>
      {mouth.get(mood, mouth["happy"])}
      <ellipse cx="100" cy="170" rx="45" ry="35" fill="white" stroke="#333" stroke-width="3"/>
      <ellipse cx="55" cy="150" rx="12" ry="18" fill="white" stroke="#333" stroke-width="3"/>
      <ellipse cx="145" cy="150" rx="12" ry="18" fill="white" stroke="#333" stroke-width="3"/>
    </svg>'''

def duck_svg(mood="happy"):
    eyes = {
        "happy": '<circle cx="80" cy="110" r="7" fill="#3d1f0a"/><circle cx="130" cy="110" r="7" fill="#3d1f0a"/>',
        "excited": '<circle cx="80" cy="110" r="9" fill="#3d1f0a"/><circle cx="82" cy="107" r="3" fill="white"/><circle cx="130" cy="110" r="9" fill="#3d1f0a"/><circle cx="132" cy="107" r="3" fill="white"/>',
        "thinking": '<circle cx="80" cy="112" r="6" fill="#3d1f0a"/><path d="M124 108 L136 112" stroke="#3d1f0a" stroke-width="3"/>',
        "sad": '<path d="M74 112 Q80 118 86 112" stroke="#3d1f0a" stroke-width="3" fill="none"/><path d="M124 112 Q130 118 136 112" stroke="#3d1f0a" stroke-width="3" fill="none"/>',
        "sleep": '<path d="M74 112 L86 112" stroke="#3d1f0a" stroke-width="3"/><path d="M124 112 L136 112" stroke="#3d1f0a" stroke-width="3"/>',
    }
    mouth = {
        "happy": '<ellipse cx="105" cy="140" rx="22" ry="10" fill="#ff9642" stroke="#3d1f0a" stroke-width="2"/><path d="M92 143 Q105 155 118 143" fill="white" stroke="#3d1f0a" stroke-width="1.5"/>',
        "excited": '<ellipse cx="105" cy="142" rx="24" ry="14" fill="#ff9642" stroke="#3d1f0a" stroke-width="2"/><path d="M88 145 Q105 165 122 145" fill="#ff6666"/>',
        "thinking": '<ellipse cx="105" cy="140" rx="20" ry="8" fill="#ff9642" stroke="#3d1f0a" stroke-width="2"/>',
        "sad": '<ellipse cx="105" cy="145" rx="20" ry="8" fill="#ff9642" stroke="#3d1f0a" stroke-width="2"/><path d="M95 148 Q105 140 115 148" stroke="#3d1f0a" stroke-width="2" fill="none"/>',
        "sleep": '<ellipse cx="105" cy="142" rx="20" ry="7" fill="#ff9642" stroke="#3d1f0a" stroke-width="2"/>',
    }
    return f'''
    <svg viewBox="0 0 220 220" xmlns="http://www.w3.org/2000/svg">
      <ellipse cx="110" cy="205" rx="70" ry="8" fill="#00000022"/>
      <ellipse cx="105" cy="120" rx="85" ry="80" fill="#ffd447" stroke="#5c2a0e" stroke-width="4"/>
      <ellipse cx="80" cy="90" rx="30" ry="35" fill="#ffe066" opacity="0.6"/>
      {eyes.get(mood, eyes["happy"])}
      {mouth.get(mood, mouth["happy"])}
      <ellipse cx="55" cy="170" rx="18" ry="12" fill="#ffd447" stroke="#5c2a0e" stroke-width="3"/>
      <ellipse cx="155" cy="170" rx="18" ry="12" fill="#ffd447" stroke="#5c2a0e" stroke-width="3"/>
      <path d="M85 200 L95 205 L105 200" stroke="#ff9642" stroke-width="4" fill="none"/>
      <path d="M115 200 L125 205 L135 200" stroke="#ff9642" stroke-width="4" fill="none"/>
    </svg>'''

def frog_cat_svg(mood="happy"):
    eyes = {
        "happy": '<circle cx="78" cy="115" r="8" fill="#1a1a1a"/><circle cx="80" cy="112" r="3" fill="white"/><circle cx="132" cy="115" r="8" fill="#1a1a1a"/><circle cx="134" cy="112" r="3" fill="white"/>',
        "excited": '<path d="M70 118 L86 108 L70 108 Z" fill="#1a1a1a"/><path d="M140 118 L124 108 L140 108 Z" fill="#1a1a1a"/>',
        "thinking": '<circle cx="78" cy="115" r="6" fill="#1a1a1a"/><path d="M124 113 L140 115" stroke="#1a1a1a" stroke-width="3"/>',
        "sad": '<path d="M70 118 Q78 125 86 118" stroke="#1a1a1a" stroke-width="3" fill="none"/><path d="M124 118 Q132 125 140 118" stroke="#1a1a1a" stroke-width="3" fill="none"/>',
        "sleep": '<path d="M70 115 L86 115" stroke="#1a1a1a" stroke-width="3"/><path d="M124 115 L140 115" stroke="#1a1a1a" stroke-width="3"/>',
    }
    mouth = {
        "happy": '<path d="M95 138 Q105 145 115 138" stroke="#1a1a1a" stroke-width="2" fill="none"/><path d="M90 135 L95 138 M120 135 L115 138" stroke="#1a1a1a" stroke-width="2"/>',
        "excited": '<ellipse cx="105" cy="140" rx="8" ry="6" fill="#ff6b8a"/>',
        "thinking": '<circle cx="105" cy="138" r="2" fill="#1a1a1a"/>',
        "sad": '<path d="M95 142 Q105 135 115 142" stroke="#1a1a1a" stroke-width="2" fill="none"/>',
        "sleep": '<path d="M100 140 Q105 143 110 140" stroke="#1a1a1a" stroke-width="2" fill="none"/>',
    }
    return f'''
    <svg viewBox="0 0 220 220" xmlns="http://www.w3.org/2000/svg">
      <ellipse cx="110" cy="205" rx="70" ry="8" fill="#00000022"/>
      <ellipse cx="105" cy="130" rx="75" ry="70" fill="white" stroke="#3d3d3d" stroke-width="3"/>
      <path d="M30 85 Q30 20 105 15 Q180 20 180 85 Q180 100 165 105 L45 105 Q30 100 30 85 Z" fill="#8ec972" stroke="#3d3d3d" stroke-width="3"/>
      <circle cx="55" cy="55" r="18" fill="#8ec972" stroke="#3d3d3d" stroke-width="3"/>
      <circle cx="55" cy="55" r="9" fill="#1a1a1a"/>
      <circle cx="155" cy="55" r="18" fill="#8ec972" stroke="#3d3d3d" stroke-width="3"/>
      <circle cx="155" cy="55" r="9" fill="#1a1a1a"/>
      <path d="M85 90 Q105 100 125 90" stroke="#3d3d3d" stroke-width="2" fill="none"/>
      {eyes.get(mood, eyes["happy"])}
      <ellipse cx="60" cy="128" rx="10" ry="6" fill="#ffb3c6" opacity="0.8"/>
      <ellipse cx="150" cy="128" rx="10" ry="6" fill="#ffb3c6" opacity="0.8"/>
      {mouth.get(mood, mouth["happy"])}
      <line x1="45" y1="130" x2="30" y2="128" stroke="#3d3d3d" stroke-width="2"/>
      <line x1="45" y1="135" x2="30" y2="138" stroke="#3d3d3d" stroke-width="2"/>
      <line x1="165" y1="130" x2="180" y2="128" stroke="#3d3d3d" stroke-width="2"/>
      <line x1="165" y1="135" x2="180" y2="138" stroke="#3d3d3d" stroke-width="2"/>
    </svg>'''

def shark_cat_svg(mood="happy"):
    eyes = {
        "happy": '<path d="M70 115 Q80 105 90 115" stroke="#1a1a1a" stroke-width="3" fill="none"/><path d="M120 115 Q130 105 140 115" stroke="#1a1a1a" stroke-width="3" fill="none"/>',
        "excited": '<path d="M65 118 L85 105 L85 118 Z M85 105 L90 118" stroke="#1a1a1a" stroke-width="2.5" fill="#1a1a1a"/><path d="M125 118 L120 105 L130 118 Z" stroke="#1a1a1a" stroke-width="2.5" fill="#1a1a1a"/>',
        "thinking": '<circle cx="80" cy="115" r="5" fill="#1a1a1a"/><circle cx="130" cy="115" r="5" fill="#1a1a1a"/>',
        "sad": '<path d="M70 118 Q80 125 90 118" stroke="#1a1a1a" stroke-width="3" fill="none"/><path d="M120 118 Q130 125 140 118" stroke="#1a1a1a" stroke-width="3" fill="none"/>',
        "sleep": '<path d="M70 115 L90 115" stroke="#1a1a1a" stroke-width="3"/><path d="M120 115 L140 115" stroke="#1a1a1a" stroke-width="3"/>',
    }
    mouth = {
        "happy": '<path d="M98 140 Q105 145 112 140" stroke="#1a1a1a" stroke-width="2" fill="none"/>',
        "excited": '<ellipse cx="105" cy="142" rx="6" ry="4" fill="#ff6b8a"/>',
        "thinking": '<circle cx="105" cy="140" r="2" fill="#1a1a1a"/>',
        "sad": '<path d="M98 143 Q105 138 112 143" stroke="#1a1a1a" stroke-width="2" fill="none"/>',
        "sleep": '<path d="M100 141 Q105 144 110 141" stroke="#1a1a1a" stroke-width="2" fill="none"/>',
    }
    return f'''
    <svg viewBox="0 0 220 220" xmlns="http://www.w3.org/2000/svg">
      <ellipse cx="110" cy="205" rx="70" ry="8" fill="#00000022"/>
      <path d="M170 30 L200 20 L185 55 Z" fill="#7ba9c7" stroke="#3d3d3d" stroke-width="3"/>
      <ellipse cx="105" cy="130" rx="75" ry="70" fill="white" stroke="#3d3d3d" stroke-width="3"/>
      <path d="M30 90 Q25 20 105 15 Q185 20 180 90 Q180 105 165 108 L45 108 Q30 105 30 90 Z" fill="#7ba9c7" stroke="#3d3d3d" stroke-width="3"/>
      <path d="M55 100 L60 90 L65 100 L70 90 L75 100 L80 90 L85 100 L90 90 L95 100 L100 90 L105 100 L110 90 L115 100 L120 90 L125 100 L130 90 L135 100 L140 90 L145 100 L150 90 L155 100" stroke="white" stroke-width="3" fill="none"/>
      {eyes.get(mood, eyes["happy"])}
      <ellipse cx="65" cy="130" rx="10" ry="6" fill="#ffb3c6" opacity="0.8"/>
      <ellipse cx="145" cy="130" rx="10" ry="6" fill="#ffb3c6" opacity="0.8"/>
      {mouth.get(mood, mouth["happy"])}
      <path d="M25 130 L15 150 L35 145 Z" fill="#7ba9c7" stroke="#3d3d3d" stroke-width="3"/>
      <path d="M185 130 L195 150 L175 145 Z" fill="#7ba9c7" stroke="#3d3d3d" stroke-width="3"/>
    </svg>'''

def banana_cat_svg(mood="happy"):
    eyes = {
        "happy": '<ellipse cx="82" cy="110" rx="8" ry="10" fill="#1a1a1a"/><ellipse cx="84" cy="106" rx="3" ry="4" fill="white"/><ellipse cx="128" cy="110" rx="8" ry="10" fill="#1a1a1a"/><ellipse cx="130" cy="106" rx="3" ry="4" fill="white"/>',
        "excited": '<ellipse cx="82" cy="110" rx="10" ry="12" fill="#1a1a1a"/><circle cx="85" cy="105" r="4" fill="white"/><ellipse cx="128" cy="110" rx="10" ry="12" fill="#1a1a1a"/><circle cx="131" cy="105" r="4" fill="white"/>',
        "thinking": '<ellipse cx="82" cy="112" rx="6" ry="8" fill="#1a1a1a"/><ellipse cx="128" cy="112" rx="6" ry="8" fill="#1a1a1a"/>',
        "sad": '<ellipse cx="82" cy="112" rx="8" ry="10" fill="#1a1a1a"/><ellipse cx="128" cy="112" rx="8" ry="10" fill="#1a1a1a"/><path d="M80 125 Q82 135 78 138" stroke="#87ceeb" stroke-width="2" fill="none"/>',
        "sleep": '<path d="M74 110 Q82 118 90 110" stroke="#1a1a1a" stroke-width="3" fill="none"/><path d="M120 110 Q128 118 136 110" stroke="#1a1a1a" stroke-width="3" fill="none"/>',
    }
    mouth = {
        "happy": '<path d="M100 128 L105 132 L110 128" stroke="#1a1a1a" stroke-width="2" fill="none"/>',
        "excited": '<path d="M98 128 Q105 138 112 128" stroke="#1a1a1a" stroke-width="2" fill="#ff6b8a"/>',
        "thinking": '<circle cx="105" cy="130" r="1.5" fill="#1a1a1a"/>',
        "sad": '<path d="M100 135 Q105 128 110 135" stroke="#1a1a1a" stroke-width="2" fill="none"/>',
        "sleep": '<path d="M102 132 Q105 135 108 132" stroke="#1a1a1a" stroke-width="2" fill="none"/>',
    }
    return f'''
    <svg viewBox="0 0 220 240" xmlns="http://www.w3.org/2000/svg">
      <ellipse cx="110" cy="225" rx="70" ry="8" fill="#00000022"/>
      <path d="M95 15 L115 15 L120 40 L100 45 L90 35 Z" fill="#8b6f47" stroke="#3d3d3d" stroke-width="2"/>
      <path d="M50 60 Q40 130 60 200 Q90 220 155 215 Q180 180 175 90 Q170 45 130 40 Q90 45 50 60 Z" fill="#ffe066" stroke="#3d3d3d" stroke-width="3"/>
      <ellipse cx="105" cy="120" rx="55" ry="50" fill="#fff5e0" stroke="#3d3d3d" stroke-width="2"/>
      <ellipse cx="105" cy="90" rx="42" ry="35" fill="white" stroke="#3d3d3d" stroke-width="2"/>
      <path d="M65 75 L60 55 L80 68 Z" fill="#d4a574" stroke="#3d3d3d" stroke-width="2"/>
      <path d="M145 75 L150 55 L130 68 Z" fill="#d4a574" stroke="#3d3d3d" stroke-width="2"/>
      {eyes.get(mood, eyes["happy"])}
      <ellipse cx="105" cy="120" rx="4" ry="3" fill="#ff9999"/>
      <ellipse cx="70" cy="118" rx="8" ry="5" fill="#ffb3c6" opacity="0.7"/>
      <ellipse cx="140" cy="118" rx="8" ry="5" fill="#ffb3c6" opacity="0.7"/>
      {mouth.get(mood, mouth["happy"])}
      <path d="M100 175 L105 185 L110 175" stroke="#8b6f47" stroke-width="3" fill="none"/>
      <path d="M95 180 L100 175 M115 175 L120 180" stroke="#8b6f47" stroke-width="3" fill="none"/>
    </svg>'''

def puppy_svg(mood="happy"):
    eyes = {
        "happy": '<circle cx="75" cy="110" r="8" fill="#1a1a1a"/><circle cx="135" cy="110" r="8" fill="#1a1a1a"/>',
        "excited": '<circle cx="75" cy="110" r="10" fill="#1a1a1a"/><circle cx="77" cy="107" r="4" fill="white"/><circle cx="135" cy="110" r="10" fill="#1a1a1a"/><circle cx="137" cy="107" r="4" fill="white"/>',
        "thinking": '<circle cx="75" cy="112" r="6" fill="#1a1a1a"/><circle cx="135" cy="112" r="6" fill="#1a1a1a"/>',
        "sad": '<path d="M67 115 Q75 122 83 115" stroke="#1a1a1a" stroke-width="3" fill="none"/><path d="M127 115 Q135 122 143 115" stroke="#1a1a1a" stroke-width="3" fill="none"/>',
        "sleep": '<path d="M67 110 L83 110" stroke="#1a1a1a" stroke-width="3"/><path d="M127 110 L143 110" stroke="#1a1a1a" stroke-width="3"/>',
    }
    mouth = {
        "happy": '<circle cx="105" cy="135" r="6" fill="#1a1a1a"/><path d="M95 145 Q105 152 115 145" stroke="#1a1a1a" stroke-width="2" fill="none"/>',
        "excited": '<circle cx="105" cy="135" r="7" fill="#1a1a1a"/><path d="M90 148 Q105 160 120 148" stroke="#1a1a1a" stroke-width="2" fill="#ff6b8a"/>',
        "thinking": '<circle cx="105" cy="135" r="5" fill="#1a1a1a"/>',
        "sad": '<circle cx="105" cy="135" r="6" fill="#1a1a1a"/><path d="M95 150 Q105 143 115 150" stroke="#1a1a1a" stroke-width="2" fill="none"/>',
        "sleep": '<circle cx="105" cy="135" r="5" fill="#1a1a1a"/>',
    }
    return f'''
    <svg viewBox="0 0 220 220" xmlns="http://www.w3.org/2000/svg">
      <ellipse cx="110" cy="205" rx="70" ry="8" fill="#00000022"/>
      <path d="M35 40 L20 100 L55 95 L60 55 Z" fill="#1a1a1a"/>
      <path d="M175 40 L190 100 L155 95 L150 55 Z" fill="#1a1a1a"/>
      <path d="M85 15 L95 30 L105 15 L115 30 L125 15" stroke="#1a1a1a" stroke-width="4" fill="#1a1a1a"/>
      <ellipse cx="105" cy="115" rx="70" ry="65" fill="white" stroke="#1a1a1a" stroke-width="3"/>
      {eyes.get(mood, eyes["happy"])}
      <ellipse cx="60" cy="130" rx="12" ry="7" fill="#ffb3c6" opacity="0.8"/>
      <ellipse cx="150" cy="130" rx="12" ry="7" fill="#ffb3c6" opacity="0.8"/>
      {mouth.get(mood, mouth["happy"])}
    </svg>'''

CHARACTERS = {
    "الفلكي 🚀": {"fn": astronaut_svg, "color": "#a8d8f5"},
    "البطة 🐥": {"fn": duck_svg, "color": "#ffd447"},
    "الضفدع 🐸": {"fn": frog_cat_svg, "color": "#8ec972"},
    "القرش 🦈": {"fn": shark_cat_svg, "color": "#7ba9c7"},
    "الموزة 🍌": {"fn": banana_cat_svg, "color": "#ffe066"},
    "الجرو 🐶": {"fn": puppy_svg, "color": "#f5f5f5"},
}

# ═══════════════════════════════════════════════════════════
# ردود المساعد المرتبطة بكل زر
# ═══════════════════════════════════════════════════════════
def build_reactions(char_name, user_name):
    return {
        "welcome": ("happy", f"مرحباً {user_name}! أنا {char_name} 💖 مستعد أساعدك بمكتبتك!"),
        "add_book": ("excited", f"وااو {user_name}! كتاب جديد؟ خلينا نضيفه بسرعة! 📖✨"),
        "book_added": ("excited", f"تمام {user_name}! أضفت الكتاب بنجاح 🎉 استمر بالقراءة!"),
        "search": ("thinking", f"همم... خليني أدور لك {user_name} 🔎"),
        "search_empty": ("sad", f"معليش {user_name}، ما لقيت شي بهذا الاسم 😢"),
        "search_found": ("happy", f"لقيت لك نتائج {user_name}! شوفها فوق ⬆️"),
        "delete": ("sad", f"طيب {user_name}... حذفت الكتاب 🥺 لكن ممكن نضيف غيره!"),
        "mark_read": ("excited", f"مبروك {user_name}! خلصت كتاب جديد 🏆📚"),
        "mark_unread": ("thinking", f"رجعناه للمكتبة {user_name}، تقدر تقراه لاحقاً 📖"),
        "clear_all": ("sad", f"مسحنا كل شي {user_name}... بداية جديدة 🌱"),
        "empty_input": ("sad", f"لازم تكتب اسم الكتاب أول {user_name} 💭"),
        "stats": ("happy", f"إحصائياتك رائعة {user_name}! استمر 📊✨"),
        "help": ("thinking", f"طبعاً {user_name}! أشرح لك كل الأزرار 👇"),
        "idle": ("sleep", f"...زززز {user_name} موجود؟ 💤"),
    }

# ═══════════════════════════════════════════════════════════
# دليل المشروع (المساعد يعرفه)
# ═══════════════════════════════════════════════════════════
PROJECT_GUIDE = """
### 📚 دليل مشروع مكتبتي
- **➕ إضافة كتاب**: اكتب اسم الكتاب والمؤلف بالشريط الجانبي واضغط الزر.
- **🔎 بحث**: اكتب أي كلمة من اسم الكتاب أو المؤلف.
- **✅ قرأته / ↩️ لم أقرأه**: بجانب كل كتاب لتغيير الحالة.
- **🗑️ حذف**: يمسح كتاب واحد فقط.
- **🧹 مسح الكل**: يفرّغ المكتبة بالكامل.
- **📊 الإحصائيات**: عدد الكتب والمقروء منها.
"""

# ═══════════════════════════════════════════════════════════
# CSS - رسائل واضحة + شخصية 3D ثابتة
# ═══════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
html, body, [class*="css"] { font-family: 'Cairo', sans-serif !important; direction: rtl; }

.main .block-container { padding-top: 2rem; padding-bottom: 200px; }

/* بطاقة الكتاب */
.book-card {
  background: linear-gradient(135deg, #fff 0%, #fef6e4 100%);
  border: 2px solid #f0d78c;
  border-radius: 14px; padding: 14px; margin-bottom: 10px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.08);
}
.book-card h4 { margin: 0; color: #333; }
.book-card .meta { color: #888; font-size: 13px; margin-top: 4px; }
.badge-read { background:#4ade80; color:white; padding:3px 10px; border-radius:20px; font-size:12px; }
.badge-unread { background:#fbbf24; color:white; padding:3px 10px; border-radius:20px; font-size:12px; }

/* الشخصية العائمة 3D */
.mascot-box {
  position: fixed; bottom: 20px; left: 20px; z-index: 9999;
  width: 180px; text-align: center;
  animation: float 3s ease-in-out infinite;
  filter: drop-shadow(0 15px 20px rgba(0,0,0,0.25));
  transform-style: preserve-3d;
  transform: perspective(600px) rotateY(-8deg) rotateX(3deg);
}
.mascot-box svg { width: 140px; height: auto; }
@keyframes float {
  0%,100% { transform: perspective(600px) rotateY(-8deg) rotateX(3deg) translateY(0); }
  50%     { transform: perspective(600px) rotateY(-8deg) rotateX(3deg) translateY(-12px); }
}

/* فقاعة الكلام */
.speech {
  background: white; color: #2d2d2d;
  border: 2.5px solid #333; border-radius: 18px;
  padding: 10px 14px; font-size: 14px; font-weight: 600;
  margin-bottom: 8px; position: relative;
  box-shadow: 0 6px 14px rgba(0,0,0,0.15);
  min-height: 50px;
}
.speech::after {
  content: ''; position: absolute; bottom: -12px; right: 30px;
  border: 12px solid transparent; border-top-color: #333;
}
.speech::before {
  content: ''; position: absolute; bottom: -8px; right: 32px;
  border: 10px solid transparent; border-top-color: white; z-index: 2;
}

/* شريط جانبي */
[data-testid="stSidebar"] {
  background: linear-gradient(180deg, #fef6e4 0%, #ffe8cc 100%);
}
.stButton>button {
  border-radius: 12px; font-weight: 700; border: 2px solid #333;
  background: #ffd447; color: #333; transition: all .2s;
}
.stButton>button:hover { transform: translateY(-2px); box-shadow: 0 6px 0 #333; }
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════
# حالة الجلسة
# ═══════════════════════════════════════════════════════════
if "books" not in st.session_state: st.session_state.books = []
if "mood" not in st.session_state: st.session_state.mood = "happy"
if "message" not in st.session_state: st.session_state.message = ""
if "setup_done" not in st.session_state: st.session_state.setup_done = False

# ═══════════════════════════════════════════════════════════
# نافذة الإعداد الأولى (اختيار الشخصية)
# ═══════════════════════════════════════════════════════════
if not st.session_state.setup_done:
    st.title("🌟 مرحباً بك في مكتبتي!")
    st.markdown("### اختر رفيقك الصغير قبل ما نبدأ 💖")

    cols = st.columns(3)
    for i, (name, data) in enumerate(CHARACTERS.items()):
        with cols[i % 3]:
            st.markdown(f'<div style="text-align:center;background:{data["color"]}33;padding:15px;border-radius:20px;border:3px solid {data["color"]};margin-bottom:10px;">{data["fn"]("happy")}<h3>{name}</h3></div>', unsafe_allow_html=True)
            if st.button(f"اختر {name}", key=f"pick_{name}", use_container_width=True):
                st.session_state.picked_char = name

    if "picked_char" in st.session_state:
        st.divider()
        st.markdown(f"### اخترت: **{st.session_state.picked_char}** 🎉")
        c1, c2 = st.columns(2)
        with c1:
            char_name = st.text_input("سمّي شخصيتك ✨", value=st.session_state.picked_char.split()[0])
        with c2:
            user_name = st.text_input("شنو أنادي عليك؟ 💝", value="صديقي")
        if st.button("🚀 يلا نبدأ!", use_container_width=True, type="primary"):
            st.session_state.char_key = st.session_state.picked_char
            st.session_state.char_name = char_name or "صديقي"
            st.session_state.user_name = user_name or "صديقي"
            st.session_state.setup_done = True
            st.session_state.mood, st.session_state.message = ("happy", f"مرحباً {user_name}! أنا {char_name} 💖")
            st.rerun()
    st.stop()

# ═══════════════════════════════════════════════════════════
# التطبيق الرئيسي
# ═══════════════════════════════════════════════════════════
REACT = build_reactions(st.session_state.char_name, st.session_state.user_name)

def react(key):
    mood, msg = REACT[key]
    st.session_state.mood = mood
    st.session_state.message = msg

st.title(f"📚 مكتبة {st.session_state.user_name}")
st.caption(f"مع رفيقك {st.session_state.char_name} 💫")

# ─── الشريط الجانبي ─────────────────────────────
with st.sidebar:
    st.header("⚙️ الأدوات")

    if st.button("🔄 غيّر الشخصية", use_container_width=True):
        st.session_state.setup_done = False
        st.rerun()

    st.divider()
    st.subheader("➕ إضافة كتاب")
    title = st.text_input("اسم الكتاب", key="new_title")
    author = st.text_input("المؤلف", key="new_author")

    if st.button("➕ أضف الكتاب", use_container_width=True, type="primary"):
        if title.strip():
            st.session_state.books.append({
                "title": title.strip(),
                "author": author.strip() or "غير معروف",
                "read": False,
                "date": datetime.now().strftime("%Y-%m-%d"),
            })
            react("book_added")
            st.rerun()
        else:
            react("empty_input")

    st.divider()
    st.subheader("🔎 بحث")
    query = st.text_input("ابحث عن كتاب أو مؤلف", key="search_q")
    if st.button("🔍 ابحث", use_container_width=True):
        if query.strip():
            react("search")
        else:
            react("empty_input")

    st.divider()
    if st.button("🧹 مسح كل الكتب", use_container_width=True):
        st.session_state.books = []
        react("clear_all")
        st.rerun()

    if st.button("❓ شرح المشروع", use_container_width=True):
        react("help")

# ─── الإحصائيات ─────────────────────────────
total = len(st.session_state.books)
read_count = sum(1 for b in st.session_state.books if b["read"])
c1, c2, c3 = st.columns(3)
c1.metric("📚 المجموع", total)
c2.metric("✅ مقروء", read_count)
c3.metric("📖 متبقي", total - read_count)

st.divider()

# ─── دليل المشروع ─────────────────────────────
if st.session_state.message and "أشرح" in st.session_state.message:
    with st.expander("📘 دليل الاستخدام", expanded=True):
        st.markdown(PROJECT_GUIDE)

# ─── قائمة الكتب ─────────────────────────────
books_to_show = st.session_state.books
if query.strip():
    q = query.strip().lower()
    books_to_show = [b for b in st.session_state.books if q in b["title"].lower() or q in b["author"].lower()]
    if books_to_show and st.session_state.mood == "thinking":
        react("search_found")
    elif not books_to_show and st.session_state.mood == "thinking":
        react("search_empty")

if not st.session_state.books:
    st.info("📭 مكتبتك فاضية... أضف أول كتاب من الشريط الجانبي!")
elif not books_to_show:
    st.warning("🔍 ما لقيت نتائج مطابقة.")
else:
    st.subheader("📖 كتبك")
    for i, book in enumerate(st.session_state.books):
        if book not in books_to_show: continue
        badge = '<span class="badge-read">✅ مقروء</span>' if book["read"] else '<span class="badge-unread">📖 قيد القراءة</span>'
        st.markdown(f'''
        <div class="book-card">
          <h4>{book["title"]}</h4>
          <div class="meta">✍️ {book["author"]} · 📅 {book["date"]} {badge}</div>
        </div>''', unsafe_allow_html=True)
        cc1, cc2, cc3 = st.columns([1,1,4])
        with cc1:
            if book["read"]:
                if st.button("↩️ لم أقرأه", key=f"u{i}"):
                    st.session_state.books[i]["read"] = False
                    react("mark_unread"); st.rerun()
            else:
                if st.button("✅ قرأته", key=f"r{i}"):
                    st.session_state.books[i]["read"] = True
                    react("mark_read"); st.rerun()
        with cc2:
            if st.button("🗑️ حذف", key=f"d{i}"):
                st.session_state.books.pop(i)
                react("delete"); st.rerun()

# ─── الشخصية العائمة ─────────────────────────────
char_fn = CHARACTERS[st.session_state.char_key]["fn"]
svg = char_fn(st.session_state.mood)
msg = st.session_state.message or REACT["welcome"][1]

st.markdown(f'''
<div class="mascot-box">
  <div class="speech">{msg}</div>
  {svg}
</div>
''', unsafe_allow_html=True)
