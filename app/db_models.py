from datetime import datetime, date, time
from decimal import Decimal
from typing import Optional

import sqlalchemy as sa
import sqlalchemy.orm as so
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)


class User(db.Model):
    __tablename__ = "users"

    id: so.Mapped[int] = so.mapped_column(primary_key=True, autoincrement=True)
    first_name: so.Mapped[str] = so.mapped_column(sa.String(100))
    last_name: so.Mapped[str] = so.mapped_column(sa.String(100))
    email: so.Mapped[str] = so.mapped_column(sa.String(200), index=True, unique=True)
    created_at: so.Mapped[datetime] = so.mapped_column(
        sa.DateTime, server_default=sa.func.now()
    )
    password_hash: so.Mapped[str] = so.mapped_column(sa.String(256))

    __table_args__ = (sa.CheckConstraint("email LIKE '_%@%_'", name="email_check"),)

    def __repr__(self):
        return f"User: {self.first_name} {self.last_name}, ID: {self.id}, email: {self.email}"


class Group(db.Model):
    __tablename__ = "groups"

    id: so.Mapped[int] = so.mapped_column(primary_key=True, autoincrement=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(100))
    join_code: so.Mapped[str] = so.mapped_column(sa.String(30), unique=True)
    created_at: so.Mapped[datetime] = so.mapped_column(
        sa.DateTime, server_default=sa.func.now()
    )
    status: so.Mapped[str] = so.mapped_column(sa.String(10), server_default="active")
    game_location: so.Mapped[str] = so.mapped_column(sa.Text)
    game_day: so.Mapped[str] = so.mapped_column(sa.String(10))
    game_time: so.Mapped[time] = so.mapped_column(sa.Time)
    game_cost: so.Mapped[Decimal] = so.mapped_column(sa.Numeric(10, 2))
    min_players: so.Mapped[int] = so.mapped_column(sa.Integer)
    max_players: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer)
    require_even_num_players: so.Mapped[bool] = so.mapped_column(
        sa.Boolean, server_default=sa.true()
    )
    payment_instructions: so.Mapped[Optional[str]] = so.mapped_column(sa.Text)

    __table_args__ = (
        sa.CheckConstraint(
            "game_day IN ('Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday')",
            name="game_day_check",
        ),
    )

    def __repr__(self):
        return f"Group: {self.name}, ID: {self.id}, Status: {self.status}, Location: {self.game_location}"


class Membership(db.Model):
    __tablename__ = "memberships"

    id: so.Mapped[int] = so.mapped_column(primary_key=True, autoincrement=True)
    user_id: so.Mapped[int] = so.mapped_column(
        sa.Integer, sa.ForeignKey("users.id", ondelete="CASCADE")
    )
    group_id: so.Mapped[int] = so.mapped_column(
        sa.Integer, sa.ForeignKey("groups.id", ondelete="CASCADE")
    )
    joined_at: so.Mapped[date] = so.mapped_column(
        sa.DateTime, server_default=sa.func.current_date()
    )
    role: so.Mapped[str] = so.mapped_column(sa.String(20), server_default="player")
    status: so.Mapped[str] = so.mapped_column(sa.String(10), server_default="active")

    __table_args__ = (
        sa.CheckConstraint(
            "role IN ('organiser','player')",
            name="role_check",
        ),
    )

    def __repr__(self):
        return f"Membership: User ID: {self.user_id}, Group ID: {self.group_id}, Role: {self.role}, Status: {self.status}"


class League(db.Model):
    __tablename__ = "leagues"

    id: so.Mapped[int] = so.mapped_column(primary_key=True, autoincrement=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(100))
    group_id: so.Mapped[int] = so.mapped_column(
        sa.Integer, sa.ForeignKey("groups.id", ondelete="CASCADE")
    )
    start_date: so.Mapped[date] = so.mapped_column(
        sa.Date, server_default=sa.func.current_date()
    )
    end_date: so.Mapped[date] = so.mapped_column(
        sa.Date, server_default=sa.func.current_date() + sa.text("INTERVAL '6 months'")
    )

    __table_args__ = (
        sa.CheckConstraint("end_date > start_date", name="end_date_check"),
    )

    def __repr__(self):
        return f"League: {self.name}, ID: {self.id}, Group ID: {self.group_id}"


class Game(db.Model):
    __tablename__ = "games"

    id: so.Mapped[int] = so.mapped_column(primary_key=True, autoincrement=True)
    group_id: so.Mapped[int] = so.mapped_column(
        sa.Integer, sa.ForeignKey("groups.id", ondelete="CASCADE")
    )
    league_id: so.Mapped[Optional[int]] = so.mapped_column(
        sa.Integer, sa.ForeignKey("leagues.id", ondelete="SET NULL")
    )
    game_location: so.Mapped[str] = so.mapped_column(sa.Text)
    game_date: so.Mapped[date] = so.mapped_column(sa.Date)
    game_time: so.Mapped[time] = so.mapped_column(sa.Time)
    game_cost: so.Mapped[Decimal] = so.mapped_column(sa.Numeric(10, 2))
    min_players: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer)
    max_players: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer)
    team_a_goals: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer)
    team_b_goals: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer)

    def __repr__(self):
        return f"ID: {self.id}, Group ID: {self.group_id}, Location: {self.game_location}, Date: {self.game_date}, Time: {self.game_time}"


class Appearance(db.Model):
    __tablename__ = "appearances"

    id: so.Mapped[int] = so.mapped_column(primary_key=True, autoincrement=True)
    user_id: so.Mapped[int] = so.mapped_column(
        sa.Integer, sa.ForeignKey("users.id", ondelete="CASCADE")
    )
    game_id: so.Mapped[int] = so.mapped_column(
        sa.Integer, sa.ForeignKey("games.id", ondelete="CASCADE")
    )
    team: so.Mapped[str] = so.mapped_column(sa.String(1))  # 'A' or 'B'
    has_paid: so.Mapped[bool] = so.mapped_column(sa.Boolean, server_default=sa.false())

    __table_args__ = (
        sa.CheckConstraint(
            "team IN ('A','B')",
            name="team_check",
        ),
    )

    def __repr__(self):
        return f"Appearance: User ID: {self.user_id}, Game ID: {self.game_id}, Team: {self.team}, Paid: {self.has_paid}"
