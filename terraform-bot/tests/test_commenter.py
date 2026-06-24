import commenter


# --- marker ---

def test_marker_format():
    assert commenter.marker('help') == '<!-- ciphertrust-bot:help -->'

def test_marker_arbitrary_key():
    assert commenter.marker('pr-triage') == '<!-- ciphertrust-bot:pr-triage -->'


# --- strip_code_and_quotes ---

def test_strip_removes_fenced_code_block():
    body = 'before\n```\n@ciphertrust-bot label\n```\nafter'
    result = commenter.strip_code_and_quotes(body)
    assert '@ciphertrust-bot' not in result
    assert 'before' in result
    assert 'after' in result

def test_strip_removes_fenced_block_with_language():
    body = 'text\n```python\ncode here\n```\nmore text'
    result = commenter.strip_code_and_quotes(body)
    assert 'code here' not in result
    assert 'more text' in result

def test_strip_removes_inline_code():
    body = 'run `@ciphertrust-bot help` to see commands'
    result = commenter.strip_code_and_quotes(body)
    assert '@ciphertrust-bot' not in result
    assert 'run' in result

def test_strip_removes_quoted_lines():
    body = 'normal line\n> quoted @ciphertrust-bot help\nanother line'
    result = commenter.strip_code_and_quotes(body)
    assert 'quoted' not in result
    assert 'normal line' in result
    assert 'another line' in result

def test_strip_preserves_normal_trigger_text():
    # The trigger in plain prose is preserved — stripping is only for
    # code/quote contexts, not plain text
    body = 'Hey @ciphertrust-bot please help'
    result = commenter.strip_code_and_quotes(body)
    assert '@ciphertrust-bot' in result

def test_strip_none_returns_empty():
    assert commenter.strip_code_and_quotes(None) == ''

def test_strip_empty_string_returns_empty():
    assert commenter.strip_code_and_quotes('') == ''

def test_strip_only_quoted_lines_returns_empty_content():
    body = '> all\n> quoted\n> lines'
    result = commenter.strip_code_and_quotes(body)
    assert 'all' not in result
    assert 'quoted' not in result
