# Third party libraries
from sqlalchemy import UUID, JSON, Column, DateTime, func, Boolean
from dataclass_type_validator import dataclass_validate
from dataclasses import dataclass

# Local libraries
from database import Base


class UserData(Base):
    """
    User Model inheriting from ActivityTracking.

    Fields:
        - first_name (str): The first name of the user.
        - last_name (str): The last name of the user.
        - email (str): The email address of the user.
        - password (str): The password of the user.
        - is_verified (bool): A flag indicating whether the user is verified or not.
        - user_role (enum) : The role of the user.
        - phone_number (str) : The phone number of the user.
    """

    __tablename__ = "user_data"
    id = Column(UUID, primary_key=True, nullable=False)
    user_data = Column(JSON, nullable=False)
    created_at = Column(DateTime(timezone=True),
                        server_default=func.now(), nullable=False)
    modified_at = Column(DateTime(timezone=True), default=func.now(),
                         onupdate=func.now(), nullable=False)
    is_active = Column(Boolean, default=True)

    def __str__(self):
        return self.id
