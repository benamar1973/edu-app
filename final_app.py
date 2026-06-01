import streamlit as st
from urllib.parse import quote
import streamlit.components.v1 as components

st.set_page_config(page_title="منصة تعليمية", page_icon="📚", layout="wide")

# خلفية علمية
bg_url = "https://images.unsplash.com/photo-1524995997946-a1c2e315a42f?q=80&w=2070&auto=format"

# التنسيقات النهائية
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;700&display=swap');
    
    * {{
        font-family: 'Tajawal', sans-serif;
    }}
    
    .stApp {{
        background: linear-gradient(rgba(0,0,0,0.7), rgba(0,0,0,0.8)), url("{bg_url}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
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
        transition: 0.3s;
    }}
    
    .stButton > button:hover {{
        transform: scale(1.02);
        box-shadow: 0 5px 15px rgba(30,136,229,0.5);
    }}
    
    .stTextInput > div > div > input {{
        background: rgba(255,255,255,0.15);
        border: 1px solid rgba(255,255,255,0.3);
        border-radius: 48px;
        padding: 12px 20px;
        color: white;
        font-size: 16px;
        text-align: right;
    }}
    
    .main-title {{
        text-align: center;
        font-size: 3rem;
        font-weight: 800;
        background: linear-gradient(120deg, #FFD166, #06D6A0);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0;
    }}
    
    .slogan {{
        text-align: center;
        font-size: 1.2rem;
        color: #ccc;
        margin-bottom: 30px;
    }}
    
    /* تنسيق الدروس المحفوظة */
    .saved-lessons {{
        background: rgba(0,0,0,0.5);
        border-radius: 15px;
        padding: 10px;
        margin-top: 20px;
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
        font-size: 14px;
    }}
    
    /* إخفاء كل العناصر السفلية */
    footer, .viewerBadge_container__r5tak, .st-emotion-cache-1v0mbdj, 
    .st-emotion-cache-16txtl3, .st-emotion-cache-1y4p8pa, .st-emotion-cache-1r6slb0,
    [data-testid="stFooter"], [data-testid="stDecoration"] {{
        display: none !important;
    }}
</style>
""", unsafe_allow_html=True)

# إخفاء الروابط بجافا سكريبت قوي
components.html("""
<script>
    function removeAllFooters() {
        var elements = document.querySelectorAll('footer, .viewerBadge_container__r5tak, [data-testid="stFooter"]');
        elements.forEach(el => el.remove());
    }
    setInterval(removeAllFooters, 500);
    window.addEventListener('load', removeAllFooters);
</script>
""", height=0)

# المحتوى
st.markdown('<div class="main-title">📚 منصة تعليمية ذكية</div>', unsafe_allow_html=True)
st.markdown('<div class="slogan">العلم نور، والإصرار طريق النجاح</div>', unsafe_allow_html=True)

topic = st.text_input("", placeholder="✏️ اكتب المادة والدرس... (مثال: فيزياء الكم)", label_visibility="collapsed")

col1, col2 = st.columns(2)
with col1:
    if st.button("📖 درس نصي", use_container_width=True):
        if topic:
            url = f"https://www.google.com/search?q={quote(topic + ' شرح')}"
            components.html(f"<script>window.open('{url}','_blank');</script>", height=0)
            st.success("✅ تم فتح الدرس النصي")
        else:
            st.warning("⚠️ اكتب الدرس أولاً")

with col2:
    if st.button("🎥 فيديو تعليمي", use_container_width=True):
        if topic:
            url = f"https://www.youtube.com/results?search_query={quote(topic + ' شرح')}"
            components.html(f"<script>window.open('{url}','_blank');</script>", height=0)
            st.success("✅ تم فتح الفيديو")
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

# عرض آخر درس
if 'last_topic' in st.session_state and st.session_state.last_topic:
    st.info(f"📌 آخر درس بحثت عنه: **{st.session_state.last_topic}**")

# عرض الدروس المحفوظة
st.markdown("---")
st.markdown('<div class="saved-lessons"><h3>⭐ دروسي المحفوظة</h3>', unsafe_allow_html=True)

if 'history' in st.session_state and st.session_state.history:
    for item in st.session_state.history:
        st.markdown(f'<div class="lesson-item">📘 {item}</div>', unsafe_allow_html=True)
else:
    st.markdown('<div class="lesson-item">💡 لا توجد دروس محفوظة. ابحث عن درس وسيظهر هنا.</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
