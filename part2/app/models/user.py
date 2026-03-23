from app.models import BaseModel
import re


class User(BaseModel):
    """
    User model representing a user in the system.
    Can be a guest or a property owner.
    """

    def __init__(self, first_name, last_name, email, password, is_admin=False):
        super().__init__()
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.is_admin = is_admin

    # ===================== FIRST NAME =====================

    @property
    def first_name(self):
        return self._first_name

    @first_name.setter
    def first_name(self, value):
        if not value or not isinstance(value, str):
            raise ValueError("First name is required and must be a string")
        value = value.strip()
        if not value:
            raise ValueError("First name cannot be empty")
        self._first_name = value

    # ===================== LAST NAME =====================

    @property
    def last_name(self):
        return self._last_name

    @last_name.setter
    def last_name(self, value):
        if not value or not isinstance(value, str):
            raise ValueError("Last name is required and must be a string")
        value = value.strip()
        if not value:
            raise ValueError("Last name cannot be empty")
        self._last_name = value

    # ===================== EMAIL =====================

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, value):
        self._email = self._validate_email(value)

    @staticmethod
    def _validate_email(email):
        if not email or not isinstance(email, str):
            raise ValueError("Email is required and must be a string")
        email = email.strip().lower()
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.fullmatch(email_regex, email):
            raise ValueError("Invalid email format")
        return email

    # ===================== PASSWORD =====================

    @property
    def password(self):
        return None  # non lisible pour sécurité

    @password.setter
    def password(self, value):
        if not value or not isinstance(value, str):
            raise ValueError("Password is required and must be a string")
        self._password = value  # hashing en partie 3

    # ===================== SERIALIZATION =====================

    def to_dict(self):
        """Convert User to dictionary — password exclu."""
        user_dict = super().to_dict()
        user_dict["first_name"] = self.first_name
        user_dict["last_name"] = self.last_name
        user_dict["email"] = self.email
        user_dict["is_admin"] = self.is_admin
        return user_dict
