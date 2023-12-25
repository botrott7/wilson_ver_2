from aiogram.utils import executor
from config.config import dp, bot
from handlers import client, admin
from logibot.loggerbot import logger
from keyboards_inline.menu import set_main_menu

async def on_startup(_):
    logger.info('Start BOT')
    await set_main_menu(bot)
    print('Start')


client.register_handlers_client(dp)
admin.register_handlers_admin(dp)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
