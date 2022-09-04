import pytest

from codchal.settings import CHALLENGES_DIR

from codchal.challenge import Challenge

TEST_CHAL_ID = 1

@pytest.fixture
def challenge():
    return Challenge(TEST_CHAL_ID, CHALLENGES_DIR)

def test_challenge_arguments_id(challenge):
    assert challenge.id == TEST_CHAL_ID

def test_challenge_arguments_chal_file(challenge):
    assert challenge.chal_file == CHALLENGES_DIR+str(TEST_CHAL_ID)+".json"
    
