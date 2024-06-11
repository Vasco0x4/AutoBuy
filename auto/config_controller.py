import yaml


CONFIG_FILE_PATH = "config.yaml"


class ConfigController:
    # TODO: config validation

    @staticmethod
    def get_config():
        with open(CONFIG_FILE_PATH, "r", encoding="utf8") as f:
            return yaml.safe_load(f)

BITGET_API_KEY = ''
BITGET_SECRET_KEY = ''
BITGET_BASE_URL = ''
BITGET_PASSPHRASE = ''

close_position_delay = 10