import streamlit as st
import requests
from urllib.parse import quote
import webbrowser
import streamlit.components.v1 as components

# إعدادات الصفحة
st.set_page_config(page_title="منصة تعليمية ذكية", page_icon="📚", layout="wide")

# تنسيق CSS احترافي (بدون أي روابط خارجية)
st.markdown("""
<style>
    /* خلفية عصرية متدرجة */
    .stApp {
        background: linear-gradient(145deg, #0B1120 0%, #19233C 100%);
    }
    
    /* تنسيق البطاقات */
    .custom-card {
        background: rgba(255,255,255,0.05);
        backdrop-filter: blur(12px);
        border-radius: 24px;
        padding: 20px;
        margin: 15px 0;
        border: 1px solid rgba(255,255,255,0.1);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    .custom-card:hover {
        transform: translateY(-4px);
        border-color: rgba(59,130,246,0.5);
        box-shadow: 0 20px 30px -12px rgba(0,0,0,0.3);
    }
    
    /* أزرار أنيقة */
    .stButton > button {
        background: linear-gradient(90deg, #3B82F6, #2563EB);
        color: white;
        border: none;
        border-radius: 40px;
        padding: 12px 24px;
        font-weight: 600;
        font-size: 16px;
        transition: all 0.2s ease;
        width: 100%;
    }
    .stButton > button:hover {
        transform: scale(1.02);
        box-shadow: 0 8px 20px rgba(59,130,246,0.4);
        background: linear-gradient(90deg, #2563EB, #1D4ED8);
    }
    
    /* حقل الإدخال */
    .stTextInput > div > div > input {
        background: rgba(255,255,255,0.08);
        border: 1px solid rgba(255,255,255,0.2);
        border-radius: 48px;
        padding: 12px 20px;
        color: white;
        font-size: 16px;
        transition: all 0.2s;
    }
    .stTextInput > div > div > input:focus {
        border-color: #3B82F6;
        box-shadow: 0 0 0 2px rgba(59,130,246,0.2);
    }
    
    /* عنوان رئيسي */
    .main-title {
        text-align: center;
        font-size: 2.8rem;
        font-weight: 700;
        background: linear-gradient(120deg, #60A5FA, #A78BFA);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 1rem;
    }
    
    /* تذييل مخفي */
    footer {
        visibility: hidden;
    }
    .reportview-container .main footer {
        display: none !important;
    }
</style>
""", unsafe_allow_html=True)

# إخفاء الرابط التلقائي
st.markdown("""
<script>
    // إخفاء عنصر footer الذي يحوي روابط GitHub
    var style = document.createElement('style');
    style.innerHTML = 'footer {display: none !important;} .viewerBadge_container__r5tak {display: none !important;}';
    document.head.appendChild(style);
</script>
""", unsafe_allow_html=True)

# العنوان
st.markdown('<div class="main-title">📚 منصة تعليمية ذكية</div>', unsafe_allow_html=True)

# حقل الإدخال
topic = st.text_input("", placeholder="✏️ اكتب المادة والدرس... (مثال: فيزياء الكم)", label_visibility="collapsed")

# أزرار
col1, col2 = st.columns(2)
with col1:
    text_btn = st.button("📖 درس نصي")
with col2:
    video_btn = st.button("🎥 فيديو تعليمي")

# دوال البحث والفتح المباشر
def search_and_open(query, mode):
    if not query.strip():
        st.warning("⚠️ الرجاء كتابة الدرس أولاً")
        return
    
    with st.spinner(f"🔍 جاري البحث عن {mode} ..."):
        if mode == "نصي":
            encoded = quote(query + " شرح درس تعليمي")
            url = f"https://www.google.com/search?q={encoded}"
        else:
            encoded = quote(query + " شرح تعليمي")
            url = f"https://www.youtube.com/results?search_query={encoded}"
        
        # حفظ في الجلسة
        if "history" not in st.session_state:
            st.session_state.history = []
        st.session_state.history.insert(0, {"topic": query, "type": mode, "url": url})
        st.session_state.history = st.session_state.history[:8]
        
        # فتح الرابط تلقائياً عبر JavaScript
        components.html(f"""
            <script>
                window.open("{url}", "_blank");
            </script>
        """, height=0)
        
        st.success(f"✅ تم فتح {mode} مباشرة بنجاح")

# تنفيذ البحث
if text_btn:
    search_and_open(topic, "نصي")
if video_btn:
    search_and_open(topic, "فيديو")

# عرض آخر درس
if "history" in st.session_state and st.session_state.history:
    last = st.session_state.history[0]
    st.info(f"📌 آخر درس: **{last['topic']}** ({last['type']})")

# منطقة الدروس المحفوظة
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