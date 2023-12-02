# -*- coding: utf-8 -*-
# IMPORTS
import datetime
import logging
import threading
import time as t

import telegram
import yaml
from telegram import *
from telegram.ext import *
from datetime import *
# Another python files imports
from MySQL_Driver import *
from functions import *

###

# IMPORT CONFIGS
with open('config.yaml', 'r') as file:
    token = yaml.safe_load(file)
    token = token['TOKEN']

###
# LOGGER SETTINGS
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.WARNING)
loggerm = logging.getLogger("CM")

###

# DEFs
async def sqltest(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.effective_user.id == 1459969627:
        return
    texts = update.effective_message.text.split(" ")
    print(f"texts: {texts}")
    texts[0] = ""
    texts = ' '.join(texts)
    print(f"texts2: {texts}")
    c = executeSQL(texts).fetchall()
    print(f"C: {c}")
    for x in c:
        await update.effective_message.reply_text(x)


async def test(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.effective_user.id == 1459969627:
        return
    ParseUserSettings(update.effective_user.id)


async def start_private_chat(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_name = update.effective_user.full_name
    chat = update.effective_chat
    if chat.type != Chat.PRIVATE:
        return

    await update.effective_message.reply_text(
        f'Привіт {user_name}. Я бот під назвою "Поклич мене", як ти розумієш з назви я допомагаю кликати в чат '
        f'користувачів, але саме тоді коли їм зручно!\n'
        f'Введи /help щоб дізнатись команди, або /info щоб дізнатись додаткову інформацію\n'
        f'Вся детальна інформація по командам і усьому іншому в моїй Wiki ⬇️',
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton(text='Wiki', url='https://github.com/cheuS1-n/CallMeBotUA/wiki/%D0%94%D0%BE%D0%BC'
                                                   '%D1%96%D0%B2%D0%BA%D0%B0')]
        ]))


async def Register(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.type == "private":
        await update.effective_message.reply_text(
            "Зареєструватись можна тільки в чаті групи! Будь ласка, надішліть команду /reg в чат групи.")
        return
    MV = 0
    msg = update.effective_message
    CID = update.effective_chat.id
    UID = update.effective_user.id
    UNick = update.effective_user.username
    info = executeSQL(f"SELECT UserID from Main WHERE UserID={UID} AND ChannelID={CID}").fetchall()
    print(f"INFO: {info}")
    for x in info:
        print(x[0])
        if x[0] == UID:
            MV = MV + 1
    if MV == 0:
        if update.effective_user.username is None:
            if AddNewProfile(CID, UID, f"!{RBS(update.effective_user.first_name)}"):
                loggerm.info(
                    f"Added new user to DB:\nChannelID: {CID}, ChannelName: {update.effective_chat.title}, UserID: {UID}, UserFLName: {update.effective_user.full_name}\nAlternative method.")
                await update.effective_message.reply_text("Ви успішно зареєстровані! Надішліть /settings в приватні повідомлення для налаштування.")
                return
            else:
                loggerm.warning(
                    "DONT ADDED new user to DB:\nChannelID: {CID}, ChannelName: {update.effective_chat.title}, UserID: {UID}, UserFLName: {update.effective_user.full_name}\nAlternative method.")
                await msg.reply_text(
                    "Помилка реєстрації! Будь ласка, зверніться до @Quality2Length \nВін залюбки зі всім Вам допоможе!")
                return
        AddNewProfile(CID, UID, UNick)
        loggerm.info(
            f"Added new user to DB:\nChannelID: {CID}, ChannelName: {update.effective_chat.title}, UserID: {UID}, UserNickname: {UNick}")
        await update.effective_message.reply_text("Ви успішно зареєстровані! Надішліть /settings в приватні повідомлення для налаштування.")
        return
    elif MV > 0:
        await msg.reply_text(
            "Ви вже зареєстровані в цьому каналі! Для мого налаштування надішліть мені /settings в **приватні повідомлення.**",
            parse_mode=telegram.constants.ParseMode.MARKDOWN)


async def Profile(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.effective_chat.type == "private":
        await update.effective_message.reply_text("Ця команда може використовуватись тільки в ПП.")
        return

    channels = ""
    uC = CheckAllUserChannels(update.effective_user.id)
    if len(uC) == 0:
        await update.effective_message.reply_text("Ви не зареєстровані ні в одному каналі!")
        return
    print(f"LEN: {len(uC)}")
    print(uC)
    for x in uC:
        channel = await context.bot.getChat(chat_id=f'{x[0]}')
        channels = channels + f"\n{channel.title}"

    text = (
        f"Профіль користувача {update.effective_user.username}:\n"
        f"Список каналів в яких ви зареєстровані:\n"
        f"{channels}"
    )
    await update.effective_message.reply_text(text)


async def Settings(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.effective_chat.type == "private":
        await update.effective_message.reply_text("Ця команда може використовуватись тільки в ПП.")
        return
    if len(ParseUserSettings(update.effective_user.id)) == 0:
        await update.effective_message.reply_text(
            "Ви не зареєстровані ні в одному каналі! Для перегляду налаштувань, будь ласка, зареєструйтесь!")
        return

    info = ParseUserSettings(update.effective_user.id)[0]
    if int(info[1]) == 1:
        ST = "Активний"
    else:
        ST = "Не активний"
    if int(info[2]) == 0:
        TW = "Завжди"
    else:
        TW = f"{info[2]}"
    if int(info[3]) == 0:
        RT = "Без затримки"
    else:
        RT = f"{info[3]} секунд"
    if int(info[4]) == 0:
        DNDM = "Не активний"
    elif int(info[4]) == 1:
        DNDM = f"Активний (До вказаного часу)"
    elif int(info[4]) == 2:
        DNDM = f"Активний (Під час вказаного періоду)"

    text = (
        f"Налашування користувача {update.effective_user.username}\n"
        f"1. Стан: {ST} | /cs \n"
        f"2. Діапазон часу пінгу: (В розробці)\n"
        f"3. Час затримки пінгу: {RT} | /rtime \n"
        f'4. Режим "Не турбувати": (В розробці)\n'
        f'Інформація по налаштуванням: [Тут](https://github.com/cheuS1-n/CallMeBotUA/wiki/%D0%9A%D0%BE%D0%BC%D0%B0%D0%BD%D0%B4%D0%B8#%D1%80%D0%BE%D0%B7%D0%B1%D1%96%D1%80-%D0%BE%D0%BF%D1%86%D1%96%D0%B9)'
    )
    await update.effective_message.reply_text(text, parse_mode=telegram.constants.ParseMode.MARKDOWN,
                                              disable_web_page_preview=True)


async def Ping(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.type == "private":
        await update.effective_message.reply_text("Ця команда може використовуватись тільки в чаті.")
        return
    CID = update.effective_chat.id
    info = ParseAllUsers(CID)
    if len(info) == 0:
        await update.effective_message.reply_text(
            "Відсутні зареєстровані користувачі. Щоб зареєструвати для пінгу - /reg")
    PINGLIST = []
    PRINTLIST = []
    APINGLIST = []
    print(f"RTM:")
    for x in info:
        settings = ParseUserSettings(x[1])[0]
        print(f"X: {x}")
        RT = settings[3]
        ct = datetime.today()
        ct1 = datetime.today().strftime("%d/%m/%y %H:%M:%S.%f")

        print(f"SETTINGS: {settings}")

        if int(settings[1]) == 1:
            print("+")
            if x[3] is None:
                print("+N")
                LPTSettings(x[0], x[1], ct1)
                if x[2].startswith("!"):
                    nick = x[2].replace("!", "")
                    id = x[1]
                    APINGLIST.extend([f"[{nick}](tg://user?id={id})"])
                    print("ADDED")
                else:
                    PINGLIST.extend([f"@{x[2]}"])
                    print("ADDED")
                continue
            else:
                print("+NN")
                dif2 = datetime.strptime(x[3], "%d/%m/%y %H:%M:%S.%f") + timedelta(seconds=RT)
                dif = dtTTS(ct, dif2)
                print(f"DIF: {dif} | DIF2: {dif2}")
                if dif >= 0:
                    print("+>0")
                    continue
                elif dif < 0:
                    print("+<0")
                    LPTSettings(x[0], x[1], ct1)
                    if x[2].startswith("!"):
                        nick = x[2].replace("!", "")
                        id = x[1]
                        APINGLIST.extend([f"[{nick}](tg://user?id={id})"])
                        print("ADDED")
                    else:
                        PINGLIST.extend([f"@{x[2]}"])
                        print("ADDED")
                    print("ADDED")
                    continue

        elif int(settings[1]) == 0:
            print("settings0 return")
            continue
    if len(PINGLIST) == 0 and len(APINGLIST) == 0:
        await update.effective_message.reply_text(
            "На жаль, список на пінг пустий[2].Для детальнішої інформації, прочитайте [Wiki(ЧаПи)](https://github.com/cheuS1-n/CallMeBotUA/wiki/%D0%A7%D0%B0%D0%9F%D0%B8)",
            parse_mode=telegram.constants.ParseMode.MARKDOWN, disable_web_page_preview=True)
        return
    MV = 0
    for x in range(len(PINGLIST)):
        print(f"MV: {MV}")
        if len(PINGLIST) == 0:
            print("PINGNULL")
            break
        PRINTLIST.extend([f"{PINGLIST[MV]}"])
        MV = MV + 1
        if (MV % 4) == 0:
            print("SENDMSG MV%")
            await update.effective_chat.send_message(' '.join(PRINTLIST))
            PRINTLIST.clear()
        elif (MV % 4) > 0:
            print("MV%>0")
            if (len(PINGLIST) - MV) <= 4:
                print("<4")
                for x in range(len(PINGLIST) - MV):
                    PRINTLIST.extend([f"{PINGLIST[MV]}"])
                    MV = MV + 1
                await update.effective_chat.send_message(' '.join(PRINTLIST))
                break

        print(f"{MV % 4} |||")

    PINGLIST.clear()
    PRINTLIST.clear()
    MV = 0
    print(f"LENA: {len(APINGLIST)} | {APINGLIST}")
    if not len(APINGLIST) == 0:
        print(f"APL: {APINGLIST}")
        for x in APINGLIST:
            PRINTLIST.extend([f"{APINGLIST[MV]}"])
            MV = MV + 1
            if (MV % 4) == 0:
                print("ASENDMSG MV%")
                await update.effective_chat.send_message(' '.join(PRINTLIST),
                                                         parse_mode=telegram.constants.ParseMode.MARKDOWN)
                PRINTLIST.clear()
            elif (MV % 4) > 0:
                print("AMV%>0")
                if (len(PINGLIST) - MV) <= 4:
                    print("<4A")
                    for x in range(len(PINGLIST) - MV):
                        PRINTLIST.extend([f"{PINGLIST[MV]}"])
                        MV = MV + 1
                    await update.effective_chat.send_message(' '.join(PRINTLIST),
                                                             parse_mode=telegram.constants.ParseMode.MARKDOWN)
                    break

    print(PINGLIST)


async def Info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.effective_message.reply_text(
        "Інформація про бота та інше.\n"
        'Бот "Поклич мене" є вашим помічником, він буде кликати Вас саме тоді, коли зручно Вам!(буде, коли дороблю '
        'налаштування :) )\n'
        'Версія: 0.4 (Ранній реліз)\n'
        "Власник: @Quality2Length\n"
        'В бота "Поклич мене!" є також Lite версія(@CallMeBotUALite_bot), попробуйте і її.\n',
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton(text='Wiki',
                                  url='https://github.com/cheuS1-n/CallMeBotUA/wiki/%D0%94%D0%BE%D0%BC%D1%96%D0%B2%D0%BA%D0%B0')],
            [InlineKeyboardButton(text='Github', url='https://github.com/cheuS1-n/CallMeBotUA/')],
            [InlineKeyboardButton(text='Різниця між Lite і простою версією',
                                  url='https://github.com/cheuS1-n/CallMeBotUA/wiki/%D0%A0%D1%96%D0%B7%D0%BD%D0%B8%D1%86%D1%8F-%D0%BC%D1%96%D0%B6-%D0%B7%D0%B2%D0%B8%D1%87%D0%B0%D0%B9%D0%BD%D0%BE%D1%8E-%D1%82%D0%B0-Lite-%D0%B2%D0%B5%D1%80%D1%81%D1%96%D1%94%D1%8E.')],
        ])
    )


async def Help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        'Команди бота "Поклич мене"\n'
        "```/ping```\n"
        "```/reg```\n"
        "```/settings```\n"
        "```/profile```\n"
        "```/userlist```\n"
        "```/cs```\n"
        "```/rtime```\n"
        'Для детальнішої інформації по командам, прочитайте Wiki'
    )
    await update.effective_message.reply_text(text, parse_mode=telegram.constants.ParseMode.MARKDOWN,
                                              disable_web_page_preview=True,
                                              reply_markup=InlineKeyboardMarkup([
                                                  [InlineKeyboardButton(text='Wiki',
                                                                        url='https://github.com/cheuS1-n/CallMeBotUA/wiki/%D0%9A%D0%BE%D0%BC%D0%B0%D0%BD%D0%B4%D0%B8')],
                                              ]))


async def AllUsersInChannel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.type == "private":
        await update.effective_message.reply_text("Ця команда може використовуватись тільки в чаті.")
        return
    AU = []
    info = ParseAllUsers(update.effective_chat.id)
    ET = ""
    if len(info) == 0:
        await update.effective_message.reply_text("В цьому чаті відсутні зареєстровані користувачі! | Wiki - /info")
        return
    for x in info:
        set = ParseUserSettings(x[1])
        if int(set[0][1]) == 0:
            ET = f"{x[2]} (користувач виключив можливіть пінгу)"
        else:
            ET = f"{x[2]}"
        AU.extend([f"{ET}"])
    alt = '\n'.join(AU)
    text = (
        "Всі зареєстровані користувачі:\n"
        f"{alt}"
    )
    await update.effective_message.reply_text(text)


###
# Main DEFs
async def ChangeState(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global text
    if not update.effective_chat.type == "private":
        await update.effective_message.reply_text("Ця команда може використовуватись тільки в ПП.")
        return
    if len(ParseUserSettings(update.effective_user.id)) == 0:
        await update.effective_message.reply_text(
            "Ви не зареєстровані ні в одному каналі! Для зміни налаштувань, будь ласка, зареєструйтесь!")
        return
    info = ParseUserSettings(update.effective_user.id)
    State = info[0][1]
    UState = 0
    if int(State) == 0:
        UState = 1
    elif int(State) == 1:
        UState = 0
    if UState == 1:
        text = (
            "Тепер я буду кликати Вас!"
        )
    elif UState == 0:
        text = (
            "Тепер я не буду кликати Вас!"
        )
    if StateSettings(update.effective_user.id, UState):
        await update.effective_message.reply_text(text)


async def ChangeRT(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.effective_chat.type == "private":
        await update.effective_message.reply_text("Ця команда може використовуватись тільки в ПП.")
        return
    if len(ParseUserSettings(update.effective_user.id)) == 0:
        await update.effective_message.reply_text(
            "Ви не зареєстровані ні в одному каналі! Для перегляду налаштувань, будь ласка, зареєструйтесь!")
        return
    if len(update.effective_message.text.split(" ")) <= 1:
        await update.effective_message.reply_text("Приклад введення команди: /rtime ЧасВСекундах | [Інформація]("
                                                  "https://github.com/cheuS1-n/CallMeBotUA/wiki/%D0%9A%D0%BE%D0%BC%D0%B0%D0%BD%D0%B4%D0%B8#rtime)",
                                                  parse_mode=telegram.constants.ParseMode.MARKDOWN,
                                                  disable_web_page_preview=True)

    if int(update.effective_message.text.split(" ")[1]) > 18000:
        await update.effective_message.reply_text("Ви не можете поставити час затримки більше 5 годин - 18000 секунд.")
        return
    if int(update.effective_message.text.split(" ")[1]) < 0:
        await update.effective_message.reply_text("Ви не можете поставити від'ємний час. Час має бути більшим/рівним нулю.")
        return
    info = ParseUserSettings(update.effective_user.id)
    args = int(update.effective_message.text.split(" ")[1])
    print(f"ARGS: {args}")
    text = (
        f'Значення опції "Час затримки пінгу" встановлено на {args} секунд'
    )
    if RTSettings(update.effective_user.id, args):
        await update.effective_message.reply_text(text)


async def Updater(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if len(update.effective_message.new_chat_members) != 0:
        for member in update.effective_message.new_chat_members:
            print(f"MEMBERU: {member.username} CBG: {context.bot.username}")
            if member.username == context.bot.username:
                await update.effective_chat.send_message(
                    'Всім привіт, тепер я буду кликати всіх саме тоді, коли їм буде зручно!\n'
                    'Щоб я почав Вас кликати, будь ласка, зареєструйтесь - /reg\n'
                    'Налаштуйте мене під свої потреби, перевірити свої налаштування - /settings\n'
                    '*Вся інформація по використанню команд та моєму налаштуванню є в Wiki*',
                    reply_markup=InlineKeyboardMarkup([
                        [InlineKeyboardButton(text='Wiki',
                                              url='https://github.com/cheuS1-n/CallMeBotUA/wiki/%D0'
                                                  '%94%D0%BE%D0%BC%D1%96%D0%B2%D0%BA%D0%B0')],
                    ]), parse_mode=telegram.constants.ParseMode.MARKDOWN)
    UNick = update.effective_user.username
    UID = update.effective_user.id
    CID = update.effective_chat.id
    info = ParseUserInfoC(UID, CID)

    print(UID)
    print(CID)
    print(info)
    if len(info) == 0:
        print("LEN 0")
        return

    if update.effective_user.username is None:
        print("NONE")

        if str(info[0][2]) == str(f"!{RBS(update.effective_user.first_name)}"):
            loggerm.info(
                f"Update not need, nicks are indentical\nChannelID: {CID}, ChannelName: {update.effective_chat.title}, UserID: {UID}, UserFLName: {update.effective_user.full_name}\n Alternative method")
            return
        else:
            if ChangeNick(update.effective_user.id, f"!{RBS(update.effective_user.first_name)}"):
                loggerm.info(
                    f"NICK CHANGED!\nChannelID: {CID}, ChannelName: {update.effective_chat.title}, UserID: {UID}, UserFLName: {update.effective_user.full_name}, OldNickName: {info[0][2]}\nAlternative method.")
                return
            else:
                logger.warning(
                    f"NICKS DONT CHANGED, CHANGE ERROR!\nChannelID: {CID}, ChannelName: {update.effective_chat.title}, UserID: {UID}, UserFLName: {update.effective_user.full_name}, OldNickName: {info[0][2]}\nAlternative method.")
                return
    if str(info[0][2]) == str(UNick):
        print("Update not need, nicks are indentical")
        return
    else:
        print("UPDATE NEED, nicks different")
    if ChangeNick(UID, UNick):
        print("NICK CHANGED")
    else:
        print("Nick Dont changed")

def START():
    while True:
        if startdbs():
            application = ApplicationBuilder().token(token).build()

            start_handler = CommandHandler('sql', sqltest)
            testh = CommandHandler('test', test)
            application.add_handler(start_handler)
            application.add_handler(testh)
            application.add_handler(CommandHandler('reg', Register))
            application.add_handler(CommandHandler('profile', Profile))
            application.add_handler(CommandHandler('cs', ChangeState))
            application.add_handler(CommandHandler('settings', Settings))
            application.add_handler(CommandHandler('ping', Ping))
            application.add_handler(CommandHandler('info', Info))
            application.add_handler(CommandHandler('userlist', AllUsersInChannel))
            application.add_handler(CommandHandler('help', Help))
            application.add_handler(CommandHandler('rtime', ChangeRT))
            application.add_handler(CommandHandler('start', start_private_chat))
            application.add_handler(MessageHandler(filters.ALL, Updater))

            application.run_polling()

START()