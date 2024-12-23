import telebot
from telebot import types
import os
from dotenv import load_dotenv
from typing import List, Tuple

load_dotenv()
TOKEN = os.getenv('tb')
if not TOKEN:
    raise ValueError("Токен Telegram Bot не найден в файле .env")
bot = telebot.TeleBot(TOKEN)

photos: List[Tuple[str, str]] = [
    ('./imagine/1r.jpeg', 'Стильное панно влюбленные!\nШирина: 85 см\nВысота: 50 см\nОснова: хдф\nСтабилизированный мох:\nДекор под заказ\nМнoго издeлий в наличии\nВыбор цвета мха из палитры 35+оттенков\nНе требует полива\nОтличный подapок\nВ случае если у вас очень ограничен бюджет на озеленение, напишите мне, я вам предложу вам способ с минимальными затратами и максимальным визуальным эффектом\n4150₽\nДля заказа пишите @mossnasty\nВ сообщении укажите: фото желаемого пано, Ваше ФИО, адрес доставки полностью'),
    ('./imagine/2r.jpeg', 'Стильное панно дерево!\nШирина: 137 см\nВысота: 81 см\nОснова: фанера\n7500₽'),
    ('./imagine/3r.jpeg', '1890 ₽'),
    ('./imagine/4r.jpeg', '2450 ₽'),
    ('./imagine/5r.jpeg', 'Длина: 50 см\nВысота: 50 см\nОснова: дерево\n3700 ₽')
]

current_photo_index: int = 0


@bot.message_handler(commands=['start'])
def main(message: types.Message) -> None:
    """Обрабатывает команду /start и выводит главное меню."""
    with open('./imagine/kk.jpeg', 'rb') as file:
        bot.send_photo(message.chat.id, file)

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = [
        types.KeyboardButton("Наличие"),
        types.KeyboardButton("Под заказ"),
        types.KeyboardButton("Уход"),
        types.KeyboardButton("Подписаться на канал")
    ]
    keyboard.add(*buttons)

    bot.send_message(
        message.chat.id,
        (
            'Доброго времени суток!\n'
            'Этот бот поможет Вам с выбором эко-подарка и поможет узнать что-то новое, оставайтесь с нами!'
        ),
        reply_markup=keyboard
    )


@bot.message_handler(func=lambda message: message.text == "Наличие")
def show_photos(message: types.Message) -> None:
    """Отображает первое фото с описанием."""
    global current_photo_index
    current_photo_index = 0
    send_photo_with_caption(message.chat.id, current_photo_index)


def send_photo_with_caption(chat_id: int, index: int) -> None:
    """Отправляет фото с подписью в указанный чат."""
    if index < 0 or index >= len(photos):
        bot.send_message(chat_id, "Ошибка: индекс фотографии выходит за пределы списка.")
        return

    photo_path, caption = photos[index]

    try:
        with open(photo_path, 'rb') as photo_file:
            bot.send_photo(chat_id, photo_file, caption=caption)
    except FileNotFoundError:
        bot.send_message(chat_id, f"Ошибка: файл {photo_path} не найден.")
    except telebot.apihelper.ApiException as api_error:
        bot.send_message(chat_id, f"Ошибка API Telegram: {api_error}")

    # Клавиатура для перелистывания фото
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    if index < len(photos) - 1:
        keyboard.add(types.KeyboardButton("Вперед"))
    if index > 0:
        keyboard.add(types.KeyboardButton("Назад"))
    keyboard.add(types.KeyboardButton("Назад в меню"))

    bot.send_message(chat_id, "Выберите действие:", reply_markup=keyboard)


@bot.message_handler(func=lambda message: message.text in ["Вперед", "Назад"])
def change_photo(message: types.Message) -> None:
    """Изменяет текущее фото на следующее или предыдущее."""
    global current_photo_index

    if message.text == "Назад" and current_photo_index > 0:
        current_photo_index -= 1
    elif message.text == "Вперед" and current_photo_index < len(photos) - 1:
        current_photo_index += 1

    send_photo_with_caption(message.chat.id, current_photo_index)


@bot.message_handler(func=lambda message: message.text == "Назад в меню")
def back_to_menu(message: types.Message) -> None:
    """Возвращает пользователя в главное меню."""
    main(message)


@bot.message_handler(func=lambda message: message.text == "Под заказ")
def show_order_info(message: types.Message) -> None:
    """Информация о заказе."""
    bot.send_message(message.chat.id,
        (
            'Не нашли подходящее? Пишите, согласуем:  @mossnasty\n'
            'В сообщении укажите:\n'
            '- Пожелания, референсы\n'
            '- ФИО\n'
            '- Страна, Город, Улица, дом, кв и почтовый индекс.'
        )
    )


@bot.message_handler(func=lambda message: message.text == "Подписаться на канал")
def show_join_staby(message: types.Message) -> None:
    """Ссылка на канал."""
    bot.send_message(message.chat.id, 'Больше интересного здесь: @stabymoh')


@bot.message_handler(func=lambda message: message.text == "Уход")
def show_care_instructions(message: types.Message) -> None:
    """Инструкция по уходу за стабилизированным мхом."""
    bot.send_message(
        message.chat.id,
        (
            'Инструкция по уходу за стабилизированным мхом:\n'
            '- Температура: от +5 до +30 °C, влажность 60-80%.\n'
            '- Избегайте попадания прямых солнечных лучей и близкого расположения источников тепла.\n'
            '- Не допускайте попадания воды: не поливать, не опрыскивать.\n'
            '- Избегайте резких колебаний температуры и влажности.\n'
            '- Не использовать в помещениях с влажностью менее 30% или выше 80%.'
        )
    )


# Запуск бота
if name == "main":
    bot.polling(none_stop=True)
