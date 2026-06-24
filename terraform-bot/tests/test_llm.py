import json
from unittest.mock import patch
import llm


# --- _strip_fences ---

def test_strip_fences_plain_json_unchanged():
    text = '{"labels": ["bug"]}'
    assert llm._strip_fences(text) == '{"labels": ["bug"]}'

def test_strip_fences_removes_json_fence():
    text = '```json\n{"labels": ["bug"]}\n```'
    assert llm._strip_fences(text) == '{"labels": ["bug"]}'

def test_strip_fences_removes_plain_fence():
    text = '```\n{"missing": []}\n```'
    assert llm._strip_fences(text) == '{"missing": []}'

def test_strip_fences_strips_surrounding_whitespace():
    text = '  {"intent": "help"}  '
    assert llm._strip_fences(text) == '{"intent": "help"}'

def test_strip_fences_empty_string():
    assert llm._strip_fences('') == ''


def test_strip_fences_multiline_json():
    text = '```json\n{\n  "labels": [\n    "bug"\n  ]\n}\n```'
    result = llm._strip_fences(text)
    assert result.startswith('{')
    assert result.endswith('}')
    assert '"bug"' in result


# --- intent: normalisation of unknown values ---

def test_intent_normalises_unrecognised_value():
    # llm.intent is the gate that turns arbitrary LLM output into a safe intent;
    # parse_command relies on it not leaking unrecognised strings through.
    with patch('llm.ask', return_value=json.dumps({'intent': 'destroy-all-issues', 'args': {}})):
        result = llm.intent('do something destructive')
        assert result['intent'] == 'unknown'

def test_intent_passes_through_valid_intent():
    with patch('llm.ask', return_value=json.dumps({'intent': 'summarize', 'args': {}})):
        result = llm.intent('please summarize this')
        assert result['intent'] == 'summarize'

def test_intent_handles_unparseable_response():
    with patch('llm.ask', return_value='not json at all'):
        result = llm.intent('anything')
        assert result['intent'] == 'unknown'

def test_intent_handles_empty_response():
    with patch('llm.ask', return_value=''):
        result = llm.intent('anything')
        assert result['intent'] == 'unknown'
