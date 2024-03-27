from datetime import datetime

from flask_login import UserMixin
from flask_sqlalchemy.model import Model
from sqlalchemy import Column, DateTime, Integer, String, Boolean, Text
from sqlalchemy.orm import declarative_base
from werkzeug.security import check_password_hash


Base = declarative_base()


class Task(Base):
    __tablename__ = 'tasks'
    id = Column(Integer(), primary_key=True)
    author = Column(String(40), nullable=False)
    email = Column(String(128), nullable=False)
    text = Column(Text(), nullable=False)
    done = Column(Boolean(), default=False)
    changed = Column(Boolean(), default=False)
    created_at = Column(DateTime(), default=datetime.utcnow)
    updated_at = Column(DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"{self.id}: {self.author}"

    @property
    def to_dict(self):
        return {
            'id': self.id,
            'author': self.author,
            'email': self.email,
            'text': self.text,
            'done': self.done,
            'changed': self.changed,
        }


class User(UserMixin, Base):
    __tablename__ = 'users'
    id = Column(Integer(), primary_key=True)
    username = Column(String(32), nullable=False, unique=True)
    email = Column(String(128), nullable=False, default='test@test.com')
    password_hash = Column(String(192), nullable=False)
    is_admin = Column(Boolean(), default=False)
    created_at = Column(DateTime(), default=datetime.utcnow)
    updated_at = Column(DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"{self.id}: {self.username}"

    @property
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'is_admin': self.is_admin,
        }

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
