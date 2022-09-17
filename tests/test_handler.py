from os.path import exists
import uuid
import pytest

from codchal.errors import LanguageError, SolutionFormatError
from codchal.handler import SolHandler
from codchal.settings import DEFAULT_DIR

RAW_SOL = """```python
          test for test
          ```"""
# changing random behaviour of uuid to reproductible
RANDOM_SEED = 1
uuid.uuid4 = lambda: uuid.UUID(int=RANDOM_SEED)
TEST_FILENAME = str(uuid.uuid4())


@pytest.fixture
def handler():
    hand = SolHandler(RAW_SOL)
    return hand


def test_handler_parse_sol_wrong_format():
    with pytest.raises(SolutionFormatError):
        SolHandler("badly formated solution")


def test_handler_parse_sol_no_language():
    with pytest.raises(SolutionFormatError):
        SolHandler("""```
        missing language here
        ```""")


def test_handler_parse_sol_unknown_language():
    with pytest.raises(LanguageError):
        SolHandler("""```java
        Unknown language
        ```""")


def test_handler_parse_sol_python(handler):
    assert handler.script_filename == TEST_FILENAME+".py"
    assert handler.lang == "python"


def test_handler_parse_sol_script_created():
    handler = SolHandler(RAW_SOL)
    assert exists(DEFAULT_DIR+handler.script_filename)


def test_handler_destructor_script_deleted():
    handler = SolHandler(RAW_SOL)
    full_fp = DEFAULT_DIR+handler.script_filename
    # making sure the script is created
    assert exists(full_fp)
    del handler
    assert not exists(full_fp)
