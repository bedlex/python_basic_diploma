# Stock_telebot

## OVERVIEW
The Stock Telebot is a Telegram bot that provides real-time information about specified stocks or a list of 
bookmarked stocks for quick reference.

## Main Features 
- **Search by Symbol:** Look up stock information using the company symbol.
- **Search by Company Name:** Find stock details by searching with the company name.
- **Bookmarks:** View all bookmarked stocks for quick reference.
- **Company Profile:** Get price change, remove or add company to bookmarks, and view all bookmarked stocks.
- **History:** Get previous history for searched items

#### Search by symbol
- ** Open the company profile by providing the company symbol. 

#### Search by company name
- ** - Get a list of stocks by searching with the company name.
- ** - Open the profile for each company.

#### Bookmarks
- ** - Get a list of stocks with current information for companies in bookmarks.
- ** - Open the profile for each company.

#### Company profile
- **Get price change:** Provided information about price change for the company, live.
- **Remove from bookmarks / add to bookmarks:** Option to remove or add company to bookmarks.
- **Bookmarks:** View all bookmarked stocks for quick reference.
- **Main menu:** Return to main menu.

#### History
/history 
- ** Get previous history for searched items.

#### Low
/low SYMBOL
- ** Displays the lowest stock price for a given symbol on the current day.

#### High
/high SYMBOL
- ** Displays the highest stock price for a given symbol on the current day.

#### Custom
/custom SYMBOL FROM_DATE TO_DATE
- ** Retrieves the specific stock history for a given

#### Help
/help 
- ** Displays a list of available commands and their descriptions for using the Stock Telebot effectively.


## Prerequisites
Before using the Stock_telebot, ensure you have a Telegram account and account in https://site.financialmodelingprep.com/ then
follow these setup steps:
- 1# Create a new bot on Telegram using the [BotFather](https://core.telegram.org/bots#botfather).
- 2# Create a new account on https://site.financialmodelingprep.com/
- 3# Clone the StockBot repository and install dependencies:


rename.env.template to .env
Edit next lines 

- BOT_API_KEY="provide your bot key"
- STOCK_KEY_API="provide your stock key"
- STOCK_API_URL="https://financialmodelingprep.com/api/v3/"
- DATABASE_URL="sqlite:///your database file"

```Bash
pip install -r requirements.txt
```