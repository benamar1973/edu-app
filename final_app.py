import streamlit as st
import requests
from urllib.parse import quote

st.set_page_config(page_title="منصة تعليمية ذكية", page_icon="📚")
st.title("📚 منصة تعليمية ذكية")

st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border-radius: 10px;
        font-size: 18px;
    }
    .stTextInput>div>div>input {
        font-size: 18px;
        border-radius: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.image("https://cdn-icons-png.flaticon.com/512/2232/2232688.png", width=80)
st.markdown("ابحث عن درس نصي أو فيديو بضغطة زر")

topic = st.text_input("✏️ اكتب اسم المادة والدرس:", placeholder="مثال: برمجة بايثون - دوال")

col1, col2 = st.columns(2)
with col1:
    text_btn = st.button("📖 درس نصي", use_container_width=True)
with col2:
    video_btn = st.button("🎥 درس فيديو", use_container_width=True)

if text_btn and topic:
    with st.spinner("جاري البحث عن درس نصي..."):
        query = quote(topic + " شرح درس تعليمي")
        link = f"https://www.google.com/search?q={query}"
        st.success("✅ تم العثور على الدرس النصي:")
        st.markdown(f"[🔗 اضغط لفتح نتائج البحث]({link})")

if video_btn and topic:
    with st.spinner("جاري البحث عن فيديو..."):
        query = quote(topic + " شرح تعليمي")
        link = f"https://www.youtube.com/results?search_query={query}"
        st.success("✅ تم العثور على الفيديو التعليمي:")
        st.markdown(f"[🎬 اضغط لفتح الفيديو]({link})")

if (text_btn or video_btn) and not topic:
    st.warning("⚠️ الرجاء كتابة اسم الدرس أولاً.")