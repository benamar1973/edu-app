import streamlit as st
from urllib.parse import quote
import streamlit.components.v1 as components

st.set_page_config(page_title="منصة تعليمية ذكية", page_icon="📚", layout="wide")

# خلفية علمية (يمكنك تغيير الرابط)
background_url = "https://images.unsplash.com/photo-1524995997946-a1c2e315a42f?q=80&w=2070&auto=format"

# إضافة خط Tajawal مع تنسيق آمن (بدون علامة % داخل st.markdown)
st.markdown(f"""
<head>
    <link href="https://fonts.googleapis.com/css2?family=Tajawal:wght@400;500;700;800&display=swap" rel="stylesheet">
</head>
<style>
    /* تطبيق الخط على كل العناصر */
    html, body, div, p, span, button, input, textarea, .stTextInput, .stButton, .stMarkdown {{
        font-family: 'Tajawal', sans-serif !important;
    }}
    
    /* خلفية الصورة مع تراكب ناعم */
    .stApp {{
        background: linear-gradient(rgba(10, 30, 50, 0.75), rgba(5, 15, 25, 0.85)), url("{background_url}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}
    
    /* بقية التنسيقات */
    .custom-card {{
        background: rgba(255,255,255,0.1);
        backdrop-filter: blur(12px);
        border-radius: 28px;
        padding: 20px;
        margin: 15px 0;
        border: 1px solid rgba(255,255,255,0.2);
        transition: all 0.3s ease;
    }}
    .custom-card:hover {{
        transform: translateY(-3px);
        background: rgba(255,255,255,0.15);
        border-color: #3B82F6;
    }}
    
    .stButton > button {{
        background: linear-gradient(95deg, #1E88E5, #6A1B9A);
        font-family: 'Tajawal', sans-serif;
        font-weight: 600;
        font-size: 18px;
        color: white;
        border: none;
        border-radius: 40px;
        padding: 10px 20px;
        width: 100%;
        transition: 0.2s;
    }}
    .stButton > button:hover {{
        transform: scale(1.02);
        box-shadow: 0 6px 14px rgba(30,136,229,0.4);
    }}
    
    .stTextInput > div > div > input {{
        background: rgba(255,255,255,0.15);
        border: 1px solid rgba(255,255,255,0.3);
        border-radius: 48px;
        padding: 12px 20px;
        color: white;
        font-size: 18px;
        font-family: 'Tajawal', sans-serif;
        text-align: right;
    }}
    .stTextInput > div > div > input:focus {{
        border-color: #1E88E5;
        box-shadow: 0 0 0 2px rgba(30,136,229,0.3);
    }}
    
    .main-title {{
        text-align: center;
        font-size: 3.2rem;
        font-weight: 800;
        background: linear-gradient(120deg, #FFD166, #06D6A0);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
        font-family: 'Tajawal', sans-serif;
    }}
    
    .slogan {{
        text-align: center;
        font-size: 1.3rem;
        color: rgba(255,255,255,0.9);
        margin-bottom: 2rem;
        font-family: 'Tajawal', sans-serif;
        font-weight: 500;
    }}
    
    /* إخفاء جميع العناصر المزعجة في الأسفل */
    footer, .viewerBadge_container__r5tak, .st-emotion-cache-1v0mbdj, .st-emotion-cache-16txtl3, .st-emotion-cache-1y4p8pa {{
        display: none !important;
    }}
    
    /* إخفاء شريط الحالة السفلي بالكامل */
    .reportview-container .main .st-emotion-cache-1r6slb0 {{
        display: none;
    }
</style>
""", unsafe_allow_html=True)

# إخفاء footer باستخدام JavaScript قوي
components.html("""
<script>
    // إخفاء العناصر التي تظهر في أسفل الصفحة
    function removeFooter() {
        var elements = document.querySelectorAll('footer, .viewerBadge_container__r5tak, .st-emotion-cache-1v0mbdj, .st-emotion-cache-16txtl3');
        elements.forEach(el => el.style.display = 'none');
    }
    setInterval(removeFooter, 100);
    window.addEventListener('load', removeFooter);
</script>
""", height=0)

# المحتوى الرئيسي
st.markdown('<div class="main-title">📚 منصة تعليمية ذكية</div>', unsafe_allow_html=True)
st.markdown('<div class="slogan">“العلم نور، والإصرار طريق النجاح”</div>', unsafe_allow_html=True)

topic = st.text_input("", placeholder="✏️ اكتب المادة والدرس... (مثال: فيزياء الكم، رياضيات متقدمة)", label_visibility="collapsed")

col1, col2 = st.columns(2)
with col1:
    text_btn = st.button("📖 درس نصي")
with col2:
    video_btn = st.button("🎥 فيديو تعليمي")

def search_and_open(query, mode):
    if not query.strip():
        st.warning("⚠️ الرجاء كتابة الدرس أولاً")
        return
    with st.spinner(f"🔍 جاري البحث عن {mode} ..."):
        if mode == "نصي":
            url = f"https://www.google.com/search?q={quote(query + ' شرح درس تعليمي')}"
        else:
            url = f"https://www.youtube.com/results?search_query={quote(query + ' شرح تعليمي')}"
        
        if "history" not in st.session_state:
            st.session_state.history = []
        st.session_state.history.insert(0, {"topic": query, "type": mode, "url": url})
        st.session_state.history = st.session_state.history[:8]
        
        components.html(f"<script>window.open('{url}','_blank');</script>", height=0)
        st.success(f"✅ تم فتح {mode} مباشرة")

if text_btn:
    search_and_open(topic, "نصي")
if video_btn:
    search_and_open(topic, "فيديو")

if "history" in st.session_state and st.session_state.history:
    last = st.session_state.history[0]
    st.info(f"📌 آخر درس: **{last['topic']}** ({last['type']})")

st.markdown("---")
st.markdown("### ⭐ دروسي المحفوظة")
if "history" in st.session_state and st.session_state.history:
    for idx, item in enumerate(st.session_state.history):
        with st.container():
            col_a, col_b = st.columns([5, 1])
            with col_a:
                st.markdown(f"📘 **{item['topic'][:50]}** ({item['type']})")
            with col_b:
                if st.button("🗑️ حذف", key=f"del_{idx}"):
                    st.session_state.history.pop(idx)
                    st.rerun()
else:
    st.caption("💡 لا توجد دروس محفوظة. ابحث عن درس وسيظهر هنا.")