import streamlit as st

from src.conversation_analyzer import analyze_conversation


st.set_page_config(page_title="AI 客服对话质检与问题归因 Agent", page_icon="💬")

st.title("AI 客服对话质检与问题归因 Agent")
st.caption("粘贴一段模拟客服对话，查看服务质量评分、风险问题和改进建议。")

conversation = st.text_area(
    "模拟客服对话",
    height=220,
    placeholder="用户：我的订单为什么还没到账？\n客服：我帮您查一下，请稍等。",
)

if st.button("开始质检"):
    result = analyze_conversation(conversation)

    st.subheader("质检结果")
    st.metric("服务质量评分", f"{result['quality_score']} / 100")
    st.markdown(f"**处理优先级：{result['priority']}**")

    st.subheader("发现的问题")
    if result["findings"]:
        for item in result["findings"]:
            st.markdown(f"- **{item['type']}**：{item['reason']}")
    else:
        st.success("未发现明显质检风险。")

    st.subheader("改进建议")
    st.write(result["suggestion"])
