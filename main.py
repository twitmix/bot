from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

bot = Bot(token='5878753811:AAHVGyNtfcIlDfjDuw8OFnpYAggmzTYtVdE')
dp = Dispatcher(bot)

BASE = {}
@dp.message_handler(commands=['start'])
async def start(message):
    BASE[message.chat.id] = ['', message.from_user.username, True, 0]
    await bot.send_message(message.chat.id, "Привет, я бот для поиска команды\nдля того чтобы искать команду тебе нужно создать анкету\nнапиши кто ты и кого хочешь найти.")
    print(BASE)

@dp.message_handler(commands=['help'])
async def help(message):
    await bot.send_message(message.chat.id, "/reg - пройти регестрацию заново\n"
                                            "/help - помощь\n"
                                            "/start - полный перезапуск бота")
    print(BASE)
@dp.message_handler(commands=['reg'])
async def reg(message):
    BASE[message.chat.id] = ['', message.from_user.username, True]
    await bot.send_message(message.chat.id, "напиши кто ты и кого хочешь найти")
    print(BASE)

@dp.message_handler(content_types=['text'])
async def main(message):
    global BASE
    keys = list(BASE.keys())
    if message.chat.id not in keys:
       await bot.send_message(message.chat.id, "Тебе нужно заргистрироваться, напиши /start")
    else:
        keys.pop(keys.index(message.chat.id))
        from_user = BASE[message.chat.id].copy()

        btn_n = KeyboardButton('следущая анкета')
        btn_ch = KeyboardButton('изменить анкету')
        btn_help = KeyboardButton('Обратная связь')
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(btn_ch, btn_n, btn_help)

        if from_user[2]:
            from_user[2] = False
            from_user[0] = message.text
            if len(keys) == 0:
                await bot.send_message(message.chat.id, 'Нету других анкет', reply_markup=markup)
            else:
                await bot.send_message(message.chat.id, f"Первая анкета:\n"
                                                        f"{BASE[keys[0]][0]}\n"
                                                        f"Telegram: @{BASE[keys[0]][1]}", reply_markup=markup)
                from_user[3] += 1
        else:
            if message.text == 'изменить анкету':
                await bot.send_message(message.chat.id, 'Напиши кто ты и кого хочешь найти')
                from_user[2] = True
            elif message.text == 'обратная связь':
                await bot.send_message(message.chat.id, 'Если у тебя не работает бот или у тебя есть рекомендации по улучшению бота, ты можешь написать мне - @twitmix123')
            elif message.text == 'следущая анкета':
                if len(keys) == 0:
                    await bot.send_message(message.chat.id, 'Нет других анкет')
                else:
                    an = BASE[keys[from_user[3] % len(keys)]]
                    await bot.send_message(message.chat.id, f"Вот следущая анкета:\n"
                                                            f"{an[0]}\n"
                                                            f"Telegram: @{an[1]}")
                    from_user[3] += 1		
            else:
                await bot.send_message(message.chat.id, 'Нет такой команды')
        if from_user[3] % 100 == 0 and from_user[3] != 0:
            await bot.send_message(message.chat.id, f"Ты посмотрел уже{from_user[3]} анкет")
        BASE[message.chat.id] = from_user.copy()
        from_user.clear()
        print(BASE)

if __name__ == '__main__':
    executor.start_polling(dp)
