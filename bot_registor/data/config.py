from os import getenv
from dotenv import load_dotenv

# Bot token can be obtained via https://t.me/BotFather
load_dotenv()
DB_NAME = getenv('DB_NAME')
USER = getenv('DB_USER')
PASSWORD = getenv('PASSWORD')
HOST = getenv('HOST')
PORT = getenv('PORT')

if __name__ == '__main__':
    print(DB_NAME, USER, PASSWORD, HOST, PORT)
