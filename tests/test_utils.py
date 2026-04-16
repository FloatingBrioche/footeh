from pytest import mark, raises, fixture
from pydantic import ValidationError

from app.utils import generate_join_code


@mark.it("Generates join code <= 30 words")
def test_code_le_30():
    join_code = generate_join_code()
    assert len(join_code) <= 30