""" Module to initialise Telebot, Stock, Database"""
import telebot

from app.config import Setting
from app.stock_market.stock import Stock

from sqlalchemy import create_engine, MetaData
# initialise setting
setting = Setting()
# initialise telebot as bot
bot = telebot.TeleBot(setting.BOT_API_KEY)
# initialise Stock as stock
stock = Stock(setting)
# initialise database engine
engine = create_engine(setting.DATABASE_URL, echo=False)
# initialise database metadata object
metadata = MetaData()


