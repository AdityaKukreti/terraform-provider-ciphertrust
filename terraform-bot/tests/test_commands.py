from unittest.mock import patch
import commands


# --- allowed ---

def test_allowed_owner():
    assert commands.allowed({'author_association': 'OWNER'})

def test_allowed_member():
    assert commands.allowed({'author_association': 'MEMBER'})

def test_allowed_collaborator():
    assert commands.allowed({'author_association': 'COLLABORATOR'})

def test_not_allowed_contributor():
    assert not commands.allowed({'author_association': 'CONTRIBUTOR'})

def test_not_allowed_none():
    assert not commands.allowed({'author_association': None})

def test_not_allowed_missing_key():
    assert not commands.allowed({})


# --- body_without_trigger ---

def test_body_without_trigger_extracts_command():
    assert commands.body_without_trigger('@ciphertrust-bot help') == 'help'

def test_body_without_trigger_trims_whitespace():
    assert commands.body_without_trigger('@ciphertrust-bot   summarize  ') == 'summarize'

def test_body_without_trigger_no_trigger_returns_empty():
    assert commands.body_without_trigger('just a normal comment') == ''

def test_body_without_trigger_strips_fenced_code():
    # Commands inside code blocks must not be extracted
    body = '@ciphertrust-bot help\n```\n@ciphertrust-bot label\n```'
    result = commands.body_without_trigger(body)
    assert result == 'help'

def test_body_without_trigger_none_returns_empty():
    assert commands.body_without_trigger(None) == ''

def test_body_without_trigger_empty_returns_empty():
    assert commands.body_without_trigger('') == ''


# --- current_label_names ---

def test_current_label_names_basic():
    issue = {'labels': [{'name': 'bug'}, {'name': 'enhancement'}]}
    assert commands.current_label_names(issue) == {'bug', 'enhancement'}

def test_current_label_names_empty_list():
    assert commands.current_label_names({'labels': []}) == set()

def test_current_label_names_skips_entries_without_name():
    issue = {'labels': [{'name': 'bug'}, {}, {'name': None}]}
    assert commands.current_label_names(issue) == {'bug'}


# --- parse_command: exact keyword matches ---

def test_parse_command_help():
    assert commands.parse_command('help')['intent'] == 'help'

def test_parse_command_features():
    assert commands.parse_command('features')['intent'] == 'features'

def test_parse_command_summarize():
    assert commands.parse_command('summarize')['intent'] == 'summarize'

def test_parse_command_explain():
    assert commands.parse_command('explain')['intent'] == 'explain'

def test_parse_command_check_labels_exact():
    assert commands.parse_command('check-labels')['intent'] == 'check-labels'

def test_parse_command_clean_labels_exact():
    assert commands.parse_command('clean-labels')['intent'] == 'clean-labels'

def test_parse_command_label_no_arg():
    result = commands.parse_command('label')
    assert result['intent'] == 'label'
    assert result['args']['label'] is None

def test_parse_command_label_with_arg():
    result = commands.parse_command('label bug')
    assert result['intent'] == 'label'
    assert result['args']['label'] == 'bug'


# --- parse_command: duplicate ---

def test_parse_command_duplicate_with_number():
    result = commands.parse_command('duplicate #123')
    assert result['intent'] == 'duplicate'
    assert result['args']['number'] == '123'

def test_parse_command_duplicate_without_number():
    result = commands.parse_command('duplicate')
    assert result['intent'] == 'duplicate'
    assert result['args']['number'] is None


# --- parse_command: regex fallbacks ---

def test_parse_command_natural_check_labels():
    assert commands.parse_command('check my labels please')['intent'] == 'check-labels'

def test_parse_command_natural_clean_labels():
    assert commands.parse_command('remove old labels')['intent'] == 'clean-labels'

def test_parse_command_natural_clean_labels_variant():
    assert commands.parse_command('clean up the labels')['intent'] == 'clean-labels'

def test_parse_command_summarise_variant():
    assert commands.parse_command('summarise this issue')['intent'] == 'summarize'

def test_parse_command_summary_variant():
    assert commands.parse_command('give me a summary')['intent'] == 'summarize'

def test_parse_command_features_natural():
    assert commands.parse_command('what can you do')['intent'] == 'features'


# --- parse_command: unknown / empty ---

def test_parse_command_empty_string():
    assert commands.parse_command('')['intent'] == 'unknown'

def test_parse_command_none():
    assert commands.parse_command(None)['intent'] == 'unknown'

def test_parse_command_unrecognized_no_nl():
    with patch.object(commands.bot_config, 'enabled', return_value=False):
        assert commands.parse_command('do something weird')['intent'] == 'unknown'

def test_parse_command_nl_fallback_routes_intent():
    with patch('commands.llm.intent', return_value={'intent': 'summarize', 'args': {}}):
        with patch.object(commands.bot_config, 'enabled', return_value=True):
            result = commands.parse_command('can you give me an overview')
            assert result['intent'] == 'summarize'

def test_parse_command_nl_fallback_unknown_intent_passthrough():
    # parse_command trusts llm.intent's return value directly;
    # llm.intent itself is responsible for normalising to 'unknown' for
    # unrecognised intents (tested in test_llm.py::test_intent_normalises_unknown)
    with patch('commands.llm.intent', return_value={'intent': 'unknown', 'args': {}}):
        with patch.object(commands.bot_config, 'enabled', return_value=True):
            result = commands.parse_command('destroy everything')
            assert result['intent'] == 'unknown'
