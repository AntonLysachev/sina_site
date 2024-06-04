import os

TESTS_DIR = os.path.dirname(os.path.dirname(__file__))
FIXTURES_PATH = f"{TESTS_DIR}/fixtures"


def build_fixture_path(file_name):
    return os.path.join(FIXTURES_PATH, file_name)


def get_content(addres):
    with open(addres, 'r') as f:
        data = f.read()
        return data
