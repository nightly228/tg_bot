import telebot
from telebot import types
import os
from dotenv import load_dotenv
from typing import List, Tuple

load_dotenv()

TK = os.getenv('tb')
bot = telebot.TeleBot(TK)

@bot.message_handler(commands=['start'])
def main(message: types.Message) -> None:
    with open('./imagine/kk.jpeg', 'rb') as file:
        bot.send_photo(message.chat.id, file)

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton("Наличие")
    button2 = types.KeyboardButton("Под заказ")
    button3 = types.KeyboardButton("Уход")
    button4 = types.KeyboardButton("Подписаться на канал")
    keyboard.add(button1, button2, button3, button4)

    bot.send_message(message.chat.id,
                     'Доброго времени суток!\nЭтот бот поможет Вам с выбором эко-подарка и поможет узнать что-то новое, оставайтесь с нами!', reply_markup=keyboard)

photos: List[Tuple[str, str]] = [
    ('./imagine/1r.jpeg', 'Стильное панно влюбленные!\nШирина: 85 см\nВысота: 50 см\nОснова: хдф\nСтабилизированный мох: ...'),
    ('./imagine/2r.jpeg', 'Стильное панно дерево!\nШирина: 137 см\nВысота: 81 см\nОснова: фанера\n7500₽'),
    ('./imagine/3r.jpeg', '1890 ₽'),
    ('./imagine/4r.jpeg', '2450 ₽'),
    ('./imagine/5r.jpeg', 'Длинна: 50 см\nВысота: 50 см\nОснова: дерево\n3700 ₽')
]

current_photo_index: int = 0

@bot.message_handler(func=lambda message: message.text == "Наличие")
def show_photos(message: types.Message) -> None:
    global current_photo_index
    current_photo_index = 0
    send_photo_with_caption(message.chat.id, current_photo_index)

def send_photo_with_caption(chat_id: int, index: int) -> None:
    if index < 0 or index >= len(photos):
        return

    photo_path, caption = photos[index]

    try:
        with open(photo_path, 'rb') as photo_file:
            bot.send_photo(chat_id, photo_file, caption=caption)
    except FileNotFoundError as e:
        bot.send_message(chat_id, f"Ошибка: Файл не найден - {e}")
    except telebot.apihelper.ApiException as e:
        bot.send_message(chat_id, f"Ошибка API: {e}")
    except Exception as e:
        bot.send_message(chat_id, f"Произошла ошибка при отправке фото: {e}")

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)

    if index < len(photos) - 1:
        keyboard.add(types.KeyboardButton("Вперед"))
    if index > 0:
        keyboard.add(types.KeyboardButton("Назад"))

    keyboard.add(types.KeyboardButton("Назад в меню"))

    bot.send_message(chat_id, 'Выберите действие:', reply_markup=keyboard)

@bot.message_handler(func=lambda message: message.text == "Под заказ")
def show_order_info(message: types.Message) -> None:
    bot.send_message(message.chat.id, 'Не нашли подходящее? Пишите, согласуем:  @mossnasty\n В сообщении укажите:\nПожелания, референсы\nФИО\nСтрана, Город, Улица, дом, кв и почтовый индекс.')

@bot.message_handler(func=lambda message: message.text == "Подписаться на канал")
def show_join_staby(message: types.Message) -> None:
    bot.send_message(message.chat.id, 'Больше интересного здесь: @stabymoh')

@bot.message_handler(func=lambda message: message.text == "Уход")
def show_facts(message: types.Message) -> None:
    bot.send_message(message.chat.id, (
        'Инструкция по уходу за стабилизированным мхом:\n'
        'Стабилизированный мох должен находиться в закрытом помещении при температуре от +5 до +30 градусов Цельсия и влажности 60-80%.\n'
        'Необходимо предохранять их от попадания прямых солнечных лучей, близкого расположения галогенных ламп и других источников повышенной температуры, а также систем кондиционирования воздуха и вентиляции, которые могут привести к преждевременному высыханию мха.\n'
        'Необходимо избегать хранения стабилизированного мха в помещениях с повышенной влажностью, а также сухих помещениях, с влажностью менее 30%.\n'
        'Избегать прямого попадания воды, не поливать, не опрыскивать, не допускать резких колебаний температуры, приводящих к появлению конденсированной влаги. Не мыть стабилизированный мох в воде.'
    ))

# Убедитесь, что функция `send_photo_with_caption` уникальна и не повторяется.

from telebot import types, TeleBot
from typing import List, Tuple

# Определите свои переменные, включая photos и другие настройки
photos: List[Tuple[str, str]] = [
    ('./imagine/1r.jpeg', 'Описание 1'),
    ('./imagine/2r.jpeg', 'Описание 2'),
    # Добавьте остальные фотографии и описания
]

current_photo_index: int = 0

def send_photo_with_caption(chat_id: int, index: int) -> None:
    """Отправляет фото с подписью в указанный чат."""
    if index < 0 or index >= len(photos):
        return

    photo_path, caption = photos[index]

    try:
        with open(photo_path, 'rb') as photo_file:
            bot.send_photo(chat_id, photo_file, caption=caption)
    except FileNotFoundError:
        bot.send_message(chat_id, "Ошибка: файл не найден.")
    except telebot.apihelper.ApiException as api_error:
        bot.send_message(chat_id, f"Ошибка API: {api_error}")
    except Exception as e:
        bot.send_message(chat_id, f"Произошла ошибка при отправке фото: {e}")

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    if index < len(photos) - 1:
        keyboard.add(types.KeyboardButton("Вперед"))
    if index > 0:
        keyboard.add(types.KeyboardButton("Назад"))
    keyboard.add(types.KeyboardButton("Назад в меню"))

    bot.send_message(chat_id, 'Выберите действие:', reply_markup=keyboard)

@bot.message_handler(func=lambda message: message.text in ["Вперед", "Назад"])
def change_photo(message: types.Message) -> None:
    """Изменяет отображаемую фотографию."""
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

bot.polling(none_stop=True)
