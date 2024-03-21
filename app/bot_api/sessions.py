from datetime import datetime
from typing import Any

from app import bot


class SessionMaker:
    """
    class SessionMaker to handle sessions in TeleBot.
    """

    def __init__(self) -> None:
        """
        class method for initialize class object.
        created dictionary self.__sessions to.
        keep all user instances in it.
        """
        self.__sessions = dict()

    def start_session(self, user_id: int, chat_id: int, start_message_id: int) -> None:
        """
        Class method to add new user by specified user id.

        Parameters:
            user_id(int): Specified user id.
        """
        if user_id not in self.__sessions:
            self.__sessions[user_id] = {
                "chat_id": chat_id,
                "start_message_id": start_message_id,
                "current_message_id": start_message_id,
                "timestamp": datetime.utcnow(),
            }

    def end_session(self, user_id: int) -> None:
        """
        Class method to delete all data from session by specified user id.

        Parameters:
            user_id(int): Specified user id.
        """
        if user_id in self.__sessions:
            del self.__sessions[user_id]

    def get_data(self, user_id: int, key: Any) -> Any:
        """
        Class method to get data from session by specified user id.
        and specified key.

        Parameters:
            user_id(int): Specified user id .
            key(Any): Specified key.
        Returns:
             Any: Data to get.
        """
        return self.__sessions.get(user_id, {}).get(key)

    def set_data(self, user_id: int, key: Any, data: Any):
        """
        class method to set data by specified user id and specified key.

        Parameters:
            user_id(int): Specified user id.
            key(Any): Specified key.
            data(Any): Data to set.
        """
        if user_id in self.__sessions:
            self.__sessions[user_id][key] = data

    def is_exist(self, user_id: int) -> bool:
        """
        class method to check if user in session.

        Parameters:
            user_id(int): Specified user id.

        Returns:
            bool: True if user exist else False.
        """
        if self.__sessions.get(user_id, None):
            return True

        return False

    def increase_current_message_id(self, user_id: int) -> None:
        """
        Class method to increase current_message_id value for specified user by one if exits.
        if not created current_message_id with value equal to start_message_id + 1

        Parameters:
            user_id (int): Specified user id
        Returns:
            None:
        """
        # Check if current_message_id in dictionary
        if self.__sessions.get(user_id, {}).get("current_message_id"):
            # if it in dictionary increase by one
            self.__sessions[user_id]["current_message_id"] += 1

    def delete_user_messages(self, user_id: int, user_current_message_id: int) -> None:
        """
        Class method to delete all messages from session by specified user_id

        Parameters:
            user_id(int): Specified user id
            user_current_message_id(int): Current message id
        Returns:
            None
        """
        start_message_id = self.__sessions.get(user_id, {}).get("start_message_id")
        current_message_id = self.__sessions.get(user_id, {}).get("current_message_id")
        chat_id = self.__sessions.get(user_id, {}).get("chat_id")

        if start_message_id and current_message_id and chat_id:
            for message_id in range(start_message_id, current_message_id, 1):
                try:
                    bot.delete_message(chat_id=chat_id, message_id=message_id)
                except Exception:
                    continue

        self.set_data(user_id=user_id, key="start_message_id", data=user_current_message_id)
        self.set_data(user_id=user_id, key="current_message_id", data=user_current_message_id)

    def __repr__(self) -> str:
        """
        class method to print class instance

        Returns:
            str: class object
        """
        return f"{self.__sessions}"
