import telebot
  from telebot import types
  import os
  from dotenv import load_dotenv

  load_dotenv()

  TK = os.getenv('tb')
  bot = telebot.TeleBot(TK)
  @bot.message_handler(commands=['start'])
  def main(message):
      with open('./.venv/imagine/kk.jpeg', 'rb') as file:
         bot.send_photo(message.chat.id, file)

      keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
      button1 = types.KeyboardButton("Наличие")
      button2 = types.KeyboardButton("Под заказ")
      button3 = types.KeyboardButton("Уход")
      button4 = types.KeyboardButton("Подписаться на канал")
      keyboard.add(button1, button2, button3, button4)

      bot.send_message(message.chat.id,
                     'Доброго времени суток!\nУбедительная просьба: не тыкайте на все кнопочки сразу, так как бот может подвиснуть. Спасибо!\nЭтот бот поможет Вам с выбором эко-подарка и поможет узнать что-то новое, оставайтесь с нами!', reply_markup=keyboard)


  photos = [
      ('./.venv/imagine/1r.jpeg', 'Стильное панно влюбленные!\nШирина: 85 см\nВысота: 50 см\nОснова: хдф\nСтабилизированный мох:\nДекор под заказ\n Мнoго издeлий в наличии\n Выбор цвета мха из палитры 35+оттенков\nНе требует полива\nОтличный подapок\nВ случае если у вас очень ограничен бюджет на озеленение, напишите мне, я вам предложу вам способ с минимальными затратами и максимальным визуальным эффектом\n4150₽\nДля заказа пишите @mossnasty\nВ сообщении укажите: фото желаемого пано, Ваше ФИО, адрес доставки полностью '),
      ('./.venv/imagine/2r.jpeg', 'Стильное панно дерево!\nШирина: 137 см\nВысота: 81 см\nОснова: фанера\n7500₽'),
      ('./.venv/imagine/3r.jpeg', '1890 ₽'),
      ('./.venv/imagine/4r.jpeg', '2450 ₽'),
      ('./.venv/imagine/5r.jpeg', 'Длинна: 50 см\nВысота: 50 см\nОснова: дерево\nВ случае если у вас очень ограничен бюджет на озеленение, напишите мне, я предложу вам способ с минимальными затратами и максимальным визуальным эффектом\n3700 ₽')
]

  current_photo_index = 0



  @bot.message_handler(func=lambda message: message.text == "Наличие")
  def show_photos(message):
      global current_photo_index
      current_photo_index = 0
      send_photo_with_caption(message.chat.id, current_photo_index)


  def send_photo_with_caption(chat_id, index):
      if index < 0 or index >= len(photos):
          return

      photo_path, caption = photos[index]

      try:
          with open(photo_path, 'rb') as photo_file:
              bot.send_photo(chat_id, photo_file, caption=caption)
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
  def show_order_info(message):
      bot.send_message(message.chat.id, 'Не нашли подходящее? Пишите, согласуем:  @mossnasty\n В сообщении укажите:\nПожелания, референсы\nФИО\nСтрана, Город, Улица, дом, кв и почтовый индекс ')

  @bot.message_handler(func=lambda message: message.text == "Подписаться на канал")
  def show_join_staby(message):
      bot.send_message(message.chat.id, 'Больше интересного здесь: @stabymoh')


  @bot.message_handler(func=lambda message: message.text == "Уход")
  def show_facts(message):
      bot.send_message(message.chat.id, 'Инструкция по уходу за стабилизированным мхом:''Стабилизированный мох должен находиться в закрытом помещении при температуре от +5 до +30 градусов Цельсия и влажности 60-80%.''Необходимо предохранять их от попадания прямых солнечных лучей, близкого расположения галогенных ламп и других источников повышенной температуры, а также систем кондиционирования воздуха и вентиляции, которые могут привести к преждевременному высыханию мха.''•Необходимо избегать хранения стабилизированного мха в помещениях с повышенной'
'влажностью, а также сухих помещениях, с влажностью менее 30%.''Избегать прямого попадания воды, не поливать, не опрыскивать, не допускать резких'
'колебаний температуры, приводящих к появлению конденсированной влаги. Не мыть стабилизированный мох в воде.')


  def send_photo_with_caption(chat_id, index):
      if index < 0 or index >= len(photos):
          return

      photo_path, caption = photos[index]

      with open('./.venv/imagine/1r.jpeg', 'rb') as photo_file:
          bot.send_photo(chat_id, photo_file, caption=caption)


  @bot.message_handler(func=lambda message: message.text == "Наличие")
  def show_photos(message):
      global current_photo_index
      current_photo_index = 0
      send_photo_with_caption(message.chat.id, current_photo_index)


  def send_photo_with_caption(chat_id, index):
      if index < 0 or index >= len(photos):
          return

      photo_path, caption = photos[index]

      try:
          with open(photo_path, 'rb') as photo_file:
              bot.send_photo(chat_id, photo_file, caption=caption)
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
  def change_photo(message):
      global current_photo_index

      if message.text == "Назад" and current_photo_index > 0:
          current_photo_index -= 1
      elif message.text == "Вперед" and current_photo_index < len(photos) - 1:
          current_photo_index += 1

      send_photo_with_caption(message.chat.id, current_photo_index)


  @bot.message_handler(func=lambda message: message.text == "Назад в меню")
  def back_to_menu(message):
      main(message)

  bot.polling(none_stop=True)
