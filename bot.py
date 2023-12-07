import asyncio
import logging
from time import sleep
import os
from aiogram import Bot, Dispatcher, executor
from aiogram.dispatcher import DEFAULT_RATE_LIMIT
from aiogram.dispatcher.handler import CancelHandler, current_handler
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from aiogram.utils.exceptions import Throttled
from aiogram import types
from config import *
from random import *
import db1
from aiogram.types.message import ContentTypes
from aiogram.types import ContentType, Message
from aiogram.types import InputFile
from aiogram.dispatcher.filters import Command
storage = MemoryStorage()
bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
logging.basicConfig(level=logging.INFO)

class Mydialog(StatesGroup):
    otvet = State()
class Mydialog1(StatesGroup):
    otvet1 = State()
class Mydialog2(StatesGroup):
    otvet2 = State()
class Mydialog3(StatesGroup):
    otvet3 = State()
class Mydialog4(StatesGroup):
    set_card = State()
class Mydialog5(StatesGroup):
    fio = State()
class Mydialog6(StatesGroup):
    message = State()
    



@dp.message_handler(commands="start")
async def start(message: types.Message):
    confirm_status = db1.get_confirm_status(message.chat.id)

    if confirm_status is None:
        db1.add_user(message.chat.id)
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(types.InlineKeyboardButton(text="Подать заявку", callback_data="zaya"))
        await message.answer("💎Приветствуем в UA.SCUM Syndicate!💎\n\n🦣Наше сообщество занимается эффективной работой по русским мамонтам. Членам нашей команды мы гарантируем доступ к лучшим мануалам, ботам, огромным пакам материалов и постоянной тех. поддержке.\n\n⏳Подайте свою заявку на вступление в наше сообщество и ожидайте её рассмотрения, вы на верном пути\n\n❕На все вопросы ждём честных и развернутых ответов", reply_markup=keyboard)
    else:
        if confirm_status == 1:
            await message.answer('Вы уже в команде! Пропишите /menu для доступа к меню.')
        elif confirm_status == 0:
            await message.answer('Вы уже подали заявку🚷\n\nОжидайте рассмотрения заявки от администрации.\n\nЗаявки принимаются, в основном, с 10:00 до 23:00. В случае игнорирования вашей заявки более 24 часов, напишите @CEO_uascm❕!')


@dp.callback_query_handler(text="zaya")
async def send_start(call: types.CallbackQuery):
    await call.message.edit_text('1️⃣ Знакомы ли вы с направлением скама, есть ли у вас опыт работы? Если да, просьба прикрепите скриншоты профитов и напишите название команд❕')
    await Mydialog.otvet.set()
    
@dp.message_handler(state=Mydialog.otvet)
async def process_message(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['text'] = message.text
        user_message = data['text']
        db1.add_text1(user_message, message.chat.id, None)
        await state.finish()

    await message.reply('2️⃣ Откуда узнали о нашем проекте? Укажите тег человека или платформу, откуда узнали❕')
    await Mydialog1.otvet1.set()
@dp.message_handler(content_types=ContentTypes.PHOTO,state=Mydialog.otvet)
async def message_photo_2(message : types.Message, state: FSMContext):
    db1.add_text1(message['caption'], message.chat.id, message.photo[0]['file_id'])
    await state.finish()
    await Mydialog1.otvet1.set()
    await message.reply('2️⃣ Откуда узнали о нашем проекте? Укажите тег человека или платформу, откуда узнали❕')
    
@dp.message_handler(state=Mydialog1.otvet1)
async def process_message(message: types.Message, state: FSMContext):
    async with state.proxy() as data1:
        print(message)
        db1.add_text2(db1.get_text1(message.chat.id), message.text, message.chat.id, db1.get_photo(message.chat.id))
        await state.finish()
        await Mydialog2.otvet2.set()
        await message.reply(f'3️⃣ Сколько готовы приделять времени работе в нашей команде?❕')
        

@dp.message_handler(state=Mydialog2.otvet2)
async def process_message(message: types.Message, state: FSMContext):
    message.chat.id = int(message.chat.id)
    async with state.proxy() as data2:
        data2['text'] = message.text
        user_message2 = data2['text']
        db1.add_text3(db1.get_text1(message.chat.id), db1.get_text2(message.chat.id), user_message2, message.chat.id, db1.get_photo(message.chat.id))
        await message.reply('4️⃣ Расскажите какие цели вы приследуете при выборе данного вида работы?❕')
        await state.finish()
        await Mydialog3.otvet3.set()

@dp.message_handler(state=Mydialog3.otvet3)
async def process_message(message: types.Message, state: FSMContext):
    user_id = int(message.from_user.id)
    db1.add_text4(db1.get_text1(message.chat.id), db1.get_text2(message.chat.id), db1.get_text3(message.chat.id),message.text, message.chat.id, db1.get_photo(message.chat.id))
    await message.reply('📤 Ваша заявка отправлена!\n\n❗️Принимаем в течении суток')
    await state.finish()
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    but1 = types.InlineKeyboardButton(text="Принять", callback_data=f"prin_{message.from_user.id}")
    but2 = types.InlineKeyboardButton(text="Отклонить", callback_data=f"otkl_{message.from_user.id}")

    keyboard.add(but1, but2)
  
    if db1.get_photo(message.chat.id) == None:
        await bot.send_message(chat_id=admin_user_id, text=f'<a href="tg://user?id={message.chat.id}">{message.from_user.first_name}</a> Отправил заявку! Его данные:\n1️⃣ Если ли у вас опыт работы?❕\n {db1.get_text1(message.chat.id)}\n\n2️⃣ Откуда узнали о нашей команде?❕\n {db1.get_text2(message.chat.id)}\n\n3️⃣ Сколько готовы уделять времени в неделю/день нашему проекту?\n - {db1.get_text3(message.chat.id)}\n\n4️⃣ Настрой?❕\n {message.text}',parse_mode='HTML', reply_markup=keyboard)
    else:
        await bot.send_photo(chat_id=admin_user_id, photo=db1.get_photo(message.chat.id), caption=f'<a href="tg://user?id={message.chat.id}">{message.from_user.first_name}</a> Отправил заявку! Его данные:\n1️⃣ Если ли у вас опыт работы?❕\n {db1.get_text1(message.chat.id)}\n\n2️⃣ Откуда узнали о нашей команде?❕\n {db1.get_text2(message.chat.id)}\n\n3️⃣ Сколько готовы уделять времени в неделю/день нашему проекту?\n - {db1.get_text3(message.chat.id)}\n\n4️⃣ Настрой?❕\n {message.text}',parse_mode='HTML', reply_markup=keyboard)




    @dp.callback_query_handler(text_startswith=f"prin_{message.from_user.id}")
    async def send_prin(call: types.CallbackQuery):

        db1.add_confirm(message.chat.id, db1.get_text2(message.chat.id), db1.get_text3(message.chat.id), message.text,
                        message.chat.id, 1, db1.get_photo(message.chat.id))
        # Создаем инлайн-клавиатуру
        keyboard = InlineKeyboardMarkup(row_width=2)  # 2 кнопки в ряду

        cont_key = InlineKeyboardButton (text="✅Перейти к уроку", callback_data="cont_key")

        keyboard.add(cont_key)

        await bot.send_message(
         chat_id=user_id,
          text="🎉 Поздравляем! Вы приняты в команду UA.SCUM Syndicate. Перед началом работы пройдите короткий видеоурок, для понимания азов работы!",
          reply_markup=keyboard
         )

        await call.message.delete()


    @dp.callback_query_handler(text_startswith=f"otkl_{message.from_user.id}")
    async def send_otkl(call: types.CallbackQuery):
        user_id = int(call.data.split("_")[1])
        db1.add_confirm(message.chat.id, db1.get_text2(message.chat.id), db1.get_text3(message.chat.id),message.text, message.chat.id, 2, db1.get_photo(message.chat.id))
        await bot.send_message(chat_id=user_id, text="Ваша заявка отклонена❌\n\nВидимо ваши критерии не подходят нашей команде. Можете оспорить решение администрации в личных сообщениях @USS_HOST.🤔")
        await call.message.delete()
    

@dp.callback_query_handler(text_startswith="cont_key") #видео 1
async def continue_to_lesson(call: types.CallbackQuery):
    # Получаем идентификатор чата пользователя
    user_id = call.from_user.id
    
    # Шаг 1: Удаление сообщения о принятии заявки
    await call.message.delete()

    # Шаг 2: Отправка пользователю кругового видеосообщения
    video_note_path = "vid1.mp4"  # Замените на реальный путь к видеосообщению
    with open(video_note_path, "rb") as video_note:
        await bot.send_video_note(chat_id=user_id, video_note=video_note)

        # Шаг 3: Ожидание 15 секунд
        await asyncio.sleep(15)

        # Шаг 4: Отправка текстового сообщения с inline кнопкой
        keyboard = InlineKeyboardMarkup(row_width=1)
        button_text = InlineKeyboardButton(text="Дальше", callback_data="1cont_key")
        keyboard.add(button_text)

        await bot.send_message(
            chat_id=user_id,
            text="После просмотра нажми на кнопку чтобы продолжить!",
            reply_markup=keyboard
        )

@dp.callback_query_handler(text_startswith="1cont_key") #видео 2
async def continue_to_lesson_1(call: types.CallbackQuery):
    await call.message.delete()
    video_note_path = "vid2.mp4"
    with open(video_note_path, "rb") as video_note:
        await bot.send_video_note(chat_id=call.from_user.id, video_note=video_note)
        await asyncio.sleep(15)
        keyboard = InlineKeyboardMarkup(row_width=1)
        button_text = InlineKeyboardButton(text="Дальше 👉", callback_data="2cont_key")
        keyboard.add(button_text)
        await bot.send_message(
            chat_id=call.from_user.id,
            text="ㅤ",
            reply_markup=keyboard
        )

@dp.callback_query_handler(text_startswith="2cont_key") #видео 3
async def continue_to_lesson_2(call: types.CallbackQuery):
    await call.message.delete()
    video_note_path = "vid3.mp4"
    with open(video_note_path, "rb") as video_note:
        await bot.send_video_note(chat_id=call.from_user.id, video_note=video_note)
        await asyncio.sleep(15)
        keyboard = InlineKeyboardMarkup(row_width=1)
        button_text = InlineKeyboardButton(text="Дальше 👉", callback_data="3cont_key")
        keyboard.add(button_text)
        await bot.send_message(
            chat_id=call.from_user.id,
            text="ㅤ",
            reply_markup=keyboard
        )

@dp.callback_query_handler(text_startswith="3cont_key") #видео 4
async def continue_to_lesson_3(call: types.CallbackQuery):
    await call.message.delete()
    video_note_path = "vid4.mp4"
    with open(video_note_path, "rb") as video_note:
        await bot.send_video_note(chat_id=call.from_user.id, video_note=video_note)
        await asyncio.sleep(15)
        keyboard = InlineKeyboardMarkup(row_width=1)
        button_text = InlineKeyboardButton(text="Дальше 👉", callback_data="4cont_key")
        keyboard.add(button_text)
        await bot.send_message(
            chat_id=call.from_user.id,
            text="ㅤ",
            reply_markup=keyboard
        )

@dp.callback_query_handler(text_startswith="4cont_key")  #видео 5
async def continue_to_lesson_4(call: types.CallbackQuery):
    await call.message.delete()
    video_note_path = "vid5.mp4"
    with open(video_note_path, "rb") as video_note:
        await bot.send_video_note(chat_id=call.from_user.id, video_note=video_note)
        await asyncio.sleep(15)
        keyboard = InlineKeyboardMarkup(row_width=1)
        button_text = InlineKeyboardButton(text="✅ Открыть WORK меню", callback_data="work_menu")
        keyboard.add(button_text)
        await bot.send_message(
            chat_id=call.from_user.id,
            text="Обучение пройдено, можешь приступать к работе!",
            reply_markup=keyboard
        )



def create_work_menu_keyboard(): #Сооздание клавиатуры ВОРК МЕНЮ
    keyboard = InlineKeyboardMarkup(row_width=2)
    button_manuals = InlineKeyboardButton(text="📚Мануалы", url="https://t.me/+4YDLWB0QqXc2MWYy")
    button_chat = InlineKeyboardButton(text="💬Чат", url="https://t.me/+rsSUyQd1rCA5ODhi")
    button_bots = InlineKeyboardButton(text="🛠Инструменты", callback_data="tools")
    button_work_bots = InlineKeyboardButton(text="🤖Боты", callback_data="bots")
    button_cards = InlineKeyboardButton(text="💳Карты/Вывод", callback_data="cards")
    button_curator = InlineKeyboardButton(text="🗣️Куратор", callback_data="curator")
    button_profile = InlineKeyboardButton(text="Мой профиль", callback_data="profile")

    keyboard.add(button_manuals, button_chat,button_work_bots, button_bots, button_cards, button_curator, button_profile)
    return keyboard

@dp.message_handler(commands="menu") #Обработчик команды "/menu"
async def open_work_menu(call: types.CallbackQuery):
    confirm_status = db1.get_confirm_status(call.from_user.id)

    if confirm_status == 1:
        
        keyboard_work = create_work_menu_keyboard()
        
        # Путь к изображению "Меню воркера" (замените на реальный путь)
        image_path = "banner_menu.jpg"

        # Отправка изображения с подписью и кнопками
        with open(image_path, "rb") as image_file:
            await bot.send_photo(
                chat_id=call.from_user.id,
                photo=image_file,
                caption="Меню воркера 🔽",
                reply_markup=keyboard_work
            )
    elif confirm_status == 0:
        # Если статус равен 0, отправляем сообщение о необходимости подтверждения
        await bot.send_message(
            chat_id=call.from_user.id,
            text="Вам нужно быть членом команды, чтобы открыть меню. Ожидайте подтверждения."
        )



@dp.callback_query_handler(text_startswith=["nazad", "work_menu"]) #Обработчик кнопки "Назад" (Замена на Меню)
async def open_work_menu(call: types.CallbackQuery):
  
        await call.message.delete()

        keyboard_work = create_work_menu_keyboard()

        # Путь к изображению "Меню воркера" (замените на реальный путь)
        image_path = "banner_menu.jpg"

        # Отправка изображения с подписью и кнопками
        with open(image_path, "rb") as image_file:
            await bot.send_photo(
                chat_id=call.from_user.id,
                photo=image_file,
                caption="Меню воркера 🔽",
                reply_markup=keyboard_work
            )

@dp.callback_query_handler(text_startswith= "delete_msg")  #Обработчик кнопки "Удалить"
async def delete_broadcast_callback(callback_query: types.CallbackQuery):
    await bot.delete_message(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id)

#Обработчик админ-панели
@dp.message_handler(Command("adm"))
async def cmd_message(call: types.CallbackQuery):
    keyboard = InlineKeyboardMarkup(row_width=1)
    button_msg = InlineKeyboardButton(text="Рассылка", callback_data="adm_msg")
    button_card = InlineKeyboardButton(text="Сменить карту ", callback_data="adm_card")
    keyboard.add(button_msg,button_card)

    if call.from_user.id == admin_user_id:
        await bot.send_message(
            chat_id=call.from_user.id,
            text="Админ панель:",
            reply_markup=keyboard)
    else:await bot.send_message(
            chat_id=call.from_user.id,
            text="У вас нету доступа к этой команде",
            )
        


@dp.callback_query_handler(text_startswith="tools") #Обработчик кнопки "Инструменты"
async def help_bots_callback(call: types.CallbackQuery):

    # Изменяем текст кнопок
    keyboard = InlineKeyboardMarkup(row_width=1)
    button_bots = InlineKeyboardButton(text="⚙️ Боты-помощники ", callback_data="help_bots")
    button_mats = InlineKeyboardButton(text="📦 Другие материалы",callback_data="materials" )
    button_back = InlineKeyboardButton(text="Назад", callback_data="nazad")
    keyboard.add(button_bots,button_mats, button_back)

    await bot.edit_message_caption(chat_id=call.message.chat.id, message_id=call.message.message_id, caption="🛠 Инструмены которые помогут тебе в работе:", reply_markup=keyboard)

@dp.callback_query_handler(text_startswith="help_bots") #Обработчик кнопки "Боты-помощники"
async def help_bots_callback(call: types.CallbackQuery):
    
    keyboard = InlineKeyboardMarkup(row_width=1)
    button_vid = InlineKeyboardButton(text="🖼Видео в кружок", url="https://t.me/UASCUM_VideoBot")
    button_sms = InlineKeyboardButton(text="📥Прием СМС", url="https://t.me/UASCUM_SmsBot")
    button_draw = InlineKeyboardButton(text="🖌Отрисовка чеков", url="https://t.me/UASCUM_DrawBot")
    button_back = InlineKeyboardButton(text="Назад", callback_data="nazad")
    keyboard.add(button_vid, button_sms, button_draw, button_back)

    await bot.edit_message_caption(chat_id=call.message.chat.id, message_id=call.message.message_id, caption="🛠 Боты-хелперы для твоих задач:", reply_markup=keyboard)

@dp.callback_query_handler(text_startswith="materials") #Обработчик кнопки "Другие материалы"
async def help_bots_callback(call: types.CallbackQuery):
    
    keyboard = InlineKeyboardMarkup(row_width=1)
    button_vid = InlineKeyboardButton(text="🖼Пак девушек", url="https://t.me/+5rSuHdQo9KNjMzQy")
    button_sms = InlineKeyboardButton(text="📥Пак чатов", url="https://t.me/+Hc-adGmAFco0MmI6")
    button_draw = InlineKeyboardButton(text="🖥Софты", callback_data="softs_help")
    button_back = InlineKeyboardButton(text="Назад", callback_data="nazad")
    keyboard.add(button_vid, button_sms, button_draw, button_back)

    await bot.edit_message_caption(chat_id=call.message.chat.id, message_id=call.message.message_id, caption="🛠 Боты-хелперы для твоих задач:", reply_markup=keyboard)

@dp.callback_query_handler(text_startswith="bots") #Обработчик кнопки "Боты"
async def help_bots_callback(call: types.CallbackQuery):
    # Изменяем текст сообщения
    keyboard = InlineKeyboardMarkup(row_width=1)
    button_apteka = InlineKeyboardButton(text="💊Нарко бот РУ", url= "https://t.me/AptekaShop_robot")
    button_aptekaBY = InlineKeyboardButton(text="💊Нарко бот РБ", url= "https://t.me/AptekaShopBY_robot")
    button_logs = InlineKeyboardButton(text="🔑Скупка логов бот", url= "https://t.me/LoginKeysRobot")
    button_gun = InlineKeyboardButton(text="🏹Оружейка канал", url= "https://t.me/travmat_sd")
    button_back = InlineKeyboardButton(text="Назад", callback_data = "nazad")

    keyboard.add(button_apteka, button_aptekaBY, button_logs, button_gun, button_back)

    await bot.edit_message_caption(chat_id=call.message.chat.id, message_id=call.message.message_id, caption="🤖 Наши скам боты/проекты:", reply_markup=keyboard)
    
@dp.callback_query_handler(text_startswith="cards")   #Обработчик кнопки "Карты" 
async def cards_callback(call: types.CallbackQuery):
    
    # Получаем значения card и fio из базы данных
    card = db1.get_card()
    fio = db1.get_fio()

    # Изменяем текст сообщения с использованием значений из базы данных
    keyboard = InlineKeyboardMarkup(row_width=1)
    button_pay = InlineKeyboardButton(text="💸Запросить вылату", url="https://t.me/ua_sc_sy")
    button_back = InlineKeyboardButton(text="Назад", callback_data="nazad")
    keyboard.add(button_pay, button_back)

    # Формируем текст сообщения с использованием значений card и fio
    message_text = f"💳 Карты под прием прямых платежей:\n\nКарта: {card}\nФИО: {fio}\n\n▫️Для получения выплаты отправте чек или скриншот перевода по контактам ниже!"

    # Отправляем отредактированное сообщение
    await bot.edit_message_caption(chat_id=call.message.chat.id, message_id=call.message.message_id, caption=message_text, reply_markup=keyboard)

@dp.callback_query_handler(text_startswith="curator") #Обработчик кнопки "Куратор"
async def help_bots_callback(call: types.CallbackQuery):
    # Изменяем текст сообщения
    keyboard = InlineKeyboardMarkup(row_width=1)
    button_back = InlineKeyboardButton(text="Назад", callback_data = "nazad")
    keyboard.add(button_back)

    await bot.edit_message_caption(chat_id=call.message.chat.id, message_id=call.message.message_id, caption="🗣 Выбери куратора с которым хочешь начать работу:", reply_markup=keyboard)

@dp.callback_query_handler(text_startswith="profile") #Обработчик кнопки "Профиль"
async def help_bots_callback(call: types.CallbackQuery):
    # Изменяем текст сообщения
    keyboard = InlineKeyboardMarkup(row_width=1)
    button_back = InlineKeyboardButton(text="Назад", callback_data = "nazad")
    keyboard.add(button_back)

    await bot.edit_message_caption(chat_id=call.message.chat.id, message_id=call.message.message_id, caption="Ваш профиль", reply_markup=keyboard)



#Обработчик кнопки "Сменить карту"
@dp.callback_query_handler(text="adm_card")
async def callback_adm_card(call: types.CallbackQuery):
    # Проверяем, является ли пользователь админом
    if call.from_user.id == admin_user_id:
        await call.message.answer("Введите новый номер карты:")
        # Устанавливаем состояние MyDialog.set_card
        await Mydialog4.set_card.set()
    else:
        await call.message.answer("У вас нету доступа к этой команде")

@dp.message_handler(state=Mydialog4.set_card)
async def set_card(message: Message, state: FSMContext):
    # Получаем введенный номер карты
    card = message.text

    # Сохраняем номер карты в базе данных
    db1.add_card(user_id=1, card=card)

    # Спрашиваем у пользователя ФИО
    await message.answer("Введите ваше ФИО:")

    # Сохраняем номер карты в состояние, чтобы его можно было использовать в следующем обработчике
    await state.update_data(card=card)

    # Устанавливаем состояние MyDialog.fio
    await Mydialog5.fio.set()

@dp.message_handler(state=Mydialog5.fio)
async def set_fio(message: Message, state: FSMContext):
    # Получаем введенное ФИО
    fio = message.text

    # Получаем номер карты из состояния
    data = await state.get_data()
    card = data.get('card')

    # Сохраняем ФИО и номер карты в базе данных
    db1.add_fio(user_id=1, fio=fio, card=card)

    # Завершаем состояние
    await state.finish()

    # Отправляем сообщение об успешном сохранении данных
    await message.answer("Данные успешно сохранены.")



#Обработчик кнопки "Рассылка"
@dp.callback_query_handler(text="adm_msg")
async def callback_adm_msg(call: types.CallbackQuery):
    # Проверяем, является ли пользователь админом
    if call.from_user.id == admin_user_id:
        await call.message.answer("Введите текст для рассылки:")
        # Устанавливаем состояние MyDialog6.message
        await Mydialog6.message.set()
    else:
        await call.message.answer("У вас нету доступа к этой команде")

@dp.message_handler(state=Mydialog6.message)
async def process_message(message: Message, state: FSMContext):

    keyboard = types.InlineKeyboardMarkup()
    button_delete = types.InlineKeyboardButton("♨️Убрать", callback_data="delete_msg")
    keyboard.add(button_delete)

    text_for_broadcast = message.text
    users = db1.get_all_users()

    for user_id in users:
        await bot.send_message(user_id, text_for_broadcast, reply_markup=keyboard)

    await state.finish()
    await message.answer("Рассылка успешно выполнена.")


     
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
