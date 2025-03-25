import sqlalchemy as sa
from sqlalchemy.orm import declarative_base
from .database import engine
Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    user_id = sa.Column(sa.Integer, primary_key=True)
    email = sa.Column(sa.Text, unique=True)
    username = sa.Column(sa.Text, unique=True)
    password_hash = sa.Column(sa.Text)


class Operation(Base):
    __tablename__ = 'operations'

    operation_id = sa.Column(sa.Integer, primary_key=True)
    user_id = sa.Column(sa.Integer, sa.ForeignKey('users.user_id'))
    date = sa.Column(sa.Date)
    operation_type = sa.Column(sa.String)
    amount = sa.Column(sa.Numeric(10, 2))
    description = sa.Column(sa.String, nullable=True)

# Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)