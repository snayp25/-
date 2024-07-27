import telebot
from main import Text2ImageAPI
import logging
import time
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

API_TOKEN = '6897585982:AAGjL-bQPF5zrsdPbr17N8MNneJbTUdLohc'

bot = telebot.TeleBot(API_TOKEN)


# Handle '/start' and '/help'
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)
def start(update: Update, context: CallbackContext) -> None:
    # Показываем статус "печатает"
    context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, """\
Привет, я EchoBot.
Я здесь для того, чтобы повторять за вами ваши добрые слова. Просто скажите что-нибудь приятное, и я скажу вам то же самое!\
""")
@bot.message_handler(commands=['help'])
def send_welcome(message):
    bot.reply_to(message, """Я бот для генерации картинок. Напишите то что хотите сгенерировать.
""")

# Handle all other messages with content_type 'text' (content_types defaults to ['text'])
@bot.message_handler(func=lambda message: True)
def echo_message(message):
    bot.send_chat_action(chat_id=message.chat.id, action="typing")
    import time
    time.sleep(5)
    # bot.send_message(message.chat.id, "typing")
    bot.reply_to(message, "Ваш заказ принят, ожидайте..")
    api = Text2ImageAPI('https://api-key.fusionbrain.ai/', '9987ED3717CA963CDB314E972CBF56AD', 'C380681D77C9EB0A8BE5A812615A3668')
    model_id = api.get_model()
    uuid = api.generate(message.text, model_id)
    images = api.check_generation(uuid)
    

  
    filename = f"image_{message.chat.id}.jpg"
    api.base64_img(images, filename)

    image = open (filename, 'rb')
    bot.send_photo(message.chat.id, photo=image)


    

bot.infinity_polling()

