import streamlit as st
import requests
from urllib.parse import quote
import time

# إعدادات الصفحة
st.set_page_config(page_title="منصة تعليمية ذكية", page_icon="📚", layout="wide")

# تنسيق CSS احترافي
st.markdown("""
<style>
    /* خلفية متدرجة أنيقة */
    .stApp {
        background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
    }
    
    /* تنسيق البطاقات */
    .custom-card {
        background: rgba(255,255,255,0.1);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 20px;
        margin: 15px 0;
        border: 1px solid rgba(255,255,255,0.2);
        transition: transform 0.3s ease;
    }
    .custom-card:hover {
        transform: translateY(-5px);
    }
    
    /* تنسيق الأزرار */
    .stButton > button {
        background: linear-gradient(90deg, #00c6ff, #0072ff);
        color: white;
        border: none;
        border-radius: 30px;
        padding: 10px 25px;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        transform: scale(1.02);
        box-shadow: 0 5px 15px rgba(0,114,255,0.4);
    }
    
    /* تنسيق حقل الإدخال */
    .stTextInput > div > div > input {
        border-radius: 30px;
        border: 1px solid rgba(255,255,255,0.3);
        background: rgba(255,255,255,0.1);
        color: white;
        padding: 10px 20px;
    }
    
    /* عنوان الصفحة */
    .main-title {
        text-align: center;
        font-size: 3rem;
        background: linear-gradient(90deg, #00c6ff, #0072ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 20px;
    }
    
    /* تنسيق الدروس المحفوظة */
    .saved-item {
        background: rgba(255,255,255,0.1);
        border-radius: 15px;
        padding: 10px 15px;
        margin: 5px 0;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
</style>
""", unsafe_allow_html=True)

# العنوان
st.markdown('<p class="main-title">📚 منصتي التعليمية الذكية</p>', unsafe_allow_html=True)

# العمودان: الإدخال والنتائج
col_left, col_right = st.columns([2, 1])

with col_left:
    st.markdown("### 🔍 ابحث عن درسك")
    topic = st.text_input("", placeholder="مثال: برمجة بايثون - دوال", label_visibility="collapsed")
    
    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        search_text = st.button("📖 درس نصي", use_container_width=True)
    with col_btn2:
        search_video = st.button("🎥 فيديو تعليمي", use_container_width=True)

    # دالة البحث
    def search_and_open(query, search_type):
        with st.spinner("🔍 جاري البحث عن أفضل محتوى..."):
            time.sleep(0.5)  # محاكاة بحث حقيقية
            if search_type == "text":
                encoded = quote(query + " شرح درس تعليمي")
                link = f"https://www.google.com/search?q={encoded}"
            else:
                encoded = quote(query + " شرح تعليمي")
                link = f"https://www.youtube.com/results?search_query={encoded}"
            
            # حفظ الدرس في الجلسة
            if "history" not in st.session_state:
                st.session_state.history = []
            st.session_state.history.insert(0, {"topic": query, "type": search_type, "link": link})
            if len(st.session_state.history) > 10:
                st.session_state.history.pop()
            
            # فتح الرابط تلقائياً
            st.markdown(f'<script>window.open("{link}", "_blank");</script>', unsafe_allow_html=True)
            st.success(f"✅ تم فتح الدرس {search_type} بنجاح")
            return link

    if search_text and topic:
        link = search_and_open(topic, "نصي")
    elif search_video and topic:
        link = search_and_open(topic, "فيديو")
    elif (search_text or search_video) and not topic:
        st.warning("⚠️ الرجاء كتابة اسم الدرس أولاً")

    # عرض آخر درس تم فتحه
    if "history" in st.session_state and st.session_state.history:
        last = st.session_state.history[0]
        st.info(f"📌 آخر درس: **{last['topic']}** ({last['type']})")

with col_right:
    st.markdown("### ⭐ دروسي المحفوظة")
    if "history" in st.session_state and st.session_state.history:
        for i, item in enumerate(st.session_state.history):
            col_a, col_b = st.columns([4, 1])
            with col_a:
                st.markdown(f"📘 {item['topic'][:30]}...")
            with col_b:
                if st.button("🗑️", key=f"del_{i}"):
                    st.session_state.history.pop(i)
                    st.rerun()
    else:
        st.info("💡 لا توجد دروس محفوظة. ابحث عن درس وسيظهر هنا.")

# تذييل أنيق
st.markdown("---")
st.markdown("<p style='text-align:center; color:rgba(255,255,255,0.6);'>✨ منصة تعليمية ذكية - ابحث وتعلم واحفظ دروسك</p>", unsafe_allow_html=True)