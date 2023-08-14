from dotenv import load_dotenv
import os

load_dotenv()


TG_TOKEN = os.getenv('TG_TOKEN')
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')