from typing import Optional

import sqlalchemy as sa
import sqlalchemy.orm as so

from app import db


class User(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    first_name: so.Mapped[str] = so.mapped_column(sa.String(100))
    last_name: so.Mapped[str] = so.mapped_column(sa.String(100))
    email: so.Mapped[str] = so.mapped_column(sa.String(200), index=True, unique=True)
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))

    def __repr__(self):
        return f'User: {self.first_name} {self.last_name}, ID: {self.id}, email: {self.email}'