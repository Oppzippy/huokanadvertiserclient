import os

ROOT_PATH = os.path.dirname(__file__)


def get_resource_path(name: str):
    return os.path.join(ROOT_PATH, name)
