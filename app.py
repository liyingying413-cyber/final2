import streamlit as st
import os
from utils import analyze_with_openai, local_analyze
from poster_generator import generate_poster_with_stable_diffusion

st.set_page_config(page_title="City × Memory × Emotion — AI Poster", layout="centered")

st.title("🌆 Emotion × City × Memory — AI Poster Generator")

st.markdown(
    "输入一个**城市名**和一段关于这座城市的**记忆文本**，"
    "AI 会先分析情绪、色彩与风格，再调用 Stable Diffusion 生成 1:1 艺术海报。"
)

city = st.text_input("城市名 City（例如：Seoul, Tokyo, Paris）")
memory = st.text_area("写下你和这座城市的记忆：", height=200)

seed = st.number_input("随机种子 Seed（同一个 seed 会生成相似风格）", value=42, step=1)

if st.button("生成海报"):
    if not city.strip() or not memory.strip():
        st.error("请输入城市名与记忆内容。")
        st.stop()

    with st.spinner("Step 1 — 分析情绪与色彩（OpenAI 或本地规则）…"):
        result = analyze_with_openai(city, memory)
        if result is None:
            st.warning("⚠ OpenAI 调用失败，已使用本地 fallback 分析。")
            result = local_analyze(city, memory)

    st.subheader("Step 2 — AI 分析结果（可写进报告）")
    st.json(result)

    with st.spinner("Step 3 — Stable Diffusion 正在生成 1:1 艺术海报…"):
        img = generate_poster_with_stable_diffusion(result, seed=int(seed))

    if img is None:
        st.error("❌ Stable Diffusion 生成失败，请检查 STABILITY_API_KEY 或稍后重试。")
    else:
        st.subheader("生成海报预览")
        st.image(img, use_column_width=True)

        import io
        buf = io.BytesIO()
        img.save(buf, format="PNG")

        st.download_button(
            "下载海报 PNG",
            data=buf.getvalue(),
            file_name="city_memory_poster.png",
            mime="image/png",
        )
