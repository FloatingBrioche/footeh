from pytest import mark, raises, fixture


from utils.aux_functions import generate_join_code, is_jcode_unique


class TestGenerateJoinCode:
    @mark.it("Generates join code <= 30 words")
    def test_code_le_30(self):
        join_code = generate_join_code()
        assert len(join_code) <= 30


class TestIsUniqueJCode:
    @mark.it("Returns True if jcode not in current jcodes")
    def test_returns_true(self, mock_db):
        assert is_jcode_unique("eggy-egg-egg", mock_db)
