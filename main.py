import telebot
from flask import Flask, request
from telebot import types
import os
from dotenv import load_dotenv
from typing import List, Tuple

load_dotenv()

TOKEN: str = os.getenv("tb")
bot = telebot.TeleBot(TOKEN)
server = Flask(__name__)

# Список фото и описаний
photos: List[Tuple[str, str]] = [
    ('./imagine/1r.jpeg', 'Описание товара 1'),
    ('./imagine/2r.jpg', 'Описание товара 2'),
    ('./imagine/3r.jpg', 'Описание товара 3'),
    ('./imagine/4r.jpg', 'Описание товара 4'),
    ('./imagine/5r.jpg', 'Описание товара 5')
]

current_photo_index: int = 0

@bot.message_handler(commands=['start'])
def main(message: types.Message) -> None:
    try:
        with open('./imagine/kk.jpeg', 'rb') as file:
            bot.send_photo(message.chat.id, file)

        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(
            types.KeyboardButton("Наличие"),
            types.KeyboardButton("Под заказ"),
            types.KeyboardButton("Уход"),
            types.KeyboardButton("Подписаться на канал")
        )

        bot.send_message(message.chat.id,
                         'Доброго времени суток! Этот бот поможет Вам с выбором эко-подарка!',
                         reply_markup=keyboard)
    except Exception as e:
        print(f"[start error] {e}")

@bot.message_handler(func=lambda message: message.text == "Наличие")
def show_photos(message: types.Message) -> None:
    global current_photo_index
    current_photo_index = 0
    send_photo_with_caption(message.chat.id, current_photo_index)

def send_photo_with_caption(chat_id: int, index: int) -> None:
    try:
        photo_path, caption = photos[index]
        with open(photo_path, 'rb') as file:
            bot.send_photo(chat_id, file, caption=caption)

        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        if index < len(photos) - 1:
            keyboard.add(types.KeyboardButton("Вперед"))
        if index > 0:
            keyboard.add(types.KeyboardButton("Назад"))
        keyboard.add(types.KeyboardButton("Назад в меню"))
        bot.send_message(chat_id, "Выберите действие:", reply_markup=keyboard)

    except Exception as e:
        print(f"[photo error] {e}")

@bot.message_handler(func=lambda message: message.text in ["Вперед", "Назад"])
def change_photo(message: types.Message) -> None:
    global current_photo_index
    if message.text == "Назад" and current_photo_index > 0:
        current_photo_index -= 1
    elif message.text == "Вперед" and current_photo_index < len(photos) - 1:
        current_photo_index += 1
    send_photo_with_caption(message.chat.id, current_photo_index)

@bot.message_handler(func=lambda message: message.text == "Назад в меню")
def back_to_menu(message: types.Message) -> None:
    main(message)

@bot.message_handler(func=lambda message: message.text == "Под заказ")
def show_order_info(message: types.Message) -> None:
    bot.send_message(message.chat.id,
                     'Пишите @mossnasty\nУкажите: пожелания, ФИО, адрес.')

@bot.message_handler(func=lambda message: message.text == "Подписаться на канал")
def show_join_staby(message: types.Message) -> None:
    bot.send_message(message.chat.id,
                     'Больше интересного здесь: @stabymoh')

@bot.message_handler(func=lambda message: message.text == "Уход")
def show_facts(message: types.Message) -> None:
    bot.send_message(message.chat.id,
                     'Инструкция по уходу за стабилизированным мхом:\n...')

# Webhook обработчик
@server.route(f"/{TOKEN}", methods=["POST"])
def webhook() -> tuple:
    update = telebot.types.Update.de_json(request.data.decode("utf-8"))
    bot.process_new_updates([update])
    return "ok", 200

# Установка Webhook
@server.route("/", methods=["GET"])
def set_webhook() -> tuple:
    bot.remove_webhook()
    webhook_url = f"https://{os.getenv('RENDER_URL')}/{TOKEN}"
    bot.set_webhook(url=webhook_url)
    return "Webhook установлен", 200

if __name__ == "__main__":
    server.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
