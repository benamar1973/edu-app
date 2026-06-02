import streamlit as st
import requests
from urllib.parse import quote

# ================== إعدادات الصفحة ==================
st.set_page_config(page_title="منصة تعليمية ذكية", page_icon="📚", layout="wide")

# خلفية علمية
bg_url = "https://images.unsplash.com/photo-1524995997946-a1c2e315a42f?q=80&w=2070&auto=format"

# التنسيقات
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
    
    /* زر المشاركة الاحترافي */
    .share-btn-wrapper {{
        display: flex;
        justify-content: flex-end;
        margin-bottom: 20px;
    }}
    .share-btn-prof {{
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border: none;
        color: white;
        padding: 10px 24px;
        border-radius: 50px;
        font-size: 14px;
        font-weight: 600;
        display: inline-flex;
        align-items: center;
        gap: 10px;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        font-family: 'Tajawal', sans-serif;
    }}
    .share-btn-prof:hover {{
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0,0,0,0.3);
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
    }}
    .share-btn-prof:active {{
        transform: translateY(1px);
    }}
</style>
""", unsafe_allow_html=True)

# العنوان
st.markdown('<div class="main-title">📚 منصة تعليمية ذكية</div>', unsafe_allow_html=True)
st.markdown('<div class="slogan">العلم نور، والإصرار طريق النجاح</div>', unsafe_allow_html=True)

# ================== زر المشاركة الاحترافي (أعلى اليمين) ==================
share_html = """
<div class="share-btn-wrapper">
    <button class="share-btn-prof" id="shareBtn">
        <span>📤</span> مشاركة التطبيق
    </button>
</div>
<script>
    document.getElementById('shareBtn').addEventListener('click', function() {
        if (navigator.share) {
            navigator.share({
                title: 'منصة تعليمية ذكية',
                text: 'اكتشف منصة تعليمية ذكية - دروس نصية وفيديوهات تعليمية مجانية',
                url: window.location.href
            }).catch(function(err) {
                console.log('Error sharing:', err);
            });
        } else {
            // نسخ الرابط كحل بديل
            navigator.clipboard.writeText(window.location.href).then(function() {
                alert('✅ تم نسخ رابط التطبيق! يمكنك الآن مشاركته مع أصدقائك');
            }).catch(function() {
                prompt('انسخ هذا الرابط لمشاركة التطبيق:', window.location.href);
            });
        }
    });
</script>
"""
st.components.v1.html(share_html, height=80)

# ================== حقل البحث + زر المسح (تم الإصلاح النهائي) ==================
# تهيئة session_state
if "search_topic" not in st.session_state:
    st.session_state.search_topic = ""

# عرض حقل البحث
col1, col2 = st.columns([5, 1])
with col1:
    topic = st.text_input(
        "", 
        placeholder="✏️ اكتب المادة والدرس...", 
        label_visibility="collapsed", 
        key="search_input",
        value=st.session_state.search_topic,
        on_change=None
    )
with col2:
    if st.button("🗑️ مسح", key="clear_btn", use_container_width=True):
        st.session_state.search_topic = ""
        st.rerun()

# مزامنة القيمة
if topic != st.session_state.search_topic:
    st.session_state.search_topic = topic

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
    if st.button("📖 درس نصي", use_container_width=True, key="text_btn"):
        if topic:
            link = get_google_link(topic)
            st.markdown(f'<div class="result-box"><a href="{link}" target="_blank">🔗 اضغط لفتح نتائج البحث</a></div>', unsafe_allow_html=True)
        else:
            st.warning("⚠️ اكتب الدرس أولاً")

with btn2:
    if st.button("🎥 فيديو تعليمي", use_container_width=True, key="video_btn"):
        if topic:
            with st.spinner("جاري البحث عن أفضل فيديو..."):
                link = get_youtube_link(topic)
            st.markdown(f'<div class="result-box"><a href="{link}" target="_blank">🔗 اضغط لفتح الفيديو المباشر</a></div>', unsafe_allow_html=True)
        else:
            st.warning("⚠️ اكتب الدرس أولاً")