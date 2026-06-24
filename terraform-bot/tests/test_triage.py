import triage


# --- text_of / raw_text ---

def test_text_of_combines_and_lowercases():
    result = triage.text_of({'title': 'HELLO', 'body': 'World'})
    assert 'hello' in result
    assert 'world' in result

def test_raw_text_preserves_case():
    result = triage.raw_text({'title': 'HELLO', 'body': 'World'})
    assert 'HELLO' in result
    assert 'World' in result

def test_text_of_handles_none_fields():
    assert triage.text_of({'title': None, 'body': None}) == '\n'


# --- provider_labels_from_text ---

def test_provider_labels_unauthorized_gives_auth_and_security():
    labels = triage.provider_labels_from_text({'title': 'unauthorized access', 'body': ''})
    assert 'auth' in labels
    assert 'security' in labels

def test_provider_labels_tls():
    labels = triage.provider_labels_from_text({'title': 'TLS handshake error', 'body': ''})
    assert 'auth' in labels
    assert 'security' in labels

def test_provider_labels_security_keyword_alone():
    labels = triage.provider_labels_from_text({'title': 'security concern', 'body': ''})
    assert 'security' in labels

def test_provider_labels_resource():
    labels = triage.provider_labels_from_text({'title': '', 'body': 'resource_ not found'})
    assert 'resource' in labels

def test_provider_labels_datasource():
    labels = triage.provider_labels_from_text({'title': 'data source broken', 'body': ''})
    assert 'data-source' in labels

def test_provider_labels_ciphertrust_manager():
    labels = triage.provider_labels_from_text({'title': 'CipherTrust Manager config', 'body': ''})
    assert 'ciphertrust-manager' in labels

def test_provider_labels_no_match_returns_empty():
    labels = triage.provider_labels_from_text({'title': 'simple question', 'body': ''})
    assert labels == []


# --- provider_labels_from_files ---

def test_provider_labels_from_files_auth_path():
    labels = triage.provider_labels_from_files(['internal/auth_handler.go'])
    assert 'auth' in labels
    assert 'security' in labels

def test_provider_labels_from_files_tls_path():
    labels = triage.provider_labels_from_files(['pkg/tls_config.go'])
    assert 'auth' in labels
    assert 'security' in labels

def test_provider_labels_from_files_resource():
    labels = triage.provider_labels_from_files(['provider/resource_ciphertrust_key.go'])
    assert 'resource' in labels

def test_provider_labels_from_files_data_source():
    labels = triage.provider_labels_from_files(['internal/data_source_keys.go'])
    assert 'data-source' in labels

def test_provider_labels_from_files_provider():
    labels = triage.provider_labels_from_files(['provider/provider.go'])
    assert 'provider-config' in labels

def test_provider_labels_from_files_empty():
    assert triage.provider_labels_from_files([]) == []


# --- matches_any ---

def test_matches_any_glob_workflow():
    assert triage.matches_any('.github/workflows/bot.yml', ['.github/workflows/**'])

def test_matches_any_exact():
    assert triage.matches_any('go.mod', ['go.mod'])

def test_matches_any_wildcard_suffix():
    assert triage.matches_any('docs/guide.md', ['docs/**'])

def test_matches_any_multiple_patterns_second_matches():
    assert triage.matches_any('examples/main.tf', ['docs/**', 'examples/**'])

def test_matches_any_no_match():
    assert not triage.matches_any('main.go', ['docs/**', 'examples/**'])


# --- missing_tests_docs ---

def test_missing_tests_docs_code_only_needs_both():
    labels, _ = triage.missing_tests_docs(['provider/resource_key.go'])
    assert 'needs-tests' in labels
    assert 'needs-docs' in labels

def test_missing_tests_docs_code_with_test_needs_docs_only():
    labels, _ = triage.missing_tests_docs([
        'provider/resource_key.go',
        'provider/resource_key_test.go',
    ])
    assert 'needs-tests' not in labels
    assert 'needs-docs' in labels

def test_missing_tests_docs_code_with_docs_needs_tests_only():
    labels, _ = triage.missing_tests_docs([
        'provider/resource_key.go',
        'docs/resource_key.md',
    ])
    assert 'needs-tests' in labels
    assert 'needs-docs' not in labels

def test_missing_tests_docs_test_only_needs_nothing():
    labels, _ = triage.missing_tests_docs(['provider/resource_key_test.go'])
    assert labels == []

def test_missing_tests_docs_docs_only_needs_nothing():
    labels, _ = triage.missing_tests_docs(['docs/guide.md'])
    assert labels == []

def test_missing_tests_docs_empty_needs_nothing():
    labels, _ = triage.missing_tests_docs([])
    assert labels == []

def test_missing_tests_docs_full_set_needs_nothing():
    labels, _ = triage.missing_tests_docs([
        'provider/resource_key.go',
        'provider/resource_key_test.go',
        'docs/resource_key.md',
    ])
    assert labels == []


# --- risk_report ---

def test_risk_report_workflow_file_is_high():
    result = triage.risk_report({'title': '', 'body': ''}, ['.github/workflows/ci.yml'])
    assert result['level'] == 'high'

def test_risk_report_bot_file_is_high():
    result = triage.risk_report({'title': '', 'body': ''}, ['terraform-bot/bot.py'])
    assert result['level'] == 'high'

def test_risk_report_go_mod_is_high():
    result = triage.risk_report({'title': '', 'body': ''}, ['go.mod'])
    assert result['level'] == 'high'

def test_risk_report_doc_only_is_low():
    result = triage.risk_report({'title': '', 'body': ''}, ['docs/guide.md'])
    assert result['level'] == 'low'

def test_risk_report_provider_go_is_medium():
    result = triage.risk_report({'title': '', 'body': ''}, ['provider/resource_key.go'])
    assert result['level'] == 'medium'

def test_risk_report_security_wording_is_high():
    result = triage.risk_report({'title': 'TLS error', 'body': 'certificate expired'}, [])
    assert result['level'] == 'high'
    assert 'security' in result['labels']

def test_risk_report_breaking_change_wording_is_high():
    result = triage.risk_report({'title': 'breaking change', 'body': ''}, [])
    assert result['level'] == 'high'

def test_risk_report_no_files_unknown_level():
    result = triage.risk_report({'title': 'simple question', 'body': 'how do I use this?'}, [])
    assert result['level'] == 'unknown'

def test_risk_report_includes_reasons():
    result = triage.risk_report({'title': '', 'body': ''}, ['provider/resource_key.go'])
    assert len(result['reasons']) > 0


# --- quality_labels_from_missing ---

def test_quality_labels_short_body_gets_needs_info():
    labels = triage.quality_labels_from_missing('short', [])
    assert 'needs-info' in labels

def test_quality_labels_two_missing_gets_needs_info():
    labels = triage.quality_labels_from_missing('x' * 100, ['terraform version', 'provider version'])
    assert 'needs-info' in labels

def test_quality_labels_complete_issue_no_labels():
    labels = triage.quality_labels_from_missing('x' * 100, [])
    assert labels == []

def test_quality_labels_one_missing_no_needs_info():
    labels = triage.quality_labels_from_missing('x' * 100, ['terraform version'])
    assert labels == []


# --- issue_quality ---

def test_issue_quality_empty_body_needs_info():
    labels, missing = triage.issue_quality({'title': 'broken', 'body': ''})
    assert 'needs-info' in labels

def test_issue_quality_all_signals_present():
    body = (
        'Terraform v1.5.0\n'
        'Provider: thalesgroup/ciphertrust version = "0.9.0"\n'
        'Steps to reproduce:\n'
        '1. run terraform apply\n'
        '2. observe error\n'
        'Expected: resource created\n'
        'Actual: Error: unauthorized\n'
        '```\nerror output here\n```'
    )
    _, missing = triage.issue_quality({'title': 'bug', 'body': body})
    assert len(missing) < 4


# --- issue_quality_comment ---

def test_issue_quality_comment_empty_missing_returns_empty():
    assert triage.issue_quality_comment([]) == ''

def test_issue_quality_comment_includes_missing_sections():
    result = triage.issue_quality_comment(['terraform version', 'steps to reproduce'])
    assert 'terraform version' in result
    assert 'steps to reproduce' in result
    assert 'ciphertrust-bot' in result


# --- pr_quality_comment ---

def test_pr_quality_comment_no_issues_returns_empty():
    assert triage.pr_quality_comment([], {'level': 'low'}) == ''

def test_pr_quality_comment_with_missing_reasons():
    result = triage.pr_quality_comment(['no test files changed'], {'level': 'low'})
    assert 'no test files changed' in result

def test_pr_quality_comment_high_risk_included():
    result = triage.pr_quality_comment([], {'level': 'high', 'reasons': ['auth-sensitive wording']})
    assert 'auth-sensitive wording' in result

def test_pr_quality_comment_both_missing_and_risk():
    result = triage.pr_quality_comment(
        ['no docs updated'],
        {'level': 'high', 'reasons': ['high-risk files changed']},
    )
    assert 'no docs updated' in result
    assert 'high-risk files changed' in result
