import bot_config


def setup_function():
    # Reset the cache before each test so tests don't bleed into each other
    bot_config._CACHE = None


# --- deep_merge ---

def test_deep_merge_adds_new_keys():
    result = bot_config.deep_merge({'x': 1}, {'y': 2})
    assert result == {'x': 1, 'y': 2}

def test_deep_merge_overrides_existing_key():
    result = bot_config.deep_merge({'x': 1, 'y': 2}, {'y': 3})
    assert result['y'] == 3
    assert result['x'] == 1

def test_deep_merge_recurses_into_nested_dicts():
    a = {'bot': {'idempotent_comments': True, 'title': 'Dashboard'}}
    b = {'bot': {'title': 'New Dashboard'}}
    result = bot_config.deep_merge(a, b)
    assert result['bot']['idempotent_comments'] is True
    assert result['bot']['title'] == 'New Dashboard'

def test_deep_merge_does_not_mutate_original():
    a = {'x': {'nested': 1}}
    b = {'x': {'nested': 2}}
    bot_config.deep_merge(a, b)
    assert a['x']['nested'] == 1

def test_deep_merge_overwrites_dict_with_scalar():
    a = {'x': {'nested': 1}}
    b = {'x': 'scalar'}
    result = bot_config.deep_merge(a, b)
    assert result['x'] == 'scalar'

def test_deep_merge_none_overlay_acts_as_no_op():
    a = {'x': 1}
    result = bot_config.deep_merge(a, None)
    assert result == {'x': 1}


# --- get ---

def test_get_returns_default_value():
    assert bot_config.get('nonexistent.key', 'fallback') == 'fallback'

def test_get_returns_none_when_no_default():
    assert bot_config.get('nonexistent.key') is None

def test_get_reads_nested_default():
    # bot.idempotent_comments is True in DEFAULTS
    assert bot_config.get('bot.idempotent_comments') is True

def test_get_partial_path_returns_default():
    assert bot_config.get('bot.missing_subkey', 42) == 42

def test_get_top_level_key():
    result = bot_config.get('bot')
    assert isinstance(result, dict)
    assert 'idempotent_comments' in result


# --- enabled ---

def test_enabled_true_value():
    assert bot_config.enabled('bot.idempotent_comments', False) is True

def test_enabled_missing_key_uses_default():
    assert bot_config.enabled('nonexistent', False) is False
    assert bot_config.enabled('nonexistent', True) is True

def test_enabled_commands_natural_language_on_by_default():
    assert bot_config.enabled('commands.natural_language', False) is True
