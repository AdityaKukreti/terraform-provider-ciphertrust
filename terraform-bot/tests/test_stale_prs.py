from datetime import datetime, timezone, timedelta
from unittest.mock import patch, MagicMock
import stale_prs


# --- parse_time ---

def test_parse_time_z_suffix():
    result = stale_prs.parse_time('2025-01-15T10:00:00Z')
    assert result is not None
    assert result.year == 2025
    assert result.month == 1
    assert result.tzinfo is not None

def test_parse_time_explicit_offset():
    result = stale_prs.parse_time('2025-01-15T10:00:00+00:00')
    assert result is not None
    assert result.tzinfo is not None

def test_parse_time_none_returns_none():
    assert stale_prs.parse_time(None) is None

def test_parse_time_empty_returns_none():
    assert stale_prs.parse_time('') is None


# --- label_names ---

def test_label_names_basic():
    item = {'labels': [{'name': 'bug'}, {'name': 'stale'}]}
    assert stale_prs.label_names(item) == ['bug', 'stale']

def test_label_names_empty():
    assert stale_prs.label_names({'labels': []}) == []

def test_label_names_skips_missing_name():
    item = {'labels': [{'name': 'bug'}, {}, {'name': None}]}
    assert stale_prs.label_names(item) == ['bug']


# --- days / minutes ---

def test_days_reads_env_var(monkeypatch):
    monkeypatch.setenv('STALE_PR_DAYS', '45')
    assert stale_prs.days('STALE_PR_DAYS', 30) == 45

def test_days_uses_default_when_unset(monkeypatch):
    monkeypatch.delenv('STALE_PR_DAYS', raising=False)
    assert stale_prs.days('STALE_PR_DAYS', 30) == 30

def test_days_uses_default_on_invalid_value(monkeypatch):
    monkeypatch.setenv('STALE_PR_DAYS', 'not-a-number')
    assert stale_prs.days('STALE_PR_DAYS', 30) == 30

def test_minutes_returns_int_when_set(monkeypatch):
    monkeypatch.setenv('STALE_PR_MINUTES', '15')
    assert stale_prs.minutes('STALE_PR_MINUTES') == 15

def test_minutes_returns_none_when_unset(monkeypatch):
    monkeypatch.delenv('STALE_PR_MINUTES', raising=False)
    assert stale_prs.minutes('STALE_PR_MINUTES') is None


# --- _process_stale ---

def _item(labels, updated_at='2020-01-01T00:00:00Z', number=1):
    return {
        'number': number,
        'updated_at': updated_at,
        'labels': [{'name': l} for l in labels],
    }


def test_process_stale_exempt_label_skips_all_actions():
    item = _item(['no-stale'])
    closer = MagicMock()
    with patch.object(stale_prs.gh, 'add_labels') as mock_add, \
         patch.object(stale_prs.gh, 'add_comment') as mock_comment, \
         patch.object(stale_prs.gh, 'log'):
        stale_prs._process_stale(
            item, 'stale', 'no-stale',
            timedelta(days=30), timedelta(days=7), '7 days', closer,
        )
        mock_add.assert_not_called()
        mock_comment.assert_not_called()
        closer.assert_not_called()


def test_process_stale_phase1_warns_when_old_enough():
    now = datetime(2025, 6, 1, tzinfo=timezone.utc)
    item = _item([], updated_at='2025-01-01T00:00:00Z')  # 5 months old
    closer = MagicMock()
    with patch('stale_prs.datetime') as mock_dt, \
         patch.object(stale_prs.gh, 'add_labels') as mock_add, \
         patch.object(stale_prs.gh, 'add_comment'), \
         patch.object(stale_prs.gh, 'log'):
        mock_dt.now.return_value = now
        mock_dt.fromisoformat.side_effect = datetime.fromisoformat
        stale_prs._process_stale(
            item, 'stale', 'no-stale',
            timedelta(days=30), timedelta(days=7), '7 days', closer,
        )
        mock_add.assert_called_once_with(1, ['stale'])
        closer.assert_not_called()


def test_process_stale_phase1_no_warn_when_too_new():
    now = datetime(2025, 6, 1, tzinfo=timezone.utc)
    item = _item([], updated_at='2025-05-31T00:00:00Z')  # 1 day old
    closer = MagicMock()
    with patch('stale_prs.datetime') as mock_dt, \
         patch.object(stale_prs.gh, 'add_labels') as mock_add, \
         patch.object(stale_prs.gh, 'log'):
        mock_dt.now.return_value = now
        mock_dt.fromisoformat.side_effect = datetime.fromisoformat
        stale_prs._process_stale(
            item, 'stale', 'no-stale',
            timedelta(days=30), timedelta(days=7), '7 days', closer,
        )
        mock_add.assert_not_called()
        closer.assert_not_called()


def test_process_stale_phase2_closes_after_grace_period():
    # Labeled 9 days ago, grace is 7 days → should close
    now = datetime(2025, 6, 10, tzinfo=timezone.utc)
    labeled_at = datetime(2025, 6, 1, tzinfo=timezone.utc)
    # updated_at is only 1 second after labeled_at (within ACTIVITY_MARGIN of 2 min)
    item = _item(['stale'], updated_at='2025-06-01T00:00:01Z')
    closer = MagicMock()
    with patch('stale_prs.datetime') as mock_dt, \
         patch('stale_prs._label_added_at', return_value=labeled_at), \
         patch.object(stale_prs.gh, 'add_comment'), \
         patch.object(stale_prs.gh, 'log'):
        mock_dt.now.return_value = now
        mock_dt.fromisoformat.side_effect = datetime.fromisoformat
        stale_prs._process_stale(
            item, 'stale', 'no-stale',
            timedelta(days=30), timedelta(days=7), '7 days', closer,
        )
        closer.assert_called_once_with(1)


def test_process_stale_phase2_revives_on_activity_after_warning():
    # Activity 1 hour after the stale label was applied → remove stale, don't close
    now = datetime(2025, 6, 5, tzinfo=timezone.utc)
    labeled_at = datetime(2025, 6, 1, tzinfo=timezone.utc)
    item = _item(['stale'], updated_at='2025-06-01T01:00:00Z')  # 1h after label
    closer = MagicMock()
    with patch('stale_prs.datetime') as mock_dt, \
         patch('stale_prs._label_added_at', return_value=labeled_at), \
         patch.object(stale_prs.gh, 'remove_label') as mock_remove, \
         patch.object(stale_prs.gh, 'log'):
        mock_dt.now.return_value = now
        mock_dt.fromisoformat.side_effect = datetime.fromisoformat
        stale_prs._process_stale(
            item, 'stale', 'no-stale',
            timedelta(days=30), timedelta(days=7), '7 days', closer,
        )
        mock_remove.assert_called_once_with(1, 'stale')
        closer.assert_not_called()


def test_process_stale_phase2_no_close_within_grace():
    # Labeled 3 days ago, grace is 7 days → too early to close
    now = datetime(2025, 6, 4, tzinfo=timezone.utc)
    labeled_at = datetime(2025, 6, 1, tzinfo=timezone.utc)
    item = _item(['stale'], updated_at='2025-06-01T00:00:01Z')
    closer = MagicMock()
    with patch('stale_prs.datetime') as mock_dt, \
         patch('stale_prs._label_added_at', return_value=labeled_at), \
         patch.object(stale_prs.gh, 'log'):
        mock_dt.now.return_value = now
        mock_dt.fromisoformat.side_effect = datetime.fromisoformat
        stale_prs._process_stale(
            item, 'stale', 'no-stale',
            timedelta(days=30), timedelta(days=7), '7 days', closer,
        )
        closer.assert_not_called()


def test_process_stale_phase2_unknown_label_time_is_conservative():
    # _label_added_at returns None → can't determine when warned → don't close
    item = _item(['stale'], updated_at='2020-01-01T00:00:00Z')
    closer = MagicMock()
    with patch('stale_prs._label_added_at', return_value=None), \
         patch.object(stale_prs.gh, 'log'):
        stale_prs._process_stale(
            item, 'stale', 'no-stale',
            timedelta(days=30), timedelta(days=7), '7 days', closer,
        )
        closer.assert_not_called()
