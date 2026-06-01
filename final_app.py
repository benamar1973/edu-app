import streamlit as st
from urllib.parse import quote

st.set_page_config(page_title="منصة تعليمية", page_icon="📚", layout="wide")

# خلفية علمية
bg_url = "https://images.unsplash.com/photo-1524995997946-a1c2e315a42f?q=80&w=2070&auto=format"

# إخفاء كل العناصر العلوية والسفلية
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
    
    /* إخفاء كل شيء في الأعلى والأسفل */
    header, footer, .st-emotion-cache-1v0mbdj, .st-emotion-cache-16txtl3,
    .st-emotion-cache-1y4p8pa, .st-emotion-cache-1r6slb0, .viewerBadge_container__r5tak,
    [data-testid="stHeader"], [data-testid="stFooter"], .stApp header {{
        display: none !important;
    }}
    
    /* تنسيق حقل الإدخال */
    .stTextInput > div > div > input {{
        background: white;
        border: 1px solid #ccc;
        border-radius: 48px;
        padding: 12px 20px;
        color: black;
        font-size: 16px;
        text-align: right;
    }}
    
    /* تنسيق الأزرار */
    .stButton > button {{
        background: linear-gradient(90deg, #1E88E5, #6A1B9A);
        color: white;
        border: none;
        border-radius: 40px;
        padding: 12px;
        font-size: 18px;
        font-weight: bold;
        width: 100%;
    }}
    
    .main-title {{
        text-align: center;
        font-size: 3rem;
        font-weight: 800;
        background: linear-gradient(120deg, #FFD166, #06D6A0);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-top: 50px;
    }}
    
    .slogan {{
        text-align: center;
        font-size: 1.2rem;
        color: #ddd;
        margin-bottom: 30px;
    }}
    
    .saved-lessons {{
        background: rgba(0,0,0,0.6);
        border-radius: 15px;
        padding: 15px;
        margin-top: 20px;
        margin-bottom: 50px;
    }}
    
    .saved-lessons h3 {{
        color: #FFD166;
        text-align: center;
    }}
    
    .lesson-item {{
        background: rgba(255,255,255,0.15);
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

# دوال البحث
def get_text_link(q):
    return f"https://www.google.com/search?q={quote(q + ' شرح')}"

def get_video_link(q):
    return f"https://www.youtube.com/results?search_query={quote(q + ' شرح')}"

col1, col2 = st.columns(2)
with col1:
    if st.button("📖 درس نصي", use_container_width=True):
        if topic:
            link = get_text_link(topic)
            st.markdown(f'<meta http-equiv="refresh" content="0; url={link}">', unsafe_allow_html=True)
            st.success("✅ جاري تحويلك إلى الدرس النصي...")
        else:
            st.warning("⚠️ اكتب الدرس أولاً")

with col2:
    if st.button("🎥 فيديو تعليمي", use_container_width=True):
        if topic:
            link = get_video_link(topic)
            st.markdown(f'<meta http-equiv="refresh" content="0; url={link}">', unsafe_allow_html=True)
            st.success("✅ جاري تحويلك إلى الفيديو...")
        else:
            st.warning("⚠️ اكتب الدرس أولاً")

# حفظ الدروس
if topic and ('last_topic' not in st.session_state or st.session_state.last_topic != topic):
    st.session_state.last_topic = topic
    if 'history' not in st.session_state:
        st.session_state.history = []
    if topic not in st.session_state.history:
        st.session_state.history.insert(0, topic)
        st.session_state.history = st.session_state.history[:6]

if 'last_topic' in st.session_state and st.session_state.last_topic:
    st.info(f"📌 آخر درس: **{st.session_state.last_topic}**")

st.markdown("---")
st.markdown('<div class="saved-lessons"><h3>⭐ دروسي المحفوظة</h3>', unsafe_allow_html=True)

if 'history' in st.session_state and st.session_state.history:
    for item in st.session_state.history:
        st.markdown(f'<div class="lesson-item">📘 {item}</div>', unsafe_allow_html=True)
else:
    st.markdown('<div class="lesson-item">💡 لا توجد دروس محفوظة. ابحث عن درس وسيظهر هنا.</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)