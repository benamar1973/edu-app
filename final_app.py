import streamlit as st
from urllib.parse import quote
import streamlit.components.v1 as components

st.set_page_config(page_title="منصة تعليمية", page_icon="📚", layout="wide")

# رابط الخلفية - يمكنك تغييره
bg_url = "https://images.unsplash.com/photo-1524995997946-a1c2e315a42f?q=80&w=2070&auto=format"

# التنسيقات (تم تبسيطها لتجنب الأخطاء)
st.markdown(f"""
<style>
    /* خط Tajawal */
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;700&display=swap');
    html, body, div, p, button, input, .stTextInput, .stButton, .stMarkdown {{
        font-family: 'Tajawal', sans-serif;
    }}
    
    /* خلفية الصورة */
    .stApp {{
        background: linear-gradient(rgba(0,0,0,0.7), rgba(0,0,0,0.8)), url("{bg_url}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}
    
    /* أزرار */
    .stButton > button {{
        background: #1E88E5;
        color: white;
        border-radius: 30px;
        padding: 10px;
        font-size: 18px;
        width: 100%;
    }}
    
    /* حقل إدخال */
    .stTextInput > div > div > input {{
        background: rgba(255,255,255,0.1);
        border-radius: 30px;
        color: white;
        padding: 10px;
    }}
    
    /* عنوان */
    .main-title {{
        text-align: center;
        font-size: 3rem;
        color: #FFD166;
        margin-bottom: 0;
    }}
    
    /* شعار */
    .slogan {{
        text-align: center;
        font-size: 1.2rem;
        color: white;
        margin-bottom: 30px;
    }}
    
    /* إخفاء التذييل */
    footer, .viewerBadge_container__r5tak {{
        display: none !important;
    }}
</style>
""", unsafe_allow_html=True)

# المحتوى
st.markdown('<div class="main-title">📚 منصة تعليمية ذكية</div>', unsafe_allow_html=True)
st.markdown('<div class="slogan">العلم نور، والإصرار طريق النجاح</div>', unsafe_allow_html=True)

topic = st.text_input("", placeholder="اكتب المادة والدرس... (مثال: فيزياء الكم)")

col1, col2 = st.columns(2)
with col1:
    if st.button("📖 درس نصي"):
        if topic:
            url = f"https://www.google.com/search?q={quote(topic + ' شرح')}"
            components.html(f"<script>window.open('{url}');</script>", height=0)
            st.success("تم فتح الدرس النصي")
        else:
            st.warning("اكتب الدرس أولاً")

with col2:
    if st.button("🎥 فيديو تعليمي"):
        if topic:
            url = f"https://www.youtube.com/results?search_query={quote(topic + ' شرح')}"
            components.html(f"<script>window.open('{url}');</script>", height=0)
            st.success("تم فتح الفيديو")
        else:
            st.warning("اكتب الدرس أولاً")

# حفظ آخر درس
if topic and ('last_topic' not in st.session_state or st.session_state.last_topic != topic):
    st.session_state.last_topic = topic
    if 'history' not in st.session_state:
        st.session_state.history = []
    st.session_state.history.insert(0, topic)
    st.session_state.history = st.session_state.history[:5]

# عرض آخر درس
if 'last_topic' in st.session_state:
    st.info(f"📌 آخر درس: {st.session_state.last_topic}")

# قائمة الدروس المحفوظة
st.markdown("---")
st.markdown("### 📚 دروسي المحفوظة")
if 'history' in st.session_state and st.session_state.history:
    for i, item in enumerate(st.session_state.history):
        st.markdown(f"- {item}")
else:
    st.caption("لا توجد دروس محفوظة بعد")