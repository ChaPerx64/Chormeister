import pytest


@pytest.fixture
def fixture_1():
    print('run fixture 1')
    return 1


def test_landing(fixture_1):
    num = fixture_1
    assert num == 1
