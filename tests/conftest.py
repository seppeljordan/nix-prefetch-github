from pytest import fixture

from .url_hasher import FakeUrlHasher


@fixture
def url_hasher():
    return FakeUrlHasher()
