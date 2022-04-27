import json
import os


# The config interface
# -----------------------------------------------------------
#   get()
#   set()
#   reset()

def get(name):
    return _values.get(name)


def set(values):
    for name in _configurable_values:
        if (name in values) and (values[name] is not None):
            _values[name] = values[name]
    with open(_config_path, 'w') as config_file:
        config_file.write(
            json.dumps(_values)
        )

def reset():
    set(DEFAULT_VALUES)

# -----------------------------------------------------------

env = os.environ['ENV'].lower()

# Directory of the config file
if env == 'prod':
    _config_filename = 'cleaconf.json'
    _config_dir = rf'{os.path.curdir}' + os.path.sep
else:
    _config_filename = 'cleaconftest.json'
    _config_dir = rf'{os.path.curdir}' + os.path.sep

_config_path = f'{_config_dir}{_config_filename}'


# Configurable values and default values
_configurable_values = (
    'storage_loc', 
    'theme', 
    'lines_per_page'
)

DEFAULT_VALUES = {
    'storage_loc': '.',
    'theme': 'default',
    'lines_per_page': 10
}


def _open(file_name: str):
    try:
        return open(file_name, 'r'), False
    except FileNotFoundError:
        return open(file_name, 'w'), True


try:
    config_file, is_new = _open(_config_path)
    if is_new:
        _values = DEFAULT_VALUES
        config_file.write(json.dumps(_values))
    else:
        _values = json.loads(config_file.read())
finally:
    config_file.close()
