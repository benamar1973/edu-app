import streamlit as st
import requests
from urllib.parse import quote

# ================== إعدادات الصفحة ==================
st.set_page_config(page_title="منصة تعليمية ذكية", page_icon="📚", layout="wide")

# خلفية علمية
bg_url = "https://images.unsplash.com/photo-1524995997946-a1c2e315a42f?q=80&w=2070&auto=format"

# التنسيقات (تشمل إخفاء الإشهار والشريط السفلي للمنصة بشكل صارم)
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;700&display=swap');
    * {{ font-family: 'Tajawal', sans-serif; }}
    
    /* إخفاء الهيدر والفوتر وشريط المنصة السفلي (الإشهار) نهائياً */
    header, footer, 
    [data-testid="stHeader"], 
    [data-testid="stFooter"], 
    [data-testid="stStatusWidget"], 
    .viewerBadge_container__1QSob, 
    .stAppDeployDropdown,
    [class^="viewerBadge_"] {{ 
        display: none !important; 
        visibility: hidden !important;
        height: 0 !important;
    }}
    
    .stApp {{ background: linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.7)), url("{bg_url}"); background-size: cover; background-attachment: fixed; }}
    .stTextInput > div > div > input {{ background: white; border-radius: 48px; padding: 12px 20px; color: black; text-align: right; }}
    .stButton > button {{ background: linear-gradient(90deg, #1E88E5, #6A1B9A); color: white; border-radius: 40px; padding: 12px; font-weight: bold; width: 100%; }}
    .main-title {{ text-align: center; font-size: 3rem; font-weight: 800; background: linear-gradient(120deg, #FFD166, #06D6A0); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }}
    .slogan {{ text-align: center; font-size: 1.2rem; color: #ddd; margin-bottom: 30px; }}
    .result-box {{ background: rgba(0,0,0,0.75); border-radius: 15px; padding: 15px; margin: 15px 0; text-align: center; }}
    .result-box a {{ color: #FFD166; font-size: 18px; text-decoration: none; }}
    .saved-lessons {{ background: rgba(0,0,0,0.5); border-radius: 15px; padding: 15px; margin-top: 30px; }}
    .saved-lessons h3 {{ color: #FFD166; text-align: center; }}
    .lesson-item {{ background: rgba(255,255,255,0.1); padding: 8px 12px; margin: 5px 0; border-radius: 10px; color: white; text-align: right; }}
</style>
""", unsafe_allow_html=True)

# العنوان
st.markdown('<div class="main-title">📚 منصة تعليمية ذكية</div>', unsafe_allow_html=True)
st.markdown('<div class="slogan">العلم نور، والإصرار طريق النجاح</div>', unsafe_allow_html=True)

# حقل الإدخال مع زر مسح
if "search_topic" not in st.session_state:
    st.session_state.search_topic = ""

col1, col2 = st.columns([5, 1])
with col1:
    topic = st.text_input("", placeholder="✏️ اكتب المادة والدرس...", label_visibility="collapsed", key="input", value=st.session_state.search_topic)
    st.session_state.search_topic = topic
with col2:
    if st.button("🗑️ مسح", use_container_width=True):
        st.session_state.search_topic = ""
        st.rerun()

if 'history' not in st.session_state:
    st.session_state.history = []

# دالة البحث عن فيديو باستخدام الـ API المحدث والرابط الصحيح
def get_youtube_link(query):
    try:
        key = st.secrets.get("YOUTUBE_API_KEY")
        if not key:
            return f"https://www.youtube.com/results?search_query={quote(query + ' شرح')}"
            
        url = "https://www.googleapis.com/youtube/v3/search"
        params = {"part": "snippet", "q": query + " شرح", "type": "video", "maxResults": 1, "key": key}
        r = requests.get(url, params=params)
        data = r.json()
        
        if "items" in data and len(data["items"]) > 0:
            video_id = data['items'][0]['id']['videoId']
            return f"https://www.youtube.com/watch?v={video_id}"
    except:
        pass
    return f"https://www.youtube.com/results?search_query={quote(query + ' شرح')}"

# دالة البحث النصي
def get_google_link(query):
    return f"https://www.google.com/search?q={quote(query + ' شرح')}"

# أزرار البحث
btn1, btn2 = st.columns(2)
with btn1:
    if st.button("📖 lesson text ", use_container_width=True):
        if topic:
            link = get_google_link(topic)
            if topic not in st.session_state.history:
                st.session_state.history.insert(0, topic)
            st.markdown(f'<div class="result-box"><a href="{link}" target="_blank">🔗 اضغط لفتح نتائج البحث</a></div>', unsafe_allow_html=True)
        else:
            st.warning("⚠️ اكتب الدرس أولاً")

with btn2:
    if st.button("🎥 فيديو تعليمي", use_container_width=True):
        if topic:
            with st.spinner("جاري البحث عن أفضل فيديو..."):
                link = get_youtube_link(topic)
            if topic not in st.session_state.history:
                st.session_state.history.insert(0, topic)
            st.markdown(f'<div class="result-box"><a href="{link}" target="_blank">🔗 اضغط لفتح الفيديو المباشر</a></div>', unsafe_allow_html=True)
        else:
            st.warning("⚠️ اكتب الدرس أولاً")

# آخر درس
if st.session_state.history:
    st.info(f"📌 آخر درس بحثت عنه: **{st.session_state.history[0]}**")

# الدروس المحفوظة
st.markdown('<div class="saved-lessons"><h3>⭐ دروسي المحفوظة</h3></div>', unsafe_allow_html=True)
if st.session_state.history:
    for i, item in enumerate(st.session_state.history):
        c1, c2 = st.columns([5, 1])
        with c1:
            st.markdown(f'<div class="lesson-item">📘 {item}</div>', unsafe_allow_html=True)
        with c2:
            if st.button("🗑️", key=f"del_{i}"):
                st.session_state.history.pop(i)
                st.rerun()
else:
    st.markdown('<div class="lesson-item" style="text-align:center;">💡 لا توجد دروس محفوظة حالياً</div>', unsafe_allow_html=True)
