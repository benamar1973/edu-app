import streamlit as st
from urllib.parse import quote
import datetime

st.set_page_config(page_title="منصة تعليمية", page_icon="📚", layout="wide")

bg_url = "https://images.unsplash.com/photo-1524995997946-a1c2e315a42f?q=80&w=2070&auto=format"

# تنسيق شامل + إخفاء header
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;700&display=swap');
    
    * {{
        font-family: 'Tajawal', sans-serif;
    }}
    
    /* إخفاء header و footer وكل العناصر العلوية */
    header, footer, .st-emotion-cache-1v0mbdj, .st-emotion-cache-16txtl3,
    .st-emotion-cache-1y4p8pa, .st-emotion-cache-1r6slb0, .viewerBadge_container__r5tak,
    [data-testid="stHeader"], [data-testid="stFooter"], .stApp header,
    .st-emotion-cache-12fm0u7, .st-emotion-cache-1w1c4f6 {{
        display: none !important;
    }}
    
    /* إخفاء المساحة الفارغة العلوية */
    .main .block-container {{
        padding-top: 2rem;
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
        margin-top: 0;
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
    }}
    
    .result-box a:hover {{
        text-decoration: underline;
    }}
    
    .saved-lessons {{
        background: rgba(0,0,0,0.5);
        border-radius: 15px;
        padding: 15px;
        margin-top: 30px;
        margin-bottom: 30px;
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
        display: flex;
        justify-content: space-between;
        align-items: center;
    }}
    
    .delete-btn {{
        background: #dc3545;
        color: white;
        border: none;
        border-radius: 20px;
        padding: 2px 12px;
        cursor: pointer;
        font-size: 12px;
    }}
</style>
""", unsafe_allow_html=True)

# المحتوى
st.markdown('<div class="main-title">📚 منصة تعليمية ذكية</div>', unsafe_allow_html=True)
st.markdown('<div class="slogan">العلم نور، والإصرار طريق النجاح</div>', unsafe_allow_html=True)

topic = st.text_input("", placeholder="✏️ اكتب المادة والدرس... (مثال: فيزياء الكم)", label_visibility="collapsed")

# تهيئة session state
if 'history' not in st.session_state:
    st.session_state.history = []
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
            if topic not in st.session_state.history:
                st.session_state.history.insert(0, topic)
                st.session_state.history = st.session_state.history[:10]
        else:
            st.warning("⚠️ اكتب الدرس أولاً")

with col2:
    if st.button("🎥 فيديو تعليمي", use_container_width=True):
        if topic:
            st.session_state.video_link = f"https://www.youtube.com/results?search_query={quote(topic + ' شرح')}"
            st.session_state.text_link = ""
            if topic not in st.session_state.history:
                st.session_state.history.insert(0, topic)
                st.session_state.history = st.session_state.history[:10]
        else:
            st.warning("⚠️ اكتب الدرس أولاً")

# عرض الرابط
if st.session_state.text_link:
    st.markdown(f"""
    <div class="result-box">
        📖 <strong>رابط الدرس النصي:</strong><br>
        <a href="{st.session_state.text_link}" target="_blank">🔗 اضغط هنا لفتح الدرس (يفتح في نافذة جديدة)</a>
    </div>
    """, unsafe_allow_html=True)

if st.session_state.video_link:
    st.markdown(f"""
    <div class="result-box">
        🎥 <strong>رابط الفيديو التعليمي:</strong><br>
        <a href="{st.session_state.video_link}" target="_blank">🔗 اضغط هنا لفتح الفيديو (يفتح في نافذة جديدة)</a>
    </div>
    """, unsafe_allow_html=True)

# آخر درس
if st.session_state.history:
    st.info(f"📌 آخر درس بحثت عنه: **{st.session_state.history[0]}**")

# الدروس المحفوظة + زر التحميل
st.markdown('<div class="saved-lessons"><h3>⭐ دروسي المحفوظة</h3>', unsafe_allow_html=True)

if st.session_state.history:
    # زر تحميل الدروس
    if st.button("📥 تحميل الدروس المحفوظة (ملف txt)"):
        file_content = "دروسي المحفوظة - منصة تعليمية ذكية\n"
        file_content += f"تاريخ التصدير: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        file_content += "=" * 40 + "\n\n"
        for i, item in enumerate(st.session_state.history, 1):
            file_content += f"{i}. {item}\n"
        st.download_button(
            label="✅ انقر هنا لتحميل الملف",
            data=file_content,
            file_name=f"دروسي_المحفوظة_{datetime.datetime.now().strftime('%Y%m%d')}.txt",
            mime="text/plain"
        )
    
    # عرض الدروس مع زر حذف لكل درس
    for idx, item in enumerate(st.session_state.history):
        col_a, col_b = st.columns([5, 1])
        with col_a:
            st.markdown(f'📘 {item}')
        with col_b:
            if st.button("🗑️", key=f"del_{idx}"):
                st.session_state.history.pop(idx)
                st.rerun()
else:
    st.markdown('<div class="lesson-item">💡 لا توجد دروس محفوظة. ابحث عن درس وسيظهر هنا.</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)