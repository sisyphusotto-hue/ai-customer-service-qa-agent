def analyze_conversation(conversation_text: str) -> dict:
    text = conversation_text.strip()
    if not text:
        return {
            "quality_score": 0,
            "findings": [],
            "priority": "P2",
            "suggestion": "请先粘贴一段模拟客服对话。",
        }

    findings = []
    if any(word in text for word in ("不清楚", "自己等等", "解决不了", "无法处理")):
        findings.append(
            {
                "type": "问题未解决",
                "reason": "客服没有提供可执行的处理路径。",
                "deduction": 40,
            }
        )
    if any(word in text for word in ("这不是我的问题", "别催")):
        findings.append(
            {
                "type": "服务态度风险",
                "reason": "客服回应带有推诿或不耐烦的表达。",
                "deduction": 20,
            }
        )

    score = max(0, 100 - sum(item["deduction"] for item in findings))
    if any(item["type"] == "问题未解决" for item in findings):
        priority = "P0"
    elif findings:
        priority = "P1"
    else:
        priority = "P2"
    suggestion = (
        "提供明确的处理步骤、预计时效和后续联系人。"
        if findings
        else "对话未发现明显质检风险。"
    )
    return {
        "quality_score": score,
        "findings": findings,
        "priority": priority,
        "suggestion": suggestion,
    }
