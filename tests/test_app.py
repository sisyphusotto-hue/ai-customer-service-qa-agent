from pathlib import Path

from streamlit.testing.v1 import AppTest

from src import conversation_analyzer, deepseek_client


def test_app_renders_deepseek_quality_result(monkeypatch):
    model_result = {
        "quality_score": 45,
        "priority": "P0",
        "findings": [{"type": "问题未解决", "reason": "客服没有提供处理路径。"}],
        "root_cause": "客服未查询订单状态。",
        "suggestion": "先查询订单，再说明时效。",
    }
    monkeypatch.setattr(deepseek_client, "get_api_key", lambda secrets: "test-key")
    monkeypatch.setattr(deepseek_client, "create_client", lambda api_key: object())
    monkeypatch.setattr(
        conversation_analyzer,
        "analyze_conversation",
        lambda conversation, client: model_result,
    )

    app = AppTest.from_file(Path(__file__).parents[1] / "app.py")
    app.run()
    app.text_area[0].input("用户：订单没到账。\n客服：不清楚。")
    app.button[0].click().run()

    assert app.metric[0].value == "45 / 100"
    assert "P0" in app.markdown[0].value

def test_app_renders_a_quality_result_after_clicking_analyze():
    app = AppTest.from_file(Path(__file__).parents[1] / "app.py")
    app.run()
    app.text_area[0].input("用户：订单一直没有到账。\n客服：不清楚，你自己等等。")
    app.button[0].click().run()

    assert app.metric[0].label == "服务质量评分"
    assert "P0" in app.markdown[0].value
