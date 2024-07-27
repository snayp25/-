import telebot
from main import Text2ImageAPI
count = 0 
API_TOKEN = '6897585982:AAGjL-bQPF5zrsdPbr17N8MNneJbTUdLohc'

bot = telebot.TeleBot(API_TOKEN)


# Handle '/start' and '/help'
@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    bot.reply_to(message, """\
Hi there, I am EchoBot.
I am here to echo your kind words back to you. Just say anything nice and I'll say the exact same thing to you!\
""")


# Handle all other messages with content_type 'text' (content_types defaults to ['text'])
@bot.message_handler(func=lambda message: True)
def echo_message(message):
    bot.reply_to(message, "Ваш заказ принят, ожидайте..")
    api = Text2ImageAPI('https://api-key.fusionbrain.ai/', '9987ED3717CA963CDB314E972CBF56AD', 'C380681D77C9EB0A8BE5A812615A3668')
    model_id = api.get_model()
    uuid = api.generate(message.text, model_id)
    images = api.check_generation(uuid)
   

  
    filename = f"image_{message.chat.id}.jpg"
    api.base64_img(images, filename)

    image = open (filename, 'rb')
    bot.send_photo(message.chat.id, photo=image)
    count =+ 1 

    if count == 2:
        bot.reply_to(message, "-")

bot.infinity_polling()