# DeepSeek Customer Service QA Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace local keyword scoring with an independent DeepSeek API workflow for simulated customer-service dialogue quality analysis.

**Architecture:** `src/deepseek_client.py` owns secret lookup and OpenAI-compatible client creation. `src/conversation_analyzer.py` sends a customer-service-specific prompt and validates JSON containing score, priority, findings, root cause, and suggestion. `app.py` creates the client from Streamlit Secrets and renders results or safe errors.

**Tech Stack:** Python, Streamlit, OpenAI Python SDK, DeepSeek API, pytest

## Global Constraints

- The project stays independent from the other two repositories.
- Only simulated dialogues are accepted; no real customer data or API keys are committed.
- Use `deepseek-chat` at `https://api.deepseek.com`.
- Expected JSON fields are `quality_score`, `priority`, `findings`, `root_cause`, and `suggestion`.

---

### Task 1: Test and add independent DeepSeek helpers

**Files:** Create `src/deepseek_client.py`; create `tests/test_deepseek_client.py`; modify `requirements.txt`.

- [ ] Write tests that `get_api_key({"DEEPSEEK_API_KEY": "test-key"})` returns the test key and that missing configuration raises `ValueError` containing `DEEPSEEK_API_KEY`.
- [ ] Run `py -m pytest tests/test_deepseek_client.py -v` and observe the missing-module failure.
- [ ] Implement `get_api_key` and `create_client` with `OpenAI(api_key=api_key, base_url="https://api.deepseek.com")`; add `openai` to requirements.
- [ ] Run `py -m pytest tests/test_deepseek_client.py -q`.

### Task 2: Test and implement structured dialogue analysis

**Files:** Modify `src/conversation_analyzer.py`; modify `tests/test_conversation_analyzer.py`.

- [ ] Use a fake client that returns JSON with `quality_score: 45`, `priority: "P0"`, one `问题未解决` finding, a root cause, and a suggestion.
- [ ] Change the analyzer signature to `analyze_conversation(conversation_text: str, client: object) -> dict`; run the test and observe the old signature failure.
- [ ] Send a dedicated customer-service prompt to `deepseek-chat`, parse optional JSON fences, and validate score range, P0/P1/P2, non-empty findings, root cause, and suggestion.
- [ ] Run `py -m pytest tests/test_conversation_analyzer.py -q`.

### Task 3: Connect Streamlit and publish safely

**Files:** Modify `app.py`, `tests/test_app.py`, `README.md`.

- [ ] Mock client helpers in the UI test and assert the model score and P0 result are rendered.
- [ ] In `app.py`, read `dict(st.secrets)` safely, create the client on click, and show `st.error` for missing secrets or failed model responses.
- [ ] Document the safe Streamlit Secrets key name `DEEPSEEK_API_KEY`; run `py -m pytest -q` and `git diff --check`.
- [ ] Commit and push after the tests pass.
