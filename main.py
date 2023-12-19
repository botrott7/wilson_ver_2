from aiogram.utils import executor
from config.config import dp
from handlers import client, admin
from logibot.loggerbot import logger


async def on_startup(_):
    logger.info('Start BOT')
    print('Start')
    # sql_start()p


client.register_handlers_client(dp)
admin.register_handlers_admin(dp)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
