import os, dotenv
dotenv.load_dotenv()


telegram_bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
telegram_chat_id = int(os.getenv("TELEGRAM_CHAT_ID"))

os.makedirs("api/cache", exist_ok=True)