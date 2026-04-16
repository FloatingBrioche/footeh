from decimal import Decimal
from datetime import time

from pydantic import BaseModel, Field, model_validator, ConfigDict, computed_field
from werkzeug.security import generate_password_hash


class Registration(BaseModel):
    model_config = ConfigDict(
        str_strip_whitespace=True, str_min_length=1, extra="allow"
    )
    email: str = Field(pattern=r".+@.+", max_length=254)
    first_name: str = Field(max_length=100)
    last_name: str = Field(max_length=100)

    @model_validator(mode="after")
    def validate_passwords(self):
        password = self.__pydantic_extra__.get("password")
        confirmation = self.__pydantic_extra__.get("confirmation")

        if not all([password, confirmation]):
            raise ValueError("Missing password or confirmation.")

        if password != confirmation:
            raise ValueError("Passwords do not match.")

        if len(password) < 8:
            raise ValueError("Password must be at least 8 characters long.")

        self.password_hash = generate_password_hash(password)
        del self.password
        del self.confirmation
        return self


class NewGroup(BaseModel):
    model_config = ConfigDict(
        str_strip_whitespace=True
    )
    name: str = Field(max_length=100)
    game_location: str
    game_day: str = Field(pattern=r"^(Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday)$")
    game_time: time = Field(pattern=r"^\d{2}:\d{2}$")  # HH:MM format
    game_cost: Decimal = Field(ge=0)
    min_players: int | None = Field(ge=1)
    max_players: int | None = Field(ge=1)
    require_even_num_players: bool = True
    payment_instructions: str | None = None

    @computed_field
    @property
    def join_code(self) -> str:
        return "egg-egg-egg"