from src.conversation_analyzer import analyze_conversation


def test_detects_unresolved_problem_as_p0():
    result = analyze_conversation(
        "用户：订单一直没有到账，怎么办？\n客服：不清楚，你自己等等。"
    )

    assert result["priority"] == "P0"
    assert result["quality_score"] < 100
    assert result["findings"][0]["type"] == "问题未解决"


def test_detects_rude_tone_as_p1():
    result = analyze_conversation("用户：为什么还没退款？\n客服：这不是我的问题，别催。")

    assert result["priority"] == "P1"
    assert result["findings"][0]["type"] == "服务态度风险"


def test_polite_resolved_conversation_keeps_full_score():
    result = analyze_conversation(
        "用户：退款什么时候到账？\n客服：已为您提交退款，预计 1-3 个工作日到账。"
    )

    assert result["quality_score"] == 100
    assert result["priority"] == "P2"


def test_returns_safe_result_for_empty_text():
    result = analyze_conversation("   ")

    assert result["quality_score"] == 0
    assert result["findings"] == []
