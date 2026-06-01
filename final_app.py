import streamlit as st
from urllib.parse import quote

st.set_page_config(page_title="منصة تعليمية", page_icon="📚", layout="wide")

# خلفية علمية
bg_url = "https://images.unsplash.com/photo-1524995997946-a1c2e315a42f?q=80&w=2070&auto=format"

# تنسيق الصفحة
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;700&display=swap');
    
    * {{
        font-family: 'Tajawal', sans-serif;
    }}
    
    .stApp {{
        background: linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.7)), url("{bg_url}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}
    
    .stTextInput > div > div > input {{
        background: white;
        border: 1px solid #ccc;
        border-radius: 48px;
        padding: 12px 20px;
        color: black;
        font-size: 16px;
        text-align: right;
    }}
    
    .stButton > button {{
        background: linear-gradient(90deg, #1E88E5, #6A1B9A);
        color: white;
        border: none;
        border-radius: 40px;
        padding: 12px;
        font-size: 18px;
        font-weight: bold;
        width: 100%;
        margin-bottom: 10px;
    }}
    
    .main-title {{
        text-align: center;
        font-size: 3rem;
        font-weight: 800;
        background: linear-gradient(120deg, #FFD166, #06D6A0);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-top: 30px;
    }}
    
    .slogan {{
        text-align: center;
        font-size: 1.2rem;
        color: #ddd;
        margin-bottom: 30px;
    }}
    
    .result-box {{
        background: rgba(0,0,0,0.7);
        border-radius: 15px;
        padding: 15px;
        margin: 15px 0;
        text-align: center;
    }}
    
    .result-box a {{
        color: #FFD166;
        font-size: 18px;
        text-decoration: none;
        word-break: break-all;
    }}
    
    .result-box a:hover {{
        text-decoration: underline;
    }}
    
    .saved-lessons {{
        background: rgba(0,0,0,0.5);
        border-radius: 15px;
        padding: 15px;
        margin-top: 30px;
        margin-bottom: 50px;
    }}
    
    .saved-lessons h3 {{
        color: #FFD166;
        text-align: center;
    }}
    
    .lesson-item {{
        background: rgba(255,255,255,0.1);
        padding: 8px 12px;
        margin: 5px 0;
        border-radius: 10px;
        color: white;
    }}
</style>
""", unsafe_allow_html=True)

# المحتوى
st.markdown('<div class="main-title">📚 منصة تعليمية ذكية</div>', unsafe_allow_html=True)
st.markdown('<div class="slogan">العلم نور، والإصرار طريق النجاح</div>', unsafe_allow_html=True)

topic = st.text_input("", placeholder="✏️ اكتب المادة والدرس... (مثال: فيزياء الكم)", label_visibility="collapsed")

# متغيرات لحفظ الروابط
if 'text_link' not in st.session_state:
    st.session_state.text_link = ""
if 'video_link' not in st.session_state:
    st.session_state.video_link = ""

col1, col2 = st.columns(2)
with col1:
    if st.button("📖 درس نصي", use_container_width=True):
        if topic:
            st.session_state.text_link = f"https://www.google.com/search?q={quote(topic + ' شرح')}"
            st.session_state.video_link = ""
        else:
            st.warning("⚠️ اكتب الدرس أولاً")

with col2:
    if st.button("🎥 فيديو تعليمي", use_container_width=True):
        if topic:
            st.session_state.video_link = f"https://www.youtube.com/results?search_query={quote(topic + ' شرح')}"
            st.session_state.text_link = ""
        else:
            st.warning("⚠️ اكتب الدرس أولاً")

# عرض الرابط إذا وجد
if st.session_state.text_link:
    st.markdown(f"""
    <div class="result-box">
        📖 <strong>رابط الدرس النصي:</strong><br>
        <a href="{st.session_state.text_link}" target="_blank">🔗 اضغط هنا لفتح الدرس</a>
    </div>
    """, unsafe_allow_html=True)

if st.session_state.video_link:
    st.markdown(f"""
    <div class="result-box">
        🎥 <strong>رابط الفيديو التعليمي:</strong><br>
        <a href="{st.session_state.video_link}" target="_blank">🔗 اضغط هنا لفتح الفيديو</a>
    </div>
    """, unsafe_allow_html=True)

# حفظ الدروس
if topic and ('last_topic' not in st.session_state or st.session_state.last_topic != topic):
    st.session_state.last_topic = topic
    if 'history' not in st.session_state:
        st.session_state.history = []
    if topic not in st.session_state.history:
        st.session_state.history.insert(0, topic)
        st.session_state.history = st.session_state.history[:6]

if 'last_topic' in st.session_state and st.session_state.last_topic:
    st.info(f"📌 آخر درس بحثت عنه: **{st.session_state.last_topic}**")

# الدروس المحفوظة
st.markdown('<div class="saved-lessons"><h3>⭐ دروسي المحفوظة</h3>', unsafe_allow_html=True)

if 'history' in st.session_state and st.session_state.history:
    for item in st.session_state.history:
        st.markdown(f'<div class="lesson-item">📘 {item}</div>', unsafe_allow_html=True)
else:
    st.markdown('<div class="lesson-item">💡 لا توجد دروس محفوظة. ابحث عن درس وسيظهر هنا.</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)