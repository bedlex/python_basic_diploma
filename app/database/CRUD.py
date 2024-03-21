""" Module to get, remove, insert data from database. """
from abc import ABC

from typing import List

from app import engine, metadata
from app.database.database import users, bookmarks, history
from sqlalchemy import insert, select, delete, desc

from datetime import datetime

from app.log import error_log


class User(ABC):
    """
    Class to add and get user data from database
    """

    @classmethod
    def add_user(cls, user_id: int, username: str, first_name: str, last_name: str) -> bool | None:
        """
        Class method to add user data to database.

        Parameters:
            user_id  (int): User id.
            username (str): Username.
            first_name (str): User first name
            last_name (str): User last name
        Returns:
            bool: If method executed without errors.
            None: If method executed with some errors.
        Exceptions:
            Any exception during execution are logged,
            and method returns None
        """
        with engine.begin() as conn:
            try:
                metadata.create_all(engine)
                user_object = insert(users).values(
                    id=user_id,
                    username=username,
                    first_name=first_name,
                    last_name=last_name,
                    timestamp=datetime.utcnow()
                )
                conn.execute(user_object)
                return True
            except Exception as error:

                error_log(f"{cls.__module__}, {cls.__name__}.add_user {error}")

                return None

    @classmethod
    def get_user_by_id(cls, user_id: int) -> List[str] | None:
        """
        Class method to get information about user by id.

        Parameters:
            user_id (int): User id to search data in database.
        Returns:
            List(str): User information
            None: If query executed with some errors
        Exceptions:
            Any exception during execution are logged,
            and method returns None
        """
        with engine.begin() as conn:
            try:
                metadata.create_all(engine)
                result = conn.execute(
                    select(users).where(users.c.id == user_id)
                )
                return result.first()
            except Exception as error:

                error_log(f"{cls.__module__}, {cls.__name__}.get_user_by_id {error}")

                return None


class Bookmark(ABC):
    """
    Class Bookmark to add, get, remove bookmarks data from database.
    """

    @classmethod
    def add_to_bookmark(cls, user_id: int, symbol: str) -> bool | None:
        """
        Class method to add bookmark data into database.

        Parameters:
            user_id (int): User id.
            symbol(str): Bookmark.
        Returns:
            bool: If method executed without errors
            None: If query executed with any error
        Exceptions:
            Any exception during execution are logged,
            and method returns None
        """

        with engine.begin() as conn:
            try:
                metadata.create_all(engine)
                bookmark_object = insert(bookmarks).values(
                    user_id=user_id,
                    symbol=symbol,
                    timestamp=datetime.utcnow()
                )
                conn.execute(bookmark_object)
                return True
            except Exception as error:

                error_log(f"{cls.__module__}, {cls.__name__}.add_to_bookmark {error}")

                return None

    @classmethod
    def get_all_bookmarks(cls, user_id: int) -> List[str] | None:
        """
        Class method to get all bookmarks by specified user.

        Parameters:
            user_id (int): User id.
        Returns:
            list(str): Bookmarks list.
            None: If query executed with any error.
        Exception:
            Any exception during execution are logged,
            and method returns None
        """
        with engine.begin() as conn:
            try:
                metadata.create_all(engine)
                result = conn.execute(select(bookmarks).where(bookmarks.c.user_id == user_id))
                return result.all()

            except Exception as error:

                error_log(f"{cls.__module__}, {cls.__name__}.get_all_bookmarks {error}")

                return None

    @classmethod
    def get_bookmark(cls, user_id: int, symbol: str) -> List[str] | None:
        """
        Class method to get bookmark by user_id and symbol

        Parameters:
            user_id (int): User id
            symbol (str): Symbol
        Returns:
            list(str): List of bookmarks
            None: If query executed with any errors
        Exception:
            Any exception during execution are logged,
            and method returns None
        """
        with engine.begin() as conn:
            try:
                metadata.create_all(engine)
                result = conn.execute(select(bookmarks).where(
                    bookmarks.c.user_id == user_id,
                    bookmarks.c.symbol == symbol
                ))
                return result.all()
            except Exception as error:

                error_log(f"{cls.__module__}, {cls.__name__}.get_bookmark {error}")

                return None

    @classmethod
    def remove_bookmark(cls, user_id: int, symbol: str) -> bool | None:
        """
        Class Method to remove bookmark by specified user_id and symbol:

        Parameters:
            user_id (str): User id
            symbol (str): Symbol
        Returns:
            bool: If query executed without errors
            None: If query executed with any errors
        Exceptions:
            Any errors during execution logged,
            and method returns None
        """
        with engine.begin() as conn:
            try:
                metadata.create_all(engine)
                conn.execute(delete(bookmarks).where(
                    bookmarks.c.user_id == user_id,
                    bookmarks.c.symbol == symbol)
                )
                return True
            except Exception as error:

                error_log(f"{cls.__module__}, {cls.__name__}.remove_bookmark {error}")

                return None


class History(ABC):

    @classmethod
    def add_to_history(cls, user_id: int, request: str, respond: str) -> bool | None:
        """
        Class method to log request and respond by specified user id.

        Parameters:
            user_id(int): Specified user id
            request(str): Request
            respond(str): Respond
        Returns:
            bool: If no errors occur.
            None: IF error occur.
        """
        with engine.begin() as conn:
            try:
                metadata.create_all(engine)

                history_object = insert(history).values(
                    user_id=user_id,
                    request=request,
                    respond=respond,
                    timestamp=datetime.utcnow()
                )

                conn.execute(history_object)
                return True

            except Exception as error:

                error_log(f"{cls.__module__}, {cls.__name__}.add_to_history {error}")

                return None

    @classmethod
    def history_delete(cls, user_id: int, amount: int = 10) -> bool | None:
        """
        Method to delete records and keep specified amount rows for specified user


        Parameters:
            user_id(int): Specified user id
            amount(int): Specified amount to keep

        Returns:
            bool: if no errors occur
            None: if any errors occur
        """

        with engine.begin() as conn:
            try:
                metadata.create_all(engine)

                result = conn.execute(
                    select(history).where(history.c.user_id == user_id).order_by(desc(history.c.timestamp))).all()

                if len(result) > amount:

                    for i in range(amount, len(result)):

                        i_id = result[i][0]

                        conn.execute(delete(history).where(history.c.id == i_id))

                return True

            except Exception as error:

                error_log(f"{cls.__module__}, {cls.__name__}.history_delete {error}")

                return None

    @classmethod
    def get_history(cls, user_id: int) -> List[str] | None:
        """
        Class method to return list of searched items for specified user

        Parameters:
            user_id(int): Specified user_id

        Returns:
             List(str): List of items history
        """

        with engine.begin() as conn:
            try:
                result = conn.execute(select(history).where(history.c.user_id == user_id))

                return result.all()

            except Exception as error:

                error_log(f"{cls.__module__}, {cls.__name__}.get_history {error}")

                return None
