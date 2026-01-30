from app.utils.guardrails import check_guardrails

def test_guardrails_clean_text():
    text = "Hello, how are you?"
    result = check_guardrails(text)
    assert result["valid"] is True
    assert len(result["violations"]) == 0

def test_guardrails_legal_advice():
    text = "You should definitely sue them."
    result = check_guardrails(text)
    assert result["valid"] is False
    assert len(result["violations"]) > 0
    assert result["violations"][0]["rule"] == "legal_advice"
