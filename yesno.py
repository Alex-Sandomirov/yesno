import os

import requests

from telegram import ReplyKeyboardMarkup
from telegram.ext import CommandHandler, Filters, MessageHandler, Updater

from dotenv import load_dotenv

load_dotenv()

token = os.getenv('TOKEN')
updater = Updater(token=token)
URL = 'https://yesno.wtf/api'

def get_new_answer():
    response = requests.get(URL).json()
    random_answer = response.get('image')
    return random_answer

def new_answer(update, context):
    chat = update.effective_chat
    context.bot.send_animation(chat.id, get_new_answer())

def faq(update, context):
    chat = update.effective_chat
    context.bot.send_message(
        chat_id=chat.id,
        text='Бот Данетка умеет отвечать на однозначные вопросы "да" или "нет". '
        'Для пущего веселья он отвечает гифками. Да, иногда будет сложно понять, '
        'что именно ответил бот, но это всего лишь повод спросить еще раз или '
        'интерпретировать ответ как удобно. Кроме того, с очень небольшой долей '
        'вероятности бот может ответь "возможно", он такой, да. '
        'Помните, что неправильно сформулированный вопрос не только '
        'поднимает уровень энтропии во Вселенной, но и не дает верного ответа.',
        )

def wake_up(update, context):
    chat = update.effective_chat
    name = update.message.chat.first_name
    button = ReplyKeyboardMarkup([['Вселенная, помоги!', 'О боте']], resize_keyboard=True)
    context.bot.send_message(
        chat_id=chat.id,
        text='{}, Привет! Я бот который умеет давать однозначный ответ на вопрос "да" или "нет".' 
        ' Например, вы можете спросить "пойти мне сегодня на работу?" или "может съесть еще один кусочек пиццы?"'
        ' и получить однозначный ответ. Просто сформулируйте свой вопрос и смело жмите на кнопку '
        '"Вселенная, помоги!".  '.format(name),
        reply_markup=button
        )

updater.dispatcher.add_handler(CommandHandler('start', wake_up))
updater.dispatcher.add_handler(MessageHandler(Filters.text('Вселенная, помоги!'), new_answer))
updater.dispatcher.add_handler(MessageHandler(Filters.text('О боте'), faq))

updater.start_polling() 
updater.idle()