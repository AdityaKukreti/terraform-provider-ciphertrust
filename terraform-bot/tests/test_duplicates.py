import pytest
import duplicates


# --- words ---

def test_words_returns_set_of_tokens():
    result = duplicates.words('rotation error failed')
    assert 'rotation' in result
    assert 'error' in result
    assert 'failed' in result

def test_words_filters_stop_words():
    # 'terraform', 'provider', 'issue', 'ciphertrust' are all stop words
    result = duplicates.words('terraform provider issue ciphertrust')
    assert 'terraform' not in result
    assert 'provider' not in result
    assert 'issue' not in result
    assert 'ciphertrust' not in result

def test_words_filters_tokens_shorter_than_3_chars():
    result = duplicates.words('ab cd resource')
    assert 'ab' not in result
    assert 'cd' not in result
    assert 'resource' in result

def test_words_splits_on_underscores_and_dashes():
    result = duplicates.words('rotation-error data_source')
    assert 'rotation' in result
    assert 'error' in result
    assert 'data' in result
    assert 'source' in result

def test_words_filters_pure_digits():
    result = duplicates.words('error 404 timeout')
    assert '404' not in result
    assert 'error' in result
    assert 'timeout' in result

def test_words_empty_string():
    assert duplicates.words('') == set()

def test_words_none():
    assert duplicates.words(None) == set()


# --- jaccard ---

def test_jaccard_identical_sets():
    a = {'foo', 'bar', 'baz'}
    assert duplicates.jaccard(a, a) == 1.0

def test_jaccard_disjoint_sets():
    assert duplicates.jaccard({'foo', 'bar'}, {'baz', 'qux'}) == 0.0

def test_jaccard_empty_sets():
    assert duplicates.jaccard(set(), {'foo'}) == 0.0
    assert duplicates.jaccard({'foo'}, set()) == 0.0
    assert duplicates.jaccard(set(), set()) == 0.0

def test_jaccard_partial_overlap():
    a = {'foo', 'bar', 'baz'}
    b = {'foo', 'bar', 'qux'}
    # intersection=2, union=4
    assert duplicates.jaccard(a, b) == pytest.approx(0.5)


# --- overlap ---

def test_overlap_returns_sorted_intersection():
    assert duplicates.overlap({'a', 'b', 'c'}, {'b', 'c', 'd'}) == ['b', 'c']

def test_overlap_no_intersection():
    assert duplicates.overlap({'a', 'b'}, {'c', 'd'}) == []

def test_overlap_empty_inputs():
    assert duplicates.overlap(set(), {'a'}) == []


# --- error_overlap ---

def test_error_overlap_substring_match():
    a = {'connection refused: cannot connect to ciphertrust manager endpoint'}
    b = {'connection refused: cannot connect to host'}
    hits = duplicates.error_overlap(a, b)
    assert len(hits) > 0

def test_error_overlap_word_overlap():
    # 3+ shared words trigger a match
    a = {'error reading resource failed with unauthorized access denied'}
    b = {'error reading resource returned 403 access denied forbidden'}
    hits = duplicates.error_overlap(a, b)
    assert len(hits) > 0

def test_error_overlap_no_match():
    a = {'authentication failed for user admin credentials invalid'}
    b = {'key rotation scheduled for next maintenance window'}
    hits = duplicates.error_overlap(a, b)
    assert hits == []

def test_error_overlap_empty_inputs():
    assert duplicates.error_overlap(set(), {'error msg'}) == []
    assert duplicates.error_overlap({'error msg'}, set()) == []


# --- signals ---

def test_signals_extracts_resources():
    issue = {
        'title': 'ciphertrust_key fails',
        'body': 'resource "ciphertrust_key" "main" {}\nError: failed',
    }
    sig = duplicates.signals(issue)
    assert 'ciphertrust_key' in sig['resources']

def test_signals_extracts_http_codes():
    issue = {'title': '401 error', 'body': 'got 401 unauthorized'}
    sig = duplicates.signals(issue)
    assert '401' in sig['http']

def test_signals_extracts_areas():
    issue = {'title': 'auth token expired', 'body': 'login failed'}
    sig = duplicates.signals(issue)
    assert 'auth' in sig['areas']

def test_signals_extracts_labels():
    issue = {
        'title': 'bug',
        'body': '',
        'labels': [{'name': 'bug'}, {'name': 'auth'}],
    }
    sig = duplicates.signals(issue)
    assert 'bug' in sig['labels']
    assert 'auth' in sig['labels']

def test_signals_handles_string_labels():
    issue = {'title': 'bug', 'body': '', 'labels': ['bug', 'auth']}
    sig = duplicates.signals(issue)
    assert 'bug' in sig['labels']


# --- score ---

def test_score_same_resource_contributes():
    a = {'title': 'key creation error', 'body': 'resource "ciphertrust_key" "main" {}', 'labels': []}
    b = {'title': 'key deletion fails', 'body': 'resource "ciphertrust_key" "test" {}', 'labels': []}
    sc, reasons = duplicates.score(a, b)
    assert sc >= 0.34
    assert any('resource' in r for r in reasons)

def test_score_unrelated_issues_below_threshold():
    a = {'title': 'tls certificate renewal process', 'body': 'cert expired last week', 'labels': []}
    b = {'title': 'dashboard loading slowly', 'body': 'page takes ten seconds', 'labels': []}
    sc, _ = duplicates.score(a, b)
    assert sc < 0.42

def test_score_capped_at_one():
    # Highly similar issue with many signals should never exceed 1.0
    body = 'resource "ciphertrust_key" "main" {}\nError: 401 unauthorized failed rotation'
    a = {'title': 'key rotation fails 401 auth error', 'body': body, 'labels': [{'name': 'bug'}, {'name': 'auth'}]}
    b = {'title': 'key rotation fails 401 auth error', 'body': body, 'labels': [{'name': 'bug'}, {'name': 'auth'}]}
    sc, _ = duplicates.score(a, b)
    assert sc <= 1.0

def test_score_same_http_code_contributes():
    a = {'title': 'getting 503 error', 'body': 'backend returns 503', 'labels': []}
    b = {'title': '503 service unavailable', 'body': 'status code 503', 'labels': []}
    sc, reasons = duplicates.score(a, b)
    assert any('503' in r for r in reasons)

def test_score_returns_reasons_list():
    a = {'title': 'key error', 'body': 'resource "ciphertrust_key" "x" {}', 'labels': []}
    b = {'title': 'key broken', 'body': 'resource "ciphertrust_key" "y" {}', 'labels': []}
    sc, reasons = duplicates.score(a, b)
    assert isinstance(reasons, list)
