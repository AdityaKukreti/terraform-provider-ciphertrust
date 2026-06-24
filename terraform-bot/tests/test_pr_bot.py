import pr_bot


# --- md_label_list ---

def test_md_label_list_sorted_output():
    result = pr_bot.md_label_list(['bug', 'auth', 'enhancement'])
    assert result == '- `auth`\n- `bug`\n- `enhancement`'

def test_md_label_list_empty_returns_none_marker():
    assert pr_bot.md_label_list([]) == '- none'

def test_md_label_list_filters_empty_strings():
    # Empty string str('') is falsy so it is filtered; None becomes 'None' via str()
    result = pr_bot.md_label_list(['bug', ''])
    assert '`bug`' in result
    assert '``' not in result

def test_md_label_list_single_label():
    assert pr_bot.md_label_list(['security']) == '- `security`'


# --- pr_triage_comment ---

def test_pr_triage_comment_contains_header():
    result = pr_bot.pr_triage_comment(['a.go'], ['bug'], [], {'level': 'low', 'reasons': []})
    assert '## PR Triage' in result

def test_pr_triage_comment_lists_labels():
    result = pr_bot.pr_triage_comment(
        ['provider/resource_key.go'],
        ['bug', 'resource'],
        [],
        {'level': 'low', 'reasons': []},
    )
    assert '`bug`' in result
    assert '`resource`' in result

def test_pr_triage_comment_shows_file_count():
    result = pr_bot.pr_triage_comment(
        ['a.go', 'b.go', 'c.go'],
        ['bug'],
        [],
        {'level': 'low', 'reasons': []},
    )
    assert '3 file(s)' in result

def test_pr_triage_comment_includes_missing_checks():
    result = pr_bot.pr_triage_comment(
        ['provider/resource_key.go'],
        ['bug'],
        ['no test files changed'],
        {'level': 'low', 'reasons': []},
    )
    assert 'no test files changed' in result
    assert 'Missing checks' in result

def test_pr_triage_comment_omits_missing_section_when_empty():
    result = pr_bot.pr_triage_comment(
        ['docs/guide.md'],
        ['documentation'],
        [],
        {'level': 'low', 'reasons': []},
    )
    assert 'Missing checks' not in result

def test_pr_triage_comment_shows_risk_section_on_high():
    result = pr_bot.pr_triage_comment(
        ['.github/workflows/ci.yml'],
        ['security'],
        [],
        {'level': 'high', 'reasons': ['high-risk files changed: .github/workflows/ci.yml']},
    )
    assert 'Risk' in result
    assert 'high-risk files changed' in result

def test_pr_triage_comment_omits_risk_section_on_low():
    result = pr_bot.pr_triage_comment(
        ['docs/guide.md'],
        ['documentation'],
        [],
        {'level': 'low', 'reasons': ['docs-only change']},
    )
    assert 'Risk' not in result

def test_pr_triage_comment_includes_bot_marker():
    result = pr_bot.pr_triage_comment([], [], [], {'level': 'low', 'reasons': []})
    assert 'ciphertrust-bot' in result

def test_pr_triage_comment_includes_maintainer_checklist():
    result = pr_bot.pr_triage_comment([], [], [], {'level': 'low', 'reasons': []})
    assert 'Maintainer checklist' in result
