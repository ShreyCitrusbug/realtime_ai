"""
This file contains the service class for user data.
"""
# Python in build libraries
from typing import Annotated, List, Tuple, Union

# third party libraries
from sqlalchemy.orm import Session
from fastapi import Depends
from sqlalchemy import exc

# local imports
from models import UserData
from dependencies import get_db


class UserDataService:
    """
    Service class for user data.
    """

    def __init__(self, db: Annotated[Session, Depends(get_db)]):
        self.db = db

    def insert_user_data(self, user_data: dict) -> dict:
        """
        Insert user data into the database.

        Args:
            user_data (dict): The user data to be inserted.

        Returns:
            UserData: The inserted user data.
        """
        try:
            user_data = UserData(**user_data)
            self.db.add(user_data)
            self.db.commit()
            self.db.refresh(user_data)
            user_data_dict = {
                "id": user_data.id,
                "user_data": user_data.user_data
            }
            return user_data_dict
        except exc.SQLAlchemyError as sqe:
            self.db.rollback()
            raise sqe
        except Exception as e:
            raise e
