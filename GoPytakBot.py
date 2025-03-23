import logging
import os
from aiogram import Bot, Dispatcher, types, F
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from openai import OpenAI
import asyncio
from django.conf import settings

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'GoPytak.settings')
django.setup()


# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=settings.BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

# OpenAI client setup
client = OpenAI(api_key=settings.OPENAI_API_KEY)


# States
class BotStates(StatesGroup):
    main_menu = State()
    ai_consultation = State()


# Chat history storage {user_id: [messages]}
chat_histories = {}


# Start command
@dp.message(Command(commands=['start']))
async def send_welcome(message: types.Message, state: FSMContext):
    await state.clear()
    markup = types.ReplyKeyboardMarkup(keyboard=[
        [types.KeyboardButton(text="🚜 Наши услуги:")],
        [types.KeyboardButton(text="🏗 Доступная техника:")],
        [types.KeyboardButton(text="❓ Частые вопросы:")],
        [types.KeyboardButton(text="🤖 Консультация с ИИ:")]
    ], resize_keyboard=True)

    await message.answer(
"""
👷‍♂️ Привет! Я — бот компании “GoPytak”
Помогу подобрать технику и расскажу об услугах. Что интересует?👇:
""" ,
        reply_markup=markup
    )
    await state.set_state(BotStates.main_menu)


# Handler for "Our Services" button
@dp.message(F.text == "🚜 Наши услуги:", BotStates.main_menu)
async def our_services(message: types.Message):
    services_text = """
Выбирайте, чем можем помочь 👇:

🔩 Монтаж металлоконструкций — профессионально и точно, в срок!
🛣 Укладка асфальта на дорогах и мостах — гладко, ровно, надежно!
⛏ Земляные работы — копаем быстро и аккуратно, любой объем!
🏗 Разработка котлованов — для фундамента, коммуникаций и строительства!

Нажмите /start чтобы вернуться в главное меню.
    """
    await message.answer(services_text)


@dp.message(F.text == "🏗 Доступная техника:", BotStates.main_menu)
async def our_services(message: types.Message):
    services_text = """
Вся техника — в отличном состоянии и готова к работе! ✅

👷‍♀️ Строительная техника:
    - 🚜 Экскаваторы — любые объемы земляных работ!

🛤 Дорожная техника:
    - 🚧 Асфальтоукладчики — ровное покрытие дорог и тротуаров!

🏗 Грузоподъемная техника:
    - 🚀 Подъемники — для монтажа, высотных работ и нестандартных задач!

Нажмите /start чтобы вернуться в главное меню.
    """
    await message.answer(services_text)


# Handler for "QA" button
@dp.message(F.text == "❓ Частые вопросы:", BotStates.main_menu)
async def qa_handler(message: types.Message):
    qa_text = """
❓ Частые вопросы:

💬 Сколько стоит аренда?
Стоимость зависит от типа техники и сроков аренды. Рассчитаю за 1 минуту — просто напишите мне!

💬 Как быстро можно получить технику?
🚚 Оперативно доставим технику на объект — от 2 часов после заказа!

💬 Работаете с физлицами и юрлицами?
✅ Да, оформляем договоры на любые виды работ.

💬 Есть ли оператор или можно арендовать технику без водителя?
🛠 Предоставляем технику с опытным оператором или “без” — как вам удобнее!

Нажмите /start чтобы вернуться в главное меню.
    """
    await message.answer(qa_text)


# Handler for "Consult with AI" button
@dp.message(F.text == "🤖 Консультация с ИИ:", BotStates.main_menu)
async def start_ai_consultation(message: types.Message, state: FSMContext):
    user_id = message.from_user.id

    # Initialize chat history for this user if it doesn't exist
    if user_id not in chat_histories:
        chat_histories[user_id] = [
            {"role": "system", "content": "You are a helpful assistant."}
        ]

    markup = types.ReplyKeyboardMarkup(keyboard=[
        [types.KeyboardButton(text="Главное меню")]
    ], resize_keyboard=True)

    await message.answer(
        '''
Не знаете, что выбрать? Напишите мне задачу — подскажу оптимальное решение и сориентирую по стоимости! 💸. 
Напишите "Главное меню" чтобы вернуться в меню:
        ''',
        reply_markup=markup
    )
    await state.set_state(BotStates.ai_consultation)


# Handler for messages in AI consultation mode
@dp.message(BotStates.ai_consultation)
async def process_ai_message(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    user_message = message.text

    # Check if user wants to go back to main menu
    if user_message == "Главное меню":
        await send_welcome(message, state)
        return

    # Add user message to chat history
    chat_histories[user_id].append({"role": "user", "content": user_message})

    try:
        # Call OpenAI API
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=chat_histories[user_id],
            max_tokens=500,
            temperature=0.7,
        )

        # Extract response
        ai_response = response.choices[0].message.content

        # Add AI response to chat history
        chat_histories[user_id].append({"role": "assistant", "content": ai_response})

        # Send response to user
        await message.answer(ai_response)

    except Exception as e:
        logging.error(f"Error calling OpenAI API: {e}")
        await message.answer("Извините, произошла ошибка. Попробуйте позже")


# Back to main menu handler
@dp.message(F.text == "Главное меню")
async def back_to_menu(message: types.Message, state: FSMContext):
    await send_welcome(message, state)


# Default handler
@dp.message()
async def default_handler(message: types.Message, state: FSMContext):
    await send_welcome(message, state)

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())