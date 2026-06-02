import streamlit as st
import requests
from urllib.parse import quote

# ================== إعدادات الصفحة ==================
st.set_page_config(page_title="منصة تعليمية ذكية", page_icon="📚", layout="wide")

bg_url = "https://images.unsplash.com/photo-1524995997946-a1c2e315a42f?q=80&w=2070&auto=format"

st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;700&display=swap');
    * {{ font-family: 'Tajawal', sans-serif; }}
    
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
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">📚 منصة تعليمية ذكية</div>', unsafe_allow_html=True)
st.markdown('<div class="slogan">العلم نور، والإصرار طريق النجاح</div>', unsafe_allow_html=True)

# ================== زر المشاركة (يعمل 100%) ==================
# طريقة Streamlit النقية بدون JavaScript معقد
app_url = "https://share.streamlit.app"  # غيّر هذا إلى رابط تطبيقك الحقيقي بعد النشر

col_url, col_share = st.columns([4, 1])
with col_url:
    st.code(app_url, language="text")
with col_share:
    st.link_button("📤 مشاركة التطبيق", app_url, use_container_width=True)

st.divider()

# ================== حقل البحث + زر مسح (يعمل الآن) ==================
if "search_topic" not in st.session_state:
    st.session_state.search_topic = ""

# العمود الأول: حقل النص
topic = st.text_input(
    "🔍 اكتب المادة والدرس",
    value=st.session_state.search_topic,
    placeholder="مثال: الرياضيات - المعادلات",
    key="topic_input"
)

# تحديث session_state عند الكتابة
st.session_state.search_topic = topic

# زر المسح أسفل الحقل مباشرة
col_clear, _ = st.columns([1, 5])
with col_clear:
    if st.button("🗑️ مسح النص", use_container_width=True):
        st.session_state.search_topic = ""
        st.rerun()

# ================== دوال البحث ==================
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

def get_google_link(query):
    return f"https://www.google.com/search?q={quote(query + ' شرح')}"

# ================== أزرار البحث ==================
btn1, btn2 = st.columns(2)
with btn1:
    if st.button("📖 درس نصي", use_container_width=True):
        if topic:
            link = get_google_link(topic)
            st.markdown(f'<div class="result-box"><a href="{link}" target="_blank">🔗 اضغط لفتح نتائج البحث</a></div>', unsafe_allow_html=True)
        else:
            st.warning("⚠️ اكتب الدرس أولاً")

with btn2:
    if st.button("🎥 فيديو تعليمي", use_container_width=True):
        if topic:
            with st.spinner("جاري البحث عن أفضل فيديو..."):
                link = get_youtube_link(topic)
            st.markdown(f'<div class="result-box"><a href="{link}" target="_blank">🔗 اضغط لفتح الفيديو المباشر</a></div>', unsafe_allow_html=True)
        else:
            st.warning("⚠️ اكتب الدرس أولاً")