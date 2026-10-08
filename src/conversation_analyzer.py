import json


def analyze_conversation(conversation_text: str, client: object | None = None) -> dict:
    text = conversation_text.strip()
    if not text:
        return {
            "quality_score": 0,
            "findings": [],
            "priority": "P2",
            "suggestion": "请先粘贴一段模拟客服对话。",
        }

    if client is not None:
        response = client.chat.completions.create(
            model="deepseek-chat",
            temperature=0.2,
            messages=[
                {
                    "role": "system",
                    "content": "你是客服质检助手，只输出符合要求的 JSON。",
                },
                {"role": "user", "content": build_qa_prompt(text)},
            ],
        )
        return parse_model_result(response.choices[0].message.content)

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


def build_qa_prompt(conversation_text: str) -> str:
    return f"""请质检以下模拟客服对话：
{conversation_text}

从客服是否解决问题、服务态度、回复完整性和风险等级分析。
quality_score 必须是 0 到 100 的整数；priority 只能是 P0、P1、P2；findings 是问题列表，每项包含 type 和 reason；root_cause 与 suggestion 都是不超过 50 字的中文。
只返回 JSON，不要使用 Markdown 代码块：
{{
  "quality_score": 80,
  "priority": "P1",
  "findings": [{{"type": "问题类型", "reason": "判断原因"}}],
  "root_cause": "问题归因",
  "suggestion": "改进建议"
}}
"""


def parse_model_result(raw_content: str | None) -> dict:
    if not raw_content:
        raise ValueError("模型没有返回质检结果。")

    content = raw_content.strip()
    if content.startswith("```"):
        content = content.split("\n", maxsplit=1)[1].rsplit("```", maxsplit=1)[0].strip()

    result = json.loads(content)
    score = result.get("quality_score")
    priority = result.get("priority")
    findings = result.get("findings")
    root_cause = result.get("root_cause")
    suggestion = result.get("suggestion")
    if not isinstance(score, int) or not 0 <= score <= 100:
        raise ValueError("模型返回的服务质量评分无效。")
    if priority not in ("P0", "P1", "P2"):
        raise ValueError("模型返回的处理优先级无效。")
    if not isinstance(findings, list):
        raise ValueError("模型返回的质检问题列表无效。")
    if not all(
        isinstance(item, dict)
        and isinstance(item.get("type"), str)
        and item["type"].strip()
        and isinstance(item.get("reason"), str)
        and item["reason"].strip()
        for item in findings
    ):
        raise ValueError("模型返回的质检问题内容无效。")
    if not all(isinstance(value, str) and value.strip() for value in (root_cause, suggestion)):
        raise ValueError("模型返回的归因或建议无效。")
    return {
        "quality_score": score,
        "priority": priority,
        "findings": findings,
        "root_cause": root_cause.strip(),
        "suggestion": suggestion.strip(),
    }
