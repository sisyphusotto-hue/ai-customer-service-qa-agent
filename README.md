# AI 客服对话质检与问题归因 Agent

一个面向客服运营和产品支持场景的可演示 MVP。用户粘贴一段**模拟**客服对话后，页面会给出：

- 服务质量评分（0-100）
- P0 / P1 / P2 处理优先级
- 风险问题类型与归因
- 可执行的改进建议

## 当前能力与边界

第一版使用可解释的本地规则识别“问题未解决”和“服务态度风险”。它是规则驱动的质检 MVP，不是 LLM 判断系统；后续可在学习阶段接入 LLM API，提高对自然语言表达的覆盖度。

仅使用 `data/sample_dialogues.txt` 内的模拟对话演示，请不要粘贴真实客户隐私、订单号或联系方式。

## 项目结构

```text
ai-customer-service-qa-agent/
├── app.py
├── data/sample_dialogues.txt
├── src/conversation_analyzer.py
├── tests/
├── requirements.txt
└── README.md
```

## 本地启动

```powershell
pip install -r requirements.txt
py -m streamlit run app.py
```

## 测试

```powershell
py -m pytest -q
```

## 部署

部署到 Streamlit Community Cloud 时，选择 GitHub 仓库的 `master` 分支，并把 Main file path 设置为 `app.py`。Secrets 保持为空。
