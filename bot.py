import asyncio, random, json, os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKENS = [
    "8419753295:AAG-EbfqSaQju1RrdaAY-F-vm2cEE9JqeGY",
    "8584138389:AAGXfkQ79AAI7mVOPtjkUOdhEBT0MNuupgc",
    "7771656978:AAHloLS84YdP2onrA60kGbTbDcHoDqSIz-o",
    "8078384083:AAHoRh8bqFd2cH0CBvyWwN4jXWnjSF_F5vY",
    "7875735234:AAElquAKoVeL5rKw9l-2eCvVHePsbVi34jo",
    "8074813042:AAHF3R6V3S8Q2LDHv3CYwpauJUO2x6mtpuo",
    "7971023306:AAEyomUs9kQzZ2niq832cyHvMgmylNYaj-0",
    "8680113020:AAEM5iBPhdbMe1ac9xG6AfPARgI48kOJprE",
    "8795707975:AAGGkF84zbak-IA-e4ZvbmFZcLbMZ_QUqeU",
    "8561350618:AAHcxsHRdQIP8RVuuLdqxLqfSIEp5jNFT48",
]

OWNER_ID = 7783086532
SUDO_FILE = "sudo.json"

if os.path.exists(SUDO_FILE):
    with open(SUDO_FILE) as f: sudo_users = set(json.load(f))
else: sudo_users = {OWNER_ID}

def save_sudo():
    with open(SUDO_FILE, "w") as f: json.dump(list(sudo_users), f)

DESTROY_TEXTS = [
    "Kya?? 😂😂\n\n  Teri???😂😂😂\n\n    Maa???? 😂😂😂😂\n\n       Randy????? 😂😂😂😂😂",
    "▒░✍️ teri maa ki chudai me maja aya ▒░✍️",
    "LUND LELE",
    "Bhagwan Na Ban Jau Isliye TERI MA Bhi CH0DTA hu",
    "तेरी माँ रैंडी है 👏🏻👏🏻👏🏻",
    "Chup rndyke bche",
    "Gc left le rndyk pille",
    "Qbnrs uth rndyk pille tery bhen k pait me thuda marun",
    "Try maa k saar pe lund marke puncture kar du",
    "Stay strong 😹😹💪\nNa na Rona ni h",
]

NC_EMOJIS = [
    "😋","😝","😜","🤪","😑","🤫","🤭","🥱","🤗","😡","😠","😤",
    "😮‍💨","🙄","😒","🥶","🥵","🤢","😎","🥸",
    "😹","💫","😼","😽","🙀","😿","😾",
    "🙈","🙉","🙊","⭐","🌟","✨","⚡","💥","💨",
    "💛","💙","💜","🤎","🤍","💘","💝"
]

REACT_EMOJI = "🤣"

destroy_name = None; destroy_active = False
attack_id = None
gcname_text = None; gcname_active = False
spam_text = None; spam_active = False
react_id = None
bot_apps = []
nc_index = 0

def ok(u): return u in sudo_users

def stretch(text):
    result = text
    while len(result) < 4000:
        result += "\n\n\n\n" + text
    return result[:4000]

async def init_bots():
    global bot_apps
    for t in TOKENS:
        try:
            app = Application.builder().token(t).build()
            await app.initialize()
            bot_apps.append(app)
        except: pass
    print(f"DRAGY ONLINE — {len(bot_apps)}/10 bots")

async def all_msg(chat_id, text, reply=None):
    async def send(app):
        try: await app.bot.send_message(chat_id, text, reply_to_message_id=reply)
        except: pass
    await asyncio.gather(*[send(a) for a in bot_apps])

async def all_react(chat_id, msg_id):
    await asyncio.gather(*[a.bot.set_message_reaction(chat_id, msg_id, REACT_EMOJI) for a in bot_apps], return_exceptions=True)

async def menu(update, context):
    await update.message.reply_text("""⚔️ DRAGY
/destroy <name>
/attack
/stop
/spam
/gcname <text>
/react <id>
/sudo <id>
/takesudo <id>
/sudolist
/check
/menu""")

async def destroy(update, context):
    global destroy_name, destroy_active
    if not ok(update.effective_user.id): return
    if not context.args: return
    destroy_name = context.args[0]
    destroy_active = True
    asyncio.create_task(destroy_loop(update.effective_chat.id))

async def destroy_loop(chat_id):
    while destroy_active and destroy_name:
        await all_msg(chat_id, stretch(f"{destroy_name} {random.choice(DESTROY_TEXTS)}"))
        await asyncio.sleep(0.1)

async def attack(update, context):
    global attack_id
    if not ok(update.effective_user.id): return
    if not update.message.reply_to_message: return
    attack_id = update.message.reply_to_message.from_user.id

async def stop(update, context):
    global destroy_active, attack_id, gcname_active, spam_active, react_id
    if not ok(update.effective_user.id): return
    destroy_active = attack_id = gcname_active = spam_active = False
    react_id = None

async def spam(update, context):
    global spam_text, spam_active
    if not ok(update.effective_user.id): return
    if not update.message.reply_to_message or not update.message.reply_to_message.text: return
    spam_text = stretch(update.message.reply_to_message.text)
    spam_active = True
    asyncio.create_task(spam_loop(update.effective_chat.id))

async def spam_loop(chat_id):
    while spam_active and spam_text:
        await all_msg(chat_id, spam_text)
        await asyncio.sleep(0.08)

async def gcname(update, context):
    global gcname_text, gcname_active
    if not ok(update.effective_user.id): return
    if not context.args: return
    gcname_text = " ".join(context.args)
    gcname_active = True
    asyncio.create_task(gcname_loop(update.effective_chat.id))

async def gcname_loop(chat_id):
    global nc_index
    while gcname_active and gcname_text:
        tasks = []
        for i, bot in enumerate(bot_apps):
            emoji = NC_EMOJIS[(nc_index + i) % len(NC_EMOJIS)]
            tasks.append(bot.bot.set_chat_title(chat_id, f"{gcname_text} {emoji}"))
        await asyncio.gather(*tasks, return_exceptions=True)
        nc_index += 1
        await asyncio.sleep(1)

async def react(update, context):
    global react_id
    if not ok(update.effective_user.id): return
    if not context.args: return
    react_id = int(context.args[0])

async def sudo(update, context):
    if update.effective_user.id != OWNER_ID: return
    if context.args:
        sudo_users.add(int(context.args[0]))
        save_sudo()

async def takesudo(update, context):
    if update.effective_user.id != OWNER_ID: return
    if context.args:
        uid = int(context.args[0])
        if uid != OWNER_ID: sudo_users.discard(uid)
        save_sudo()

async def sudolist(update, context):
    await update.message.reply_text(f"Sudo: {sudo_users}")

async def check(update, context):
    await all_msg(update.effective_chat.id, "⚡")

async def handler(update, context):
    global attack_id, react_id
    if not update.message or not update.message.from_user: return
    chat_id = update.effective_chat.id
    user_id = update.message.from_user.id
    msg_id = update.message.message_id
    if react_id and user_id == react_id:
        await all_react(chat_id, msg_id)
    if attack_id and user_id == attack_id:
        await all_msg(chat_id, stretch(random.choice(DESTROY_TEXTS)), msg_id)

def main():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(init_bots())
    app = Application.builder().token(TOKENS[0]).build()
    for c in [menu, destroy, attack, stop, spam, gcname, react, sudo, takesudo, sudolist, check]:
        app.add_handler(CommandHandler(c.__name__, c))
    app.add_handler(MessageHandler(filters.ALL, handler))
    app.run_polling(allowed_updates=Update.ALL_TYPES, drop_pending_updates=True)

if __name__ == "__main__":
    main()

