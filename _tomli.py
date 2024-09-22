import tomli as toml_loader
import tomli_w as toml_write


class tomli:
    @staticmethod
    def load(file: bytes) -> dict:
        return toml_loader.load(file)

    @staticmethod
    def dump(file: bytes, data: dict) -> None:
        return toml_write.dump(file, data)

def get_config(key, default=None):
    with open('config.toml', 'rb') as file:
        data = tomli.load(file)
    return data.get(key, default)
