import streamlit as st

from src import conversation_analyzer, deepseek_client


def get_streamlit_secrets() -> dict:
    try:
        return dict(st.secrets)
    except FileNotFoundError:
        return {}


st.set_page_config(page_title="AI 客服对话质检与问题归因 Agent", page_icon="💬")

st.title("AI 客服对话质检与问题归因 Agent")
st.caption("粘贴一段模拟客服对话，查看服务质量评分、风险问题和改进建议。")

conversation = st.text_area(
    "模拟客服对话",
    height=220,
    placeholder="用户：我的订单为什么还没到账？\n客服：我帮您查一下，请稍等。",
)

if st.button("开始质检"):
    if not conversation.strip():
        st.warning("请先粘贴一段模拟客服对话。")
        st.stop()

    try:
        api_key = deepseek_client.get_api_key(get_streamlit_secrets())
        client = deepseek_client.create_client(api_key)
        with st.spinner("正在调用模型进行质检……"):
            result = conversation_analyzer.analyze_conversation(conversation, client)
    except ValueError as error:
        st.error(str(error))
        st.stop()
    except Exception:
        st.error("模型质检暂时失败，请稍后重试。")
        st.stop()

    st.subheader("质检结果")
    st.metric("服务质量评分", f"{result['quality_score']} / 100")
    st.markdown(f"**处理优先级：{result['priority']}**")

    st.subheader("发现的问题")
    if result["findings"]:
        for item in result["findings"]:
            st.markdown(f"- **{item['type']}**：{item['reason']}")
    else:
        st.success("未发现明显质检风险。")

    st.subheader("问题归因")
    st.write(result["root_cause"])

    st.subheader("改进建议")
    st.write(result["suggestion"])
