from pathlib import Path

from streamlit.testing.v1 import AppTest


def test_app_renders_a_quality_result_after_clicking_analyze():
    app = AppTest.from_file(Path(__file__).parents[1] / "app.py")
    app.run()
    app.text_area[0].input("用户：订单一直没有到账。\n客服：不清楚，你自己等等。")
    app.button[0].click().run()

    assert app.metric[0].label == "服务质量评分"
    assert "P0" in app.markdown[0].value
