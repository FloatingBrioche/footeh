from pydantic import BaseModel, Field, model_validator, ConfigDict, ValidationError
from werkzeug.security import generate_password_hash


class Registration(BaseModel):
    model_config = ConfigDict(
        str_strip_whitespace=True,
        str_min_length=1,
        extra="allow"
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
        return self