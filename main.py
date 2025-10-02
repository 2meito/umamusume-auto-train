import threading
import keyboard
import uvicorn
import traceback

from utils.helper import sleep
from utils.log import info, error, debug
from utils.adb_helper import ADB
import utils.constants as constants

import core.config as config

# from core.bot import Bot
from core.bot import Bot

from update_config import update_config
from server.main import app

hotkey = "f1"
adb = ADB()
bot = Bot(adb)


def main():
    print("Uma Auto!")
    try:
        config.reload_config()

        info(f"Config: {config.CONFIG_NAME}")
        bot.start()
        threading.Thread(target=bot.run, daemon=True).start()
    except Exception as e:
        error(f"Error in main thread: {e}")
        traceback.print_exc()


def hotkey_listener():
    while True:
        keyboard.wait(hotkey)
        if bot.is_running:
            bot.stop()
        else:
            main()
        sleep(0.5)


def start_server():
    host = "127.0.0.1"
    port = 8000
    info(f"Press '{hotkey}' to start/stop the bot.")
    print(f"[SERVER] Open http://{host}:{port} to configure the bot.")
    config = uvicorn.Config(app, host=host, port=port, workers=1, log_level="warning")
    server = uvicorn.Server(config)
    server.run()


if __name__ == "__main__":
    constants.adjust_constants_x_coords()
    update_config()
    threading.Thread(target=hotkey_listener, daemon=True).start()
    adb.connect()
    start_server()
