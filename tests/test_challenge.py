import pytest

from codchal.settings import CHALLENGES_DIR

from codchal.challenge import Challenge

TEST_CHAL_ID = 1


@pytest.fixture
def challenge():
    return Challenge(TEST_CHAL_ID, CHALLENGES_DIR)


@pytest.mark.parametrize("value,expected",
                         [("name", "List sort"),
                          ("desc", "Simply sort a list of integer in ascending order."),
                          ("ex_inputs", ["1 2 3 4", "4 3 2 1"]),
                          ("ex_outputs", ["1 2 3 4", "1 2 3 4"]),
                          ("inputs", ["1 2 3 4", "4 3 2 1"]),
                          ("outputs", ["1 2 3 4", "1 2 3 4"])])
def test_challenge_read_chal_json(challenge, value, expected):
    assert challenge._read_chal_json(value) == expected


def generator_tester(generator, expected_vals):
    for i, (actual, expected) in enumerate(zip(generator, expected_vals)):
        assert i+1 <= len(expected_vals), 'Too many values returned from range'
        assert expected == actual
    assert i+1 == len(expected_vals), 'Too few values returned from range'


def test_challenge_inputs(challenge):
    generator_tester(challenge.inputs, ["1 2 3 4", "4 3 2 1"])


def test_challenge_outputs(challenge):
    generator_tester(challenge.outputs, ["1 2 3 4", "1 2 3 4"])


def test_challenge_io(challenge):
    generator_tester(
        challenge.io, [("1 2 3 4", "1 2 3 4"), ("4 3 2 1", "1 2 3 4")])
