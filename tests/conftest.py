import pytest


@pytest.fixture
def hello():
    # rien à faire

    return 'hello, world\n'

    # rien à faire


@pytest.fixture
def my_monkeypatch():
    class Monkey:
        def __init__(self):
            self.backup = None

        def setattr(self, objet, method, fake):
            self.backup = getattr(objet, method)
            self.objet = objet
            self.method = method
            setattr(objet, method, fake)

    monkey = Monkey()

    yield monkey

    backup = monkey.backup
    objet = monkey.objet
    method = monkey.method
    setattr(objet, method, backup)
