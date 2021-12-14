import json
import os
from dotenv import load_dotenv

def get_bot_config():
    config_path = os.path.join(os.path.dirname(__file__), 'big_bot_config.json')
    with open(config_path) as f:
        BOT_CONFIG = json.load(f)
    return BOT_CONFIG

def get_sec_key():
    dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
    if os.path.exists(dotenv_path):
        load_dotenv(dotenv_path)
    SEC_KEY  = os.getenv("SECRET_KEY")
    return SEC_KEY
