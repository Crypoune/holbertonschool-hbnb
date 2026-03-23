from app.models.base_model import BaseModel
import re


class User(BaseModel):
    def __init__(self, first_name, last_name, email, is_admin=False):
        super().__init__()
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = is_admin

    @property
    def first_name(self):
        return self._first_name

    @first_name.setter
    def first_name(self, value):
        if not value or not isinstance(value, str) or not value.strip():
            raise ValueError("First name is required and must be a string")
        self._first_name = value.strip()

    @property
    def last_name(self):
        return self._last_name

    @last_name.setter
    def last_name(self, value):
        if not value or not isinstance(value, str) or not value.strip():
            raise ValueError("Last name is required and must be a string")
        self._last_name = value.strip()

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, value):
        if not value or not isinstance(value, str):
            raise ValueError("Email is required and must be a string")
        value = value.strip().lower()
        if not re.fullmatch(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', value):
            raise ValueError("Invalid email format")
        self._email = value

    def to_dict(self):
        d = super().to_dict()
        d['first_name'] = self.first_name
        d['last_name'] = self.last_name
        d['email'] = self.email
        d['is_admin'] = self.is_admin
        return d
