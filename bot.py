import asyncio, random, time
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKENS = [
    "8419753295:AAH52EgNfesaapeyCrVsYFTzz2Xk9JSJzSo",
    "8584138389:AAHGe96urO4U_fVh8RcBKXPN9PdDhu7PYAo",
    "7771656978:AAGw2Mi98PspHTEG7xAUVqEjoc2uCX7ttL8",
    "8078384083:AAGMrtoZUB0kS-XPfRqWIYZG7crIvmPaoI8",
    "7875735234:AAGmidhLgTFZLl1XC0GOPEdIwjtaugAxOIw",
    "8074813042:AAFT4n2jDI-Dj1rkWi8rbCtTuLoKTgUuTb8",
    "7971023306:AAE0U6OF74icSjThgkZOLvLOVbTnJpp9Uhw",
    "8680113020:AAHRJhpZsULH0hHZVfQaOrdVT8yc5TsRcek",
    "8795707975:AAF0DtAazSMizJUI5fqYU108mp6fQmetQSo",
    "8561350618:AAGY53rO7A7YOIsZGzW_Uewc8pz36Q1SA3U",
]

OWNER_ID = 7783086532
sudo_users = {OWNER_ID}

EMOJI_SETS = [
    "😂💀🔥🤡⚡🎯💣☠️👻🤬👊💢🗿💩🖕🐶🤯😈👹👺💀🔥⚡🎯💣☠️👻🤬👊💢🗿💩🖕🐶🤯😈👹👺😂💀🔥🤡⚡🎯💣☠️👻🤬👊💢🗿💩🖕🐶🤯😈👹",
    "❤️🧡💛💚🩵💙💜🤎🖤🩶🤍🩷💘💝💖🤎🖤🩶🤍🩷💘💝💖💗💓💞❣️♥️💕💟💌❤️‍🩹💔❤️‍🔥💋🫂❤️💛💚🤎🩵🖤💜🩶💖🩶💘",
    "🙇🙋💁🙆🙅🤷🤦🙍🏃🙎🛌🧏🛀💆🧖💇🧍🤸🧎🧑‍🦼🧑‍🦽🧑‍🦯🧑‍🦯🚶🚶🏃⛹️🤼‍♂️🤾🤼🚴🏋️🧗🚵🤼‍♀️🏌️🏇🤹🤺🏌️🏂🪂",
]

DESTROY_TEXTS = [
    "Kya?? 😂😂\n\n  Teri???😂😂😂\n\n    Maa???? 😂😂😂😂\n\n       Randy????? 😂😂😂😂😂",
    "▒░✍️ teri maa ki chudai me maja aya ▒░✍️",
    "Qbnrs uth rndyk pille tery bhen k pait me thuda marun🦧🩴",
    "LUND LELE",
    "Bhagwan Na Ban Jau Isliye TERI MA Bhi CH0DTA hu",
    "Try maa k saar pe lund marke puncture kar du 😐",
    "𝐒ʜᴜᴛ 𝐔ᴘ 𝐑ᴀɴᴅɪᴋᴇ 𝐓ᴇʀɪ 𝐌ᴀᴀ 𝐊ɪ 𝐂ʜᴜᴅᴀɪ 𝐄ɴᴊᴏʏ 𝐊ʀ",
    "तेरी माँ रैंडी है 👏🏻👏🏻👏🏻",
    "No girl🚫 your mom🚫 My love ♥️",
    "Chup rndyke bche",
    "Try maa rndy chup",
    "tera baap Dragy hai 😂",
    "Gc left le rndyk pille",
    "Stay strong 😹😹💪",
    "Na na Rona ni h",
]

REACT_EMOJI = "🤣"

destroy_name = None
destroy_active = False
attack_id = None
gcname_text = None
gcname_active = False
spam_text = None
spam_active = False
react_id = None
start_time = time.time()

def ok(u): return u in sudo_users

# ⚡ ULTRA FAST ALL BOTS
async def all_bots(chat_id, text, reply=None):
    async def fire(token):
        try:
            a = Application.builder().token(token).build()
            await a.initialize()
            await a.bot.send_message(chat_id, text, reply_to_message_id=reply)
            await a.shutdown()
        except: pass
    await asyncio.gather(*[fire(t) for t in TOKENS])

async def menu(update, context):
    await update.message.reply_text("""⚔️ DRAGY ⚔️
/destroy <name>
/attack
/stop
/spam
/gcname <text>
/react <id>
/sudo <id>
/check
/menu""")

async def destroy(update, context):
    global destroy_name, destroy_active
    if not ok(update.effective_user.id): return
    if not context.args: return
    destroy_name = context.args[0]
    destroy_active = True
    asyncio.create_task(destroy_loop(update.effective_chat.id))
    await update.message.reply_text(f"⚔️ Destroy: {destroy_name}")

async def destroy_loop(chat_id):
    while destroy_active and destroy_name:
        text = random.choice(DESTROY_TEXTS)
        final = f"{destroy_name} {text}"
        await all_bots(chat_id, final)
        await asyncio.sleep(0.15)

async def attack(update, context):
    global attack_id
    if not ok(update.effective_user.id): return
    if not update.message.reply_to_message: return
    attack_id = update.message.reply_to_message.from_user.id
    await update.message.reply_text("🎯 Attack ON")

async def stop(update, context):
    global destroy_active, attack_id, gcname_active, spam_active
    if not ok(update.effective_user.id): return
    destroy_active = attack_id = gcname_active = spam_active = False
    await update.message.reply_text("🛑 All stopped")

async def spam(update, context):
    global spam_text, spam_active
    if not ok(update.effective_user.id): return
    if not update.message.reply_to_message or not update.message.reply_to_message.text: return
    spam_text = update.message.reply_to_message.text
    spam_active = True
    asyncio.create_task(spam_loop(update.effective_chat.id))
    await update.message.reply_text("💣 Spam NON-STOP")

async def spam_loop(chat_id):
    while spam_active and spam_text:
        await all_bots(chat_id, spam_text)
        await asyncio.sleep(0.1)

async def gcname(update, context):
    global gcname_text, gcname_active
    if not ok(update.effective_user.id): return
    if not context.args: return
    gcname_text = " ".join(context.args)
    gcname_active = True
    asyncio.create_task(gcname_loop(update.effective_chat.id))
    await update.message.reply_text(f"🔄 GC: {gcname_text}")

async def gcname_loop(chat_id):
    i = 0
    while gcname_active and gcname_text:
        full = f"{gcname_text} {EMOJI_SETS[i%3]}"
        tasks = []
        for t in TOKENS:
            async def nc(tok=t):
                try:
                    a = Application.builder().token(tok).build()
                    await a.initialize()
                    await a.bot.set_chat_title(chat_id, full)
                    await a.shutdown()
                except: pass
            tasks.append(nc())
        await asyncio.gather(*tasks)
        i += 1
        await asyncio.sleep(1.5)

async def react(update, context):
    global react_id
    if not ok(update.effective_user.id): return
    if not context.args: return
    react_id = int(context.args[0])
    await update.message.reply_text(f"🤣 React: {react_id}")

async def sudo(update, context):
    if update.effective_user.id != OWNER_ID: return
    if context.args: sudo_users.add(int(context.args[0])); await update.message.reply_text("✅ Sudo added")

async def check(update, context):
    await all_bots(update.effective_chat.id, "⚡")
    await update.message.reply_text("✅ All 10 alive")

async def handler(update, context):
    global attack_id, react_id
    if not update.message or not update.message.from_user: return
    chat_id = update.effective_chat.id
    user_id = update.message.from_user.id
    msg_id = update.message.message_id

    if react_id and user_id == react_id:
        for t in TOKENS:
            try:
                a = Application.builder().token(t).build()
                await a.initialize()
                await a.bot.set_message_reaction(chat_id, msg_id, REACT_EMOJI)
                await a.shutdown()
            except: pass

    if attack_id and user_id == attack_id:
        text = random.choice(DESTROY_TEXTS)
        await all_bots(chat_id, text, msg_id)

def main():
    app = Application.builder().token(TOKENS[0]).build()
    for c in [menu, destroy, attack, stop, spam, gcname, react, sudo, check]:
        app.add_handler(CommandHandler(c.__name__, c))
    app.add_handler(MessageHandler(filters.ALL, handler))
    print("DRAGY ONLINE")
    app.run_polling(allowed_updates=Update.ALL_TYPES, drop_pending_updates=True)

if __name__ == "__main__":
    main()

