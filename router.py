from aiogram import Router
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, \
    CallbackQuery
from aiogram.filters import Command

from utils import text_on_rus, text_on_eng, get_all_themes, get_subtopics_for_theme, translate_text
from gpt_config import get_answer

router = Router()

users = {}


async def change_language(user_id, language, callback_query=None):
    if user_id in users:
        if users[user_id]["language"] != language:
            users[user_id]["language"] = language
            if callback_query:
                await callback_query.message.edit_text(f"Language changed to {language.capitalize()}!!!")
    else:
        users[user_id] = {
            "username": callback_query.from_user.username if callback_query else None,
            "language": language.lower()
        }
        if callback_query:
            text_func = text_on_rus if language == "rus" else text_on_eng
            await callback_query.message.edit_text(text_func(users[user_id]["username"]))


@router.message(Command("start"))
async def start_handler(msg: Message):
    if msg.from_user.id not in users:
        rus = InlineKeyboardButton(text="Rus", callback_data='Ru')
        eng = InlineKeyboardButton(text="Eng", callback_data='En')
        await msg.answer("Привет👋🏻\nChoose a language / Выберите язык:",
                         reply_markup=InlineKeyboardMarkup(inline_keyboard=[[rus, eng]]))
    else:
        if users[msg.from_user.id]["language"] == "eng":
            await msg.answer("If you have any issues, you can see available commands through the /help command.")
        else:
            await msg.answer(
                "Если у вас возникли какие-либо проблемы, вы можете просмотреть доступные команды с помощью команды /help.")


@router.callback_query(lambda c: c.data == 'Ru')
async def process_callback_kz(callback_query: CallbackQuery):
    await change_language(callback_query.from_user.id, "rus", callback_query)


@router.callback_query(lambda c: c.data == 'En')
async def process_callback_en(callback_query: CallbackQuery):
    await change_language(callback_query.from_user.id, "eng", callback_query)


@router.message(Command("help"))
async def help_handler(message: Message):
    language = users.get(message.from_user.id, {}).get("language", "eng")

    if language == "eng":
        help_text = """
        Welcome to the Help Center! Here are some available commands:
/start - Start using the bot
/language - Change your language preference
/themes - Choose a theme
/present - Get a presentation based on your username
/advice - Receive presenatiton
/random - Receive a random piece of advice
/help - Display this help message
        """
    else:
        help_text = """
        Добро пожаловать в Центр помощи! Вот некоторые доступные команды:
/start - Начать использование бота
/language - Изменить предпочтения языка
/themes - Выбрать тему
/present - Получить представление
/advice - Получить персональный совет
/random -  Получить случайный совет
/help - Показать это сообщение справки
        """

    await message.answer(help_text)


@router.message(Command("present"))
async def present_handler(msg: Message):
    language = users.get(msg.from_user.id, {}).get("language", "Eng")
    print(language)
    if language == "rus":
        await msg.answer(text_on_rus(msg.from_user.username))
    else:
        await msg.answer(text_on_eng(msg.from_user.username))


@router.message(Command("language"))
async def language_handler(msg: Message):
    rus = InlineKeyboardButton(text="Rus", callback_data='Ru')
    eng = InlineKeyboardButton(text="Eng", callback_data='En')
    await msg.answer("Choose a language / Выберите язык:",
                     reply_markup=InlineKeyboardMarkup(inline_keyboard=[[rus, eng]]))


@router.message(Command("themes"))
async def theme_handler(message: Message):
    themes = get_all_themes()
    response_text = "Choose a topic:"
    try:
        if users[message.from_user.id]["language"] == "eng":
            keyboard = InlineKeyboardMarkup(row_width=1,
                                            inline_keyboard=[
                                                [InlineKeyboardButton(text=theme, callback_data=f"theme_{theme}")]
                                                for theme in themes])
        else:
            keyboard = InlineKeyboardMarkup(row_width=1,
                                            inline_keyboard=[
                                                [InlineKeyboardButton(text=translate_text(theme),
                                                                      callback_data=f"theme_{theme}")]
                                                for theme in themes])
            response_text = translate_text(response_text)

        await message.answer(response_text, reply_markup=keyboard)
    except Exception as e:
        print(e.__class__.__name__)


@router.callback_query(lambda c: c.data.startswith('theme_'))
async def handle_theme_callback(callback_query: CallbackQuery):
    theme = callback_query.data.replace('theme_', '')
    subtopics = get_subtopics_for_theme(theme)
    response_text = f"Subtopics for {theme}:"

    if users[callback_query.from_user.id]["language"] == "eng":
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[[InlineKeyboardButton(text=subtopic, callback_data=f"subtopic_{subtopic}")] for subtopic in
                             subtopics])
    else:
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[[InlineKeyboardButton(text=translate_text(subtopic), callback_data=f"subtopic_{subtopic}")]
                             for subtopic in subtopics])
        response_text = translate_text(response_text)
    await callback_query.message.edit_text(response_text, reply_markup=keyboard)


@router.callback_query(lambda c: c.data.startswith('subtopic_'))
async def handle_subtopic_callback(callback_query: CallbackQuery):
    subtopic = callback_query.data.replace('subtopic_', '')
    user_id = callback_query.from_user.id
    if user_id in users:
        user_data = users[user_id]
        language_value = user_data.get('language', "eng")
        if language_value == "eng":
            await callback_query.message.edit_text(subtopic)
        else:
            await callback_query.message.edit_text(translate_text(subtopic))
        response_text = get_answer(text=subtopic, lng=language_value)
        await callback_query.message.answer(response_text)
        return
    else:
        await callback_query.message.answer(get_answer(subtopic))


@router.message(Command("advice"))
async def advice_handler(message: Message):
    try:
        if message.text == "/advice":
            await message.answer("Type form are `/advice Your psychology question`")
        else:
            user_id = message.from_user.id
            if user_id in users:
                user_data = users[user_id]
                language_value = user_data.get('language', "eng")
                await message.answer(text="Wait a sec⏳" if language_value == "eng" else "Подождите немного⏳")
                advice_text = get_answer(message.text)
                if language_value == "rus":
                    advice_text = get_answer(message.text, language_value)
                await message.delete()
                await message.answer(advice_text)
    except Exception as e:
        print(e.__class__.__name__)


@router.message(Command("random"))
async def random_advice_handler(message: Message):
    try:
        language = users.get(message.from_user.id, {}).get("language", "eng")

        response_text = get_answer("Make me random advice to psychology")
        if language == "rus":
            response_text = translate_text(response_text)

        await message.answer(response_text)
    except Exception as e:
        print(e.__class__.__name__)


@router.message()
async def bot(message: Message):
    text = message.text.lower()
    if text == "hello" or text == "hi":
        await message.answer("Hello what i help for you?")
    elif text == "привет":
        await message.answer("Привет чем я могу вам помочь?")
    else:
        await message.answer("Please check list of commands: /help")
