from dotenv import load_dotenv
from robot import TelegramBot

# Load environment variables
load_dotenv()

if __name__ == '__main__':
    TelegramBot(debug=True).startup()
