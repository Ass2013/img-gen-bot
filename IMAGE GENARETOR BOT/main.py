import telebot
import requests

from config import TOKEN, DATABASE
from logic import DatabaseManager

bot = telebot.TeleBot(TOKEN)
db = DatabaseManager(DATABASE)


# START
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(
        message.chat.id,
        "Just write what image you want.\nExample: make a black square"
    )


# ANY TEXT = IMAGE GENERATION
@bot.message_handler(func=lambda message: True)
def generate(message):
    username = message.from_user.username
    prompt = message.text

    bot.send_message(message.chat.id, "Generating...")

    # save prompt
    db.save_image(username, prompt)

    # create image link
    url = "https://image.pollinations.ai/prompt/" + prompt.replace(" ", "_")

    # download image
    img = requests.get(url).content

    file = open("image.jpg", "wb")
    file.write(img)
    file.close()

    # send image
    file = open("image.jpg", "rb")
    bot.send_photo(message.chat.id, file)
    file.close()


print("Bot running...🏃‍➡️🏃‍♂️‍➡️🏃‍♀️‍➡️🏃🏃‍♂️🏃‍♀️")
bot.infinity_polling()
import telebot
import requests

from config import TOKEN, DATABASE
from logic import DatabaseManager

bot = telebot.TeleBot(TOKEN)
db = DatabaseManager(DATABASE)


# START
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(
        message.chat.id,
        "Just write what image you want me to generate.✅\nExample: make a black square⬛"
    )

# SHOW HISTORY
@bot.message_handler(commands=['show'])
def show(message):
    username = message.from_user.username
    images = db.get_images(username)

    if not images:
        bot.send_message(message.chat.id, "No images yet❌")
        return

    text = "Your prompts:\n"
    for i in images:
        text += "- " + i[0] + "\n"

    bot.send_message(message.chat.id, text)

 
@bot.message_handler(func=lambda message: True)
def generate(message):
    username = message.from_user.username
    prompt = message.text

    bot.send_message(message.chat.id, "Generating...")

    db.save_image(username, prompt)

    url = "https://image.pollinations.ai/prompt/" + prompt.replace(" ", "_")

    response = requests.get(url)

    if response.status_code != 200 or len(response.content) < 1000:
        bot.send_message(message.chat.id, "Image failed, try again ❌")
        return

    file = open("image.jpg", "wb")
    file.write(response.content)
    file.close()

    file = open("image.jpg", "rb")
    bot.send_photo(message.chat.id, file)
    file.close()




print("Bot running...")
bot.infinity_polling()