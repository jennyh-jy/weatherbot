import os

BOT_TOKEN = os.environ.get('BOT_TOKEN', '')
CHAT_ID = os.environ.get('CHAT_ID', '')

if not BOT_TOKEN or not CHAT_ID:
    raise Exception('Check either BOT_TOKEN or CHAT_ID!')
