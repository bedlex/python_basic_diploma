""" Module to handle all inputs for telebot """
from telebot.types import Message, CallbackQuery
from typing import Callable, Any, Dict
from functools import wraps

from app import bot, stock
from telebot import types

from app.bot_api.libs import validate_dates, custom_dict_to_string

from app.database.CRUD import User, Bookmark, History

from app.bot_api.sessions import SessionMaker

session = SessionMaker()


def user_check(func: Callable) -> Callable:
    """
    Function decorator to check if global variable user have some value,
    If not required to press start button for redirect.

    Parameters:
        func (Callable): function to decorate

    Returns:
        wrapper (Callable): Decorated function
    """

    @wraps(func)
    def wrapper(answer: Message | CallbackQuery) -> None:
        """
        Function wrapper to check if user exists in session

        Parameters:
            answer(Message | CallbackQuery) :
        Returns:
            Callable: wrapped function
            None: if user id not in session
        """
        # Get user id
        user_id = answer.from_user.id
        # check if user exists in session
        if session.is_exist(user_id):
            # Get current message id
            session.increase_current_message_id(user_id=user_id)
            # Wrapped function
            func(answer)

        else:
            # Create custom keyboard
            keyboard = types.ReplyKeyboardMarkup()
            # Create custom button
            button = types.KeyboardButton("/start")
            # Add button to keyboard
            keyboard.row(button)
            # Send message to user
            bot.send_message(answer.chat.id, "To continue press start button", reply_markup=keyboard)

    return wrapper


@bot.message_handler(commands=["start"])
def start(message: Message) -> None:
    """
    Handle the start command
        Assign global variables user and start_id.

    Parameters:
        message (Message): The incoming message

    Returns:
        None
    """
    # Get user id
    user_id = message.from_user.id
    # Get chat id
    chat_id = message.chat.id
    # Delete messages if any exists.
    session.delete_user_messages(user_id=user_id, user_current_message_id=message.message_id)
    # Start user session
    session.start_session(user_id=user_id, chat_id=chat_id, start_message_id=message.message_id)
    # Redirect to main menu
    main_menu(message)


@bot.message_handler(commands=["high"])
@user_check
def high(message: Message):
    """
        Function to handle /high command from user in Telegram bot.

        Parameters:
        - message (telebot.types.Message): The Telegram message object containing the
        /high command and the stock symbol.

        Returns:
        - None.

        Raises:
        - ValueError: If the input is not as expected, a message will be sent to the user
        indicating an error has occurred.
    """
    # Get chat id
    chat_id = message.chat.id

    try:
        # Get article
        _, article = message.text.strip().split()
        # Get stock highest price for today
        result = stock.high(symbol=article)
        # Sent message
        bot.send_message(chat_id, f"Stock '{article.upper()}' maximum price today: ${result}")
    except ValueError:
        bot.send_message(chat_id, "Something went wrong!\n"
                                  "/high SYMBOL\n"
                                  "example: "
                                  "/high IBM")


@bot.message_handler(commands=["low"])
@user_check
def low(message: Message):
    """
        Function to handle /low command from user in Telegram bot.

        Parameters:
        - message (telebot.types.Message): The Telegram message object containing the
        /low command and the stock symbol.

        Returns:
        - None.

        Raises:
        - ValueError: If the input is not as expected, a message will be sent to the user
        indicating an error has occurred.
    """
    # Get chat id
    chat_id = message.chat.id

    try:
        # Get article
        _, article = message.text.strip().split()
        # Get stock highest price for today
        result = stock.low(symbol=article)
        # Sent message
        bot.send_message(chat_id, f"Stock '{article.upper()}' lowest price today: ${result}")
    except ValueError:
        bot.send_message(chat_id, "Something went wrong!\n"
                                  "/low SYMBOL\n"
                                  "example: "
                                  "/low IBM")


@bot.message_handler(commands=["custom"])
@user_check
def custom(message: Message):
    """
     Function to get specified stock symbol by specified date frame.

     Args:
         message (Message): Incoming message object from the user.

     Returns:
         None

     Raises:
         ValueError: When there is an issue with the input parameters.
     """
    # Get chat id
    chat_id = message.chat.id
    # Assign variables symbol, from_date, to_date
    try:
        _, symbol, from_date, to_date, = message.text.strip().split()
        # Validating dates
        from_date, to_date = validate_dates(from_date=from_date, to_date=to_date)

        if from_date and to_date and symbol != "":
            result = stock.custom(symbol=symbol, from_date=from_date, to_date=to_date)
            if result:

                for date, history_chart in result:
                    history_date_string = f"stock symbol: {symbol.upper()}\ndate: {date}\n\n"

                    for el in history_chart:
                        history_date_string = f"{history_date_string}\n{custom_dict_to_string(el)}"

                    bot.send_message(chat_id, history_date_string)
            else:
                bot.send_message(chat_id, f"SYMBOL not found")
        else:
            raise ValueError

    except ValueError:
        bot.send_message(chat_id, 'Something went wrong!\n'
                                  '/custom SYMBOL FROM_DATE TO_DATE\n'
                                  'example:\n'
                                  '/custom IBM 2022-05-12 2022-05-18')


@bot.message_handler(commands=["history"])
@user_check
def history(message: Message) -> None:
    """
    Set the full item search history for specified user

    Parameters:
        message (Message): The incoming message

    Returns:
         None
    """

    # Get user id
    user_id = message.from_user.id
    # Get chat id
    chat_id = message.chat.id
    # Get first name
    first_name = message.from_user.first_name
    # Get last name
    last_name = message.from_user.last_name
    # Delete previous messages
    session.delete_user_messages(user_id=user_id, user_current_message_id=message.message_id)
    # Get user history
    user_history = History.get_history(user_id=user_id)

    for el in user_history:
        bot.send_message(chat_id, f'User "{first_name} {last_name}" request: {el[1]}\n\nServer response:\n{el[2]}')


@bot.message_handler(commands=["help"])
def help_route(message: Message):
    """
        Function to handle /help command from user in Telegram bot.

        Parameters:
        - message (telebot.types.Message): The Telegram message object containing the
        /help command.

        Returns:
        - None.

        Raises:
        - ValueError: If the input is not as expected, a message will be sent to the user
        indicating an error has occurred.
    """
    # Get chat id
    chat_id = message.chat.id

    help_message = f"Hello! Here are some commands you can use:\n\n" \
                   "/high SYMBOL - Displays the highest stock price for a given symbol on the current day.\n" \
                   "example: /high IBM\n\n" \
                   "/low SYMBOL - Displays the lowest stock price for a given symbol on the current day.\n" \
                   "example: /low IBM\n\n" \
                   "/custom SYMBOL FROM_DATE TO_DATE - Retrieves the specific stock history for a given" \
                   " symbol between two specified dates.\n" \
                   "example: /custom IBM 2022-05-12 2022-05-18\n\n" \
                   "/history - Displays the history of all your previous searches for a symbol.\n\n" \
                   "\n\t\t*******Buttons menu*******\n" \
                   "\n\n\t\t****Main menu****\n" \
                   '- Search by "company symbol:  Searches for a company by its stock symbol\n' \
                   '- Search by "company name": Searches for a company by its name\n' \
                   "- Bookmarks: Displays the user\'s bookmarked companies\n" \
                   '\n\n\t\t****Search by "company symbol"****\n' \
                   'Enter a valid symbol to go on company profile\n' \
                   'For instance, you can use "/s AAPL" for Apple Inc., or "/s GOOGL" for Alphabet Inc. (Google)\n' \
                   'Additionally, ensure that the entered symbol is spelled correctly and in its standard form.\n' \
                   "- Main menu: Redirect to main menu" \
                   '\n\n\t\t****Search by "company name"****\n' \
                   'To begin a search, kindly provide the exact name or a partial match of the desired company.\n' \
                   'The system will then return a list of potential matches based on your input\n' \
                   'For instance, you can use "Microsoft Corporation" or simply "Microsoft".\n' \
                   'Please note that the search results may include items with names resembling your input as well.\n' \
                   "- Main menu: Redirect to main menu" \
                   '\n\n\t\t****Bookmarks****\n' \
                   "View and manage your list of bookmarked companies.\n" \
                   "- Main menu: Redirect to main menu" \
                   f"\n\n\t\t****Company profile****\n" \
                   '- Get price change - Obtain detailed historical price data for this company,' \
                   'from the past decade up until the present.\n' \
                   '- Remove from bookmarks:  Delete this company from your list of bookmarked companies.\n' \
                   '- Add to bookmarks:  Bookmark this company to easily access its profile in the future.\n' \
                   '- Bookmarks: Displays the user\'s bookmarked companies\n' \
                   "- Main menu: Redirect to main menu"

    bot.send_message(chat_id, help_message)


@user_check
def main_menu(message: Message) -> None:
    """
    Function to handle main menu.
    Assign start_id global variable.
    Redirect:
        Search by "company symbol"
        Search by "company name"
        Bookmarks
    Parameters:
        message (Message): The incoming message

    Returns None
    """
    # Get specified user id
    user_id = message.from_user.id
    # Delete all previous messages
    session.delete_user_messages(user_id=user_id, user_current_message_id=message.message_id)
    # Create custom keyboard with buttons
    markup = types.ReplyKeyboardMarkup()
    # Created custom buttons
    symbol_search_btn = types.KeyboardButton('Search by "company symbol":')
    company_search_btn = types.KeyboardButton('Search by "company name":')
    bookmarks_btn = types.KeyboardButton('Bookmarks')
    # add buttons to keyboard rows
    markup.row(symbol_search_btn)
    markup.row(company_search_btn)
    markup.row(bookmarks_btn)
    # send message to user
    bot.send_message(message.chat.id, f'Choose action:', reply_markup=markup)


@user_check
def symbol_search(message: Message) -> None:
    """
    Function to Hande search stock menu.
    Assign search_type global variable
    Redirect:
        Main menu
    Parameters:
        message(Message): The incoming message

    Returns:
        None
    """
    # Get specified user id
    user_id = message.from_user.id
    # Delete all previous messages
    session.delete_user_messages(user_id=user_id, user_current_message_id=message.message_id)
    # Set session object search_type equal to symbol by specified user id
    session.set_data(user_id=user_id, key="search_type", data="symbol")
    # Create custom keyboard with buttons
    keyboard = types.ReplyKeyboardMarkup()
    # Create custom button for keyboard
    main_menu_btn = types.KeyboardButton('Main menu')
    # Add button to keyboard row
    keyboard.row(main_menu_btn)
    # Send message to user
    bot.send_message(message.chat.id, f'Enter company symbol:', reply_markup=keyboard)


@user_check
def company_search(answer: Message | CallbackQuery) -> None:
    """
    Function to handle company search menu.
    Assign global variable search_type
    Redirect:
        Main menu
    Parameters:
        answer (Message): The incoming message

    Returns:
         None
    """
    # Get specified user id
    user_id = answer.from_user.id

    # Check if answer is message or callback object
    if isinstance(answer, Message):
        message = answer
    else:
        # elif isinstance(answer, CallbackQuery):
        message = answer.message
    # Get message id
    message_id = message.message_id
    # Delete all previous messages
    session.delete_user_messages(user_id=user_id, user_current_message_id=message_id)

    # Set session object search_type equal to company by specified user id
    session.set_data(user_id=user_id, key="search_type", data="company")
    # Created keyboard with buttons
    keyboard = types.ReplyKeyboardMarkup()
    # Create custom button
    main_menu_btn = types.KeyboardButton('Main menu')
    # Add custom button to keyboard
    keyboard.row(main_menu_btn)
    # Send message to user
    bot.send_message(message.chat.id, f'Enter company name:', reply_markup=keyboard)


@user_check
def item(answer: Message | CallbackQuery) -> None:
    """
    Function to handle item menu.
    Assign global variable article, if got response from Stock API
    Redirect to:
            Add to bookmark/ Remove bookmark
            Get price change
            Main menu
    Parameters:
        answer (Message | CallbackQuery): The incoming message

    Returns:
         None
    """
    # Get user id from answer
    user_id: int = answer.from_user.id

    if isinstance(answer, Message):
        # Assign message from message
        message = answer
        article = message.text.upper()
        session.set_data(user_id=user_id, key="article", data=article)
    else:
        # elif isinstance(answer, CallbackQuery):
        # Assign message from callback
        message = answer.message
        # Get searchable article from session by specified id
        article = session.get_data(user_id=user_id, key="article")

    # Get stock from stock_api
    result = stock.get_stock(article)
    # Check if result exist
    if not result:
        # If not redirect to company_search
        company_search(answer)
        return

    # Add to history
    History.add_to_history(
        user_id=user_id,
        request=result.get('symbol'),
        respond=result.get('company')
    )
    # Delete extra history from database
    History.history_delete(user_id=user_id)
    # Create custom keyboard with custom buttons
    keyboard = types.ReplyKeyboardMarkup()
    # Check if bookmark with specified article exist
    if Bookmark.get_bookmark(user_id=user_id, symbol=article):
        # If bookmark exist create button "Remove from bookmarks"
        bookmark_btn = types.KeyboardButton("Remove from bookmarks")
    else:
        # If bookmark not exist create button "Add to bookmarks"
        bookmark_btn = types.KeyboardButton("Add to bookmarks")
    # Create custom buttons for keyboard
    price_change_btn = types.KeyboardButton("Get price change")
    bookmarks_btn = types.KeyboardButton('Bookmarks')
    main_menu_btn = types.KeyboardButton("Main menu")
    # Add buttons to keyboard
    keyboard.row(price_change_btn)
    keyboard.row(bookmark_btn)
    keyboard.row(bookmarks_btn)
    keyboard.row(main_menu_btn)
    # Send message to user
    bot.send_message(message.chat.id, f"{result.get('company')}.", reply_markup=keyboard)


@user_check
def companies(message: Message) -> None:
    """
    Function to perform companies search based by user incoming message.
    Created redirect button for each founded company.
    Redirect to main menu.

    Parameters:
        message (Message): The incoming message

    Returns:
        None

    """
    # Get specified user id
    user_id = message.from_user.id
    # Created keyboard with custom button
    markup = types.ReplyKeyboardMarkup()
    # Created custom button for keyboard
    main_menu_btn = types.KeyboardButton("Main menu")
    # Add button to keyboard
    markup.row(main_menu_btn)
    # list of companies information with specified limit from Stock API
    bot.send_message(message.chat.id, f'Companies search result for: "{message.text}.', reply_markup=markup)
    # Loop through each company in result
    result: Dict[str, Any] | None = stock.company_search(message.text, limit=10)
    # send message to user
    if result:
        for el, value in result.items():
            # Add each message id to session by specified user id
            session.increase_current_message_id(user_id=user_id)
            # Created keyboard with custom button
            el_markup = types.InlineKeyboardMarkup()
            # Created custom button for keyboard
            open_profile = types.InlineKeyboardButton("Open company profile", callback_data=f"item|{el}")
            # Add button for keyboard
            el_markup.row(open_profile)
            # send message to user
            bot.send_message(message.chat.id, f"{value}.", reply_markup=el_markup)


#
@user_check
def price_change(message: Message) -> None:
    """
    Function to handle price change menu
    Get result from Stock API
    Redirect to main menu

    Parameters:
        message (Message): Incoming message
    Returns:
        None
    """
    user_id = message.from_user.id
    article = session.get_data(user_id=user_id, key="article")
    # Get response from Stock Api and assign variable
    result: str | None = stock.price_change(article)
    # Checked if result object exist
    if result is None:
        result = "Not found"
    # Created custom keyboard with custom buttons
    markup = types.ReplyKeyboardMarkup()
    # Created custom variables for keyboard
    main_menu_btn = types.KeyboardButton("Main menu")
    # Added button to keyboard
    markup.row(main_menu_btn)
    # Send message to user
    bot.send_message(message.chat.id, f"{result}.", reply_markup=markup)


#
@user_check
def add_to_bookmarks(message: Message) -> None:
    """
    Function to handle add bookmarks
    Add user and bookmark if not in database, then redirect to specified item.

    Parameters:
        message (Message): Incoming message.

    Returns:
        None
    """
    # Get user info
    user_id = message.from_user.id
    username = message.from_user.username
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name
    # Get article infor
    article = session.get_data(user_id=user_id, key="article")
    # Check if user in database
    if not User.get_user_by_id(user_id):
        # Add user if not in database
        User.add_user(user_id=user_id, username=username, first_name=first_name, last_name=last_name)
    # Check if bookmark in database
    if not Bookmark.get_bookmark(user_id=user_id, symbol=article):
        # Add bookmark if not in database
        Bookmark.add_to_bookmark(user_id=user_id, symbol=article)
    # redirect to item
    item(message)


@user_check
def remove_bookmark(message: Message) -> None:
    """
    Handle remove bookmark.
    Remove bookmark if in database, then redirect to item.

    Parameters:
        message (Message): The incoming message

    Returns:
        None
    """
    user_id = message.from_user.id

    article = session.get_data(user_id=user_id, key="article")

    # Check if bookmark in database
    if Bookmark.get_bookmark(user_id=user_id, symbol=article):
        # Remove bookmark if in database
        Bookmark.remove_bookmark(user_id=user_id, symbol=article)
    # Redirect to item
    item(message)


@user_check
def bookmarks(message: Message) -> None:
    """
    Function to handle bookmarks.
    Get current information fo each symbol founded from bookmarks table in database.
    Redirect to main menu.

    Parameters:
        message (Message): The incoming message
    Returns:
        None
    """
    # Get specified user id
    user_id = message.from_user.id
    # Get all bookmarks from specified user
    all_bookmarks = Bookmark().get_all_bookmarks(user_id)
    # Loop through all bookmarks
    for bookmarks_item in all_bookmarks:
        # Search company result by symbol
        company = stock.bookmark(bookmarks_item[1])

        # check if company exists
        if company:
            # If new message send to user increase current message id in session
            session.increase_current_message_id(user_id=user_id)
            # Created custom keyboard with custom buttons
            item_markup = types.InlineKeyboardMarkup()
            # Created custom button
            open_profile = types.InlineKeyboardButton(f"Open company profile",
                                                      callback_data=f"item|{company.get('symbol')}")
            # Added custom button to keyboard
            item_markup.row(open_profile)
            # Send message to user
            bot.send_message(message.chat.id, f"{company.get('company')}.", reply_markup=item_markup)

    # Created custom keyboard with custom button
    markup = types.ReplyKeyboardMarkup()
    # Created custom button
    main_menu_btn = types.KeyboardButton("Main menu")
    # Added button to keyboard
    markup.row(main_menu_btn)
    # Send message to bot
    bot.send_message(message.chat.id, f'All bookmarks loaded', reply_markup=markup)


@bot.message_handler(func=lambda message: True)
def message_handler(message: Message) -> None:
    """
    Function to handle buttons input and text input messages.

    Parameters:
        message (Message): The input message
    Returns:
        None
    """
    # Get specified user id
    user_id = message.from_user.id

    session.increase_current_message_id(user_id=user_id)

    # Check if message equal specified string
    if message.text == 'Search by "company symbol":':
        # Redirect to symbol_search
        symbol_search(message)
    # Check if message equal specified string
    elif message.text == 'Search by "company name":':
        # Redirect to company_search
        company_search(message)
    # Check if message equal specified string
    elif message.text == 'Bookmarks':
        # Redirect to bookmarks
        bookmarks(message)
    # Check if message equal specified string
    elif message.text == 'Main menu':
        # Redirect to main_menu
        main_menu(message)
    # Check if message equal specified string
    elif message.text == 'Add to bookmarks':
        # Redirect to add_to_bookmarks
        add_to_bookmarks(message)
    # Check if message equal specified string
    elif message.text == 'Remove from bookmarks':
        # Redirect to remove_bookmark
        remove_bookmark(message)
    # Check if message equal specified string
    elif message.text == 'Get price change':
        # Redirect message to price_change
        price_change(message)
    else:
        search_type = session.get_data(user_id=user_id, key="search_type")
        # Check if message equal specified string
        if search_type == "symbol":
            # Redirect to item
            item(message)
        # Check if message equal specified string
        elif search_type == "company":
            # Redirect to companies
            companies(message)
        else:
            # Redirect to main_menu
            main_menu(message)


@bot.callback_query_handler(func=lambda callback: callback.data)
def callback_query_handler(callback: CallbackQuery) -> None:
    """
    Function to handle callbacks

    Parameters:
        callback (CallbackQuery): The input instance
    Returns:
        None
    """
    # Get user_id from callback data
    user_id = callback.from_user.id
    # Increase current message id by one
    session.increase_current_message_id(user_id=user_id)

    # Separate callback to value and function name
    function_name, value = callback.data.split("|")
    # Check if function equal to "item"
    if function_name == "item":
        # session set data to search by specified user id
        session.set_data(user_id=user_id, key="article", data=value)
        # Assign callback.message.text to value from callback data
        callback.message.text = value
        # Redirect to item
        item(callback)
