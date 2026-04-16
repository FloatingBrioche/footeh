from pytest import mark, raises, fixture
from pydantic import ValidationError

from utils.validators import Registration, NewGroup


@fixture
def registration():
    return {
        "email": "martin@eggs.com",
        "first_name": "Martin",
        "last_name": "Egg",
        "password": "password",
        "confirmation": "password",
    }


class TestRegistration:
    @mark.it("Raises Validation Error if not passed email")
    def test_no_email(self, registration):
        del registration["email"]
        with raises(ValidationError):
            new_user = Registration(**registration)

    @mark.it("Raises Validation Error if not passed first_name")
    def test_no_fname(self, registration):
        del registration["first_name"]
        with raises(ValidationError):
            new_user = Registration(**registration)

    @mark.it("Raises Validation Error if not passed last_name")
    def test_no_lname(self, registration):
        del registration["last_name"]
        with raises(ValidationError):
            new_user = Registration(**registration)

    @mark.it("Raises Validation Error if not passed password")
    def test_no_pass(self, registration):
        del registration["password"]
        with raises(ValidationError):
            new_user = Registration(**registration)

    @mark.it("Raises Validation Error if not passed confirmation")
    def test_no_confirm(self, registration):
        del registration["confirmation"]
        with raises(ValidationError):
            new_user = Registration(**registration)

    @mark.it("Raises Validation Error if password != confirmation")
    def test_pass_not_confirm(self, registration):
        registration["confirmation"] = "possward"
        with raises(ValidationError):
            new_user = Registration(**registration)

    @mark.it("Raises Validation Error if password < 8")
    def test_short_pass(self, registration):
        registration["password"] = "passwor"
        with raises(ValidationError):
            new_user = Registration(**registration)

    @mark.it("Instantiates object if passed valid k-v args")
    def test_valid_args(self, registration):
        new_user = Registration(**registration)
        assert True

    @mark.it("Object has password_hash attr")
    def test_valid_args_has_hash(self, registration):
        new_user = Registration(**registration)
        assert new_user.password_hash

    @mark.it("model_dump() returns only wanted keys")
    def test_model_dump(self, registration):
        new_user = Registration(**registration)
        model_dump = new_user.model_dump()
        required_keys = {"email", "first_name", "last_name", "password_hash"}
        assert set(model_dump.keys()) == required_keys
