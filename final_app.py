import streamlit as st
from urllib.parse import quote
import requests
import streamlit.components.v1 as components
import datetime

# قراءة المفتاح من الإعدادات السرية (آمن)
YOUTUBE_API_KEY = st.secrets["YOUTUBE_API_KEY"]

# باقي الكود كما هو...
st.set_page_config(page_title="منصة تعليمية ذكية", page_icon="📚", layout="wide")

# خلفية علمية
bg_url = "https://images.unsplash.com/photo-1524995997946-a1c2e315a42f?q=80&w=2070&auto=format"

# التنسيقات
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;700&display=swap');
    
    * {{ font-family: 'Tajawal', sans-serif; }}
    
    header, footer, .st-emotion-cache-1v0mbdj, [data-testid="stHeader"], [data-testid="stFooter"] {{
        display: none !important;
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
        background: rgba(0,0,0,0.75);
        border-radius: 15px;
        padding: 15px;
        margin: 15px 0;
        text-align: center;
        border: 1px solid rgba(255,255,255,0.2);
    }}
    
    .result-box a {{
        color: #FFD166;
        font-size: 18px;
        text-decoration: none;
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
    }}
</style>
""", unsafe_allow_html=True)

# إخفاء العناصر السفلية
components.html("""
<script>
    function removeFooter() {
        const elements = ['footer', '.viewerBadge_container__r5tak', '[data-testid="stFooter"]'];
        elements.forEach(sel => {
            document.querySelectorAll(sel).forEach(el => el.remove());
        });
    }
    setInterval(removeFooter, 500);
    window.addEventListener('load', removeFooter);
</script>
""", height=0)

# المحتوى
st.markdown('<div class="main-title">📚 منصة تعليمية ذكية</div>', unsafe_allow_html=True)
st.markdown('<div class="slogan">العلم نور، والإصرار طريق النجاح</div>', unsafe_allow_html=True)

# حقل الإدخال + زر مسح
if "search_topic" not in st.session_state:
    st.session_state.search_topic = ""

col_input, col_clear = st.columns([4, 1])
with col_input:
    topic = st.text_input("", placeholder="✏️ اكتب المادة والدرس...", label_visibility="collapsed", key="search_input", value=st.session_state.search_topic)
    st.session_state.search_topic = topic

with col_clear:
    if st.button("🗑️ مسح", key="clear_btn", use_container_width=True):
        st.session_state.search_topic = ""
        st.session_state.pop("search_input", None)
        st.rerun()

if 'history' not in st.session_state:
    st.session_state.history = []

# دوال البحث
def search_youtube_video(query):
    url = "https://www.googleapis.com/youtube/v3/search"
    params = {
        "part": "snippet",
        "q": query + " شرح تعليمي",
        "type": "video",
        "maxResults": 1,
        "key": YOUTUBE_API_KEY
    }
    try:
        response = requests.get(url, params=params)
        data = response.json()
        if "items" in data and len(data["items"]) > 0:
            video_id = data["items"][0]["id"]["videoId"]
            return f"https://www.youtube.com/watch?v={video_id}"
    except:
        pass
    return None

def search_text_google(query):
    return f"https://www.google.com/search?q={quote(query + ' شرح درس تعليمي')}"

# الأزرار
col1, col2 = st.columns(2)
with col1:
    if st.button("📖 درس نصي", use_container_width=True):
        if topic:
            with st.spinner("🔍 جاري البحث..."):
                link = search_text_google(topic)
                if link:
                    if topic not in st.session_state.history:
                        st.session_state.history.insert(0, topic)
                        st.session_state.history = st.session_state.history[:10]
                    st.markdown(f"""
                    <div class="result-box">
                        📖 <strong>نتيجة البحث:</strong><br>
                        <a href="{link}" target="_blank">🔗 اضغط لفتح نتائج البحث</a>
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.warning("⚠️ اكتب الدرس أولاً")

with col2:
    if st.button("🎥 فيديو تعليمي", use_container_width=True):
        if topic:
            with st.spinner("🔍 جاري البحث..."):
                link = search_youtube_video(topic)
                if link:
                    if topic not in st.session_state.history:
                        st.session_state.history.insert(0, topic)
                        st.session_state.history = st.session_state.history[:10]
                    st.markdown(f"""
                    <div class="result-box">
                        🎥 <strong>نتيجة البحث:</strong><br>
                        <a href="{link}" target="_blank">🔗 اضغط لفتح الفيديو مباشرة</a>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.error("❌ لم يتم العثور على فيديو.")
        else:
            st.warning("⚠️ اكتب الدرس أولاً")

if st.session_state.history:
    st.info(f"📌 آخر درس: **{st.session_state.history[0]}**")

st.markdown('<div class="saved-lessons"><h3>⭐ دروسي المحفوظة</h3>', unsafe_allow_html=True)

if st.session_state.history:
    if st.button("📥 تحميل الدروس"):
        file_content = "دروسي المحفوظة\n" + "="*30 + "\n"
        for i, item in enumerate(st.session_state.history, 1):
            file_content += f"{i}. {item}\n"
        st.download_button("✅ تحميل", file_content, f"دروسي_{datetime.datetime.now().strftime('%Y%m%d')}.txt", "text/plain")
    
    for idx, item in enumerate(st.session_state.history):
        col_a, col_b = st.columns([5, 1])
        with col_a:
            st.markdown(f'📘 {item}')
        with col_b:
            if st.button("🗑️", key=f"del_{idx}"):
                st.session_state.history.pop(idx)
                st.rerun()
else:
    st.markdown('<div class="lesson-item">💡 لا توجد دروس محفوظة.</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)