import os
import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

#GSheets Imports: 
import gspread
from oauth2client.service_account import ServiceAccountCredentials
# from ai4bharat.transliteration import XlitEngine 

# ------------- Imports END -------------

API_KEY  = "5817719804:AAFTcrpvRSBwo1vE5HiVQe-cn5TuFASkQIk"
bot = telebot.TeleBot(API_KEY)

# GSheets Credentials start: 

# Google Sheets API Credentials
SCOPE = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
CREDENTIALS_FILE = 'RamayanaBotSACredentials.json'  # Path to your credentials JSON file

# Connect to Google Sheets
credentials = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, SCOPE)
client = gspread.authorize(credentials)

# spreadsheet_key = '1VRrnaSiLjVi9c_s638GUtzs-36LMJusLyFQJZiFBBy0'  
spreadsheet_key = '1y8D0WWgTQ-Vn-WjCIKKw5ugna3eoKFOHKMc2_HPKjlU'  # Replace with your actual spreadsheet key
sheet_name = 'Sheet1'  # Replace with your sheet name
sheet = client.open_by_key(spreadsheet_key).worksheet(sheet_name)

# ------------- Setup END -------------


# ------------- Functions Start -------------

# Set command suggestions
commands = [
    telebot.types.BotCommand('/father', 'Get father\'s name by character\'s name'),
    telebot.types.BotCommand('/mother', 'Get mother\'s name by character\'s name'),
    telebot.types.BotCommand('/help', 'Show available commands')
]
bot.set_my_commands(commands)

# Set up custom keyboard with buttons
keyboard = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True, one_time_keyboard=True)
button1 = KeyboardButton('\*/father_',)
button2 = KeyboardButton('/mother')
keyboard.add(button1, button2)

# Handle the /start command
@bot.message_handler(commands=['start'])
def handle_start_command(message):
    bot.reply_to(message, 'Jai Shree RAM! How can we assist you?', reply_markup=keyboard)

@bot.message_handler(commands = ['repMessage'])
def repMessage(message):
  bot.reply_to(message, "Hey",reply_markup=keyboard);  
  
@bot.message_handler(commands = ['sendMessage'],content_types="text")
def sendMessage(message):
  bot.send_message(message.chat.id, f"Hey This is a reply to a message {message.chat.id}");  

@bot.message_handler(commands = ['testDelete'])
def testDelete(message):
  bot.delete_message(message.chat.id, message.message_id)

# Handle the /father command
@bot.message_handler(commands=['father'])
def handle_father_command(message):
    command_parts = message.text.split()
    if len(command_parts) == 2:
        character_name = command_parts[1]
        father_name = get_father_name(character_name)
        if father_name:
            bot.send_message(message.chat.id,f"{character_name.capitalize()}'s father is {father_name.capitalize()}, Learn More : https://en.wikipedia.org/wiki/{father_name}") 
          
        else:
            bot.reply_to(message, f"No data found for {character_name.capitalize()}.")
    else:
        bot.reply_to(message, "Father's name for the character_name \t \n Command: /father character_name")

# Retrieve the father's name from the Google Spreadsheet
def get_father_name(character_name):
    data = sheet.get_all_values()
    for row in data:
        if character_name.lower() == row[0].lower():  # Assuming son names are in the first column
            return row[3] # Assuming father names are in the forth column
    return None

# Handle the /mother command
@bot.message_handler(commands=['mother'])
def handle_mother_command(message):
    command_parts = message.text.split()
    if len(command_parts) == 2:
        character_name = command_parts[1]
        mother_name = get_mother_name(character_name)
        if mother_name:
            bot.send_message(message.chat.id, f"{character_name.capitalize()}'s mother is {mother_name.capitalize()}. \n  Learn more: https://en.wikipedia.org/wiki/{mother_name}")
        else:
            bot.reply_to(message, f"No data found for {character_name}.")
    else:
        bot.reply_to(message, "Mother's name for the given character_name \t \n Command: /mother character_name")

# Retrieve the mother's name from the Google Spreadsheet
def get_mother_name(character_name):
    data = sheet.get_all_values()
    for row in data:
        if character_name.lower() == row[0].lower():  # Assuming son names are in the first column
            return row[4]  # Assuming mother names are in the fifth column
    return None

# Handle the /typing command
@bot.message_handler(commands=['typing'])
def handle_typing_command(message):
    bot.send_chat_action(message.chat.id, "Typing") 

# Handle the /invite command - Works only on groups :
@bot.message_handler(commands=['invite'])
def handle_invite_command(message):
    bot.export_chat_invite_link(message.chat.id) 

@bot.message_handler(func=lambda message: True, content_types=['audio', 'photo', 'voice', 'video', 'document','text', 'location', 'contact', 'sticker'])

def default_command(message):
  bot.send_message(message.chat.id, f"This is the default command handler. Input is {message.chat.id}")


bot.polling()

# Terminal commands - To create a virtual environment and run the bot - For VS CODE
# py -m venv ramayana_bot
# ramayana_bot\Scripts\activate