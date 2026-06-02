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

# ================== رابط التطبيق الحقيقي ==================
# ضع رابط تطبيقك الحقيقي هنا
MY_APP_URL = "https://k4jcubpuuhs.streamlit.app"

# ================== زر مشاركة التطبيق (يعمل) ==================
st.markdown(f"""
<div style="display: flex; justify-content: center; margin: 20px 0;">
    <a href="{MY_APP_URL}" target="_blank" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 10px 30px; border-radius: 50px; text-decoration: none; font-weight: bold; display: inline-flex; align-items: center; gap: 10px;">
        📤 مشاركة التطبيق
    </a>
</div>
""", unsafe_allow_html=True)

st.divider()

# ================== حقل البحث + زر مسح (الطريقة الصحيحة) ==================
# استخدام form لحل مشكلة المسح
with st.form(key="search_form"):
    topic = st.text_input("🔍 اكتب المادة والدرس", placeholder="مثال: الرياضيات - المعادلات")
    
    col1, col2, col3 = st.columns([2, 2, 1])
    with col1:
        submitted_text = st.form_submit_button("📖 درس نصي", use_container_width=True)
    with col2:
        submitted_video = st.form_submit_button("🎥 فيديو تعليمي", use_container_width=True)
    with col3:
        clear = st.form_submit_button("🗑️ مسح", use_container_width=True)

# معالجة المسح
if clear:
    topic = ""
    st.rerun()

# معالجة البحث
if submitted_text and topic:
    link = f"https://www.google.com/search?q={quote(topic + ' شرح')}"
    st.markdown(f'<div class="result-box"><a href="{link}" target="_blank">🔗 اضغط لفتح نتائج البحث</a></div>', unsafe_allow_html=True)
elif submitted_text and not topic:
    st.warning("⚠️ اكتب الدرس أولاً")

if submitted_video and topic:
    with st.spinner("جاري البحث عن أفضل فيديو..."):
        try:
            key = st.secrets.get("YOUTUBE_API_KEY")
            if key:
                url = "https://www.googleapis.com/youtube/v3/search"
                params = {"part": "snippet", "q": topic + " شرح", "type": "video", "maxResults": 1, "key": key}
                r = requests.get(url, params=params)
                data = r.json()
                if "items" in data and len(data["items"]) > 0:
                    video_id = data['items'][0]['id']['videoId']
                    link = f"https://www.youtube.com/watch?v={video_id}"
                else:
                    link = f"https://www.youtube.com/results?search_query={quote(topic + ' شرح')}"
            else:
                link = f"https://www.youtube.com/results?search_query={quote(topic + ' شرح')}"
        except:
            link = f"https://www.youtube.com/results?search_query={quote(topic + ' شرح')}"
    st.markdown(f'<div class="result-box"><a href="{link}" target="_blank">🔗 اضغط لفتح الفيديو المباشر</a></div>', unsafe_allow_html=True)
elif submitted_video and not topic:
    st.warning("⚠️ اكتب الدرس أولاً")