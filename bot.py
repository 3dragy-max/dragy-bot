import asyncio, random
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKENS = [
    "8419753295:AAFnas9X25-FVMlbUmWxmvpENCr-i7HAxTg",
    "8584138389:AAEsopwB_yW5xL8bMnCAp4Kd0FPO4XkYADw",
    "7771656978:AAGsKBEKXO1BtCBXjToFSNpzYmndsr0-BvQ",
    "8078384083:AAGGoYM7Q8QCgefO1OTbDZd8YYFEOhDY43Y",
    "7875735234:AAHNBjTyZtOc7Yw4kVDBSfPB8L_McDoH5YU",
    "8074813042:AAGMVNJuHdU5S39CzeP-wsXOevbxXtQwZoU",
    "7971023306:AAEtBcjBcOMPn5bUP621hvWYu2kEDXDxzoo",
    "8680113020:AAFJ6LpkatbdK6_oloOdie4ukTT7BX9hqR4",
    "8795707975:AAGgIsDRYpDyNsbLWfkJR6jBPg7udoFBvok",
    "8561350618:AAHB1NwsXiTW0froCwn4DJ2BzTf5yi7X5Fc",
]

OWNER_ID = 7783086532
sudo_users = {OWNER_ID}
EMOJIS = ["😂","💀","🔥","🤡","⚡","🎯","💣","☠️","👻","🤬","👊","💢","🗿","💩","🖕","🐶"]

DESTROY = [
    "Kya?? 😂😂\n\n  Teri???😂😂😂\n\n    Maa???? 😂😂😂😂\n\n       Randy????? 😂😂😂😂😂",
    "▒░✍️ teri maa ki chudai me maja aya ▒░✍️",
    "⋆🔭 Shut Up Randike Teri Maa Ki Chudai Enjoy Kr Raha Telescope Se ⋆🔭",
    "Qbnrs uth rndyk pille tery bhen k pait me thuda marun🦧🩴",
    "#bAaP_sE_lAdEgA_pAgAL_⚠️☣️",
    "Clapping kro because तेरी माँ रैंडी है 👏🏻👏🏻👏🏻",
    "LUND LELE",
    "Bhagwan Na Ban Jau Isliye TERI MA Bhi CH0DTA hu",
    "No girl🚫 your mom🚫 My love ♥️",
    "Try maa k saar pe lund marke puncture kar du 😐",
    "ye deykho ghoda🐴 muhh me le lo iska loda",
    "Dm Pe Likho Dragy Daddy Love You So Much 😭🎀",
    "Tare ma ko eagle le jaye 👧🏿",
    "Oi try maa rndy chup",
    "Try maa maar jaye agr ab msg aya Kisi ka toh",
]

destroy_name = None
destroy_active = False
attack_id = None
gcname_text = None
gcname_active = False
spam_text = None
react_id = None

def ok(u): return u in sudo_users

async def all_bots(action, chat_id, **kw):
    async def worker(token):
        try:
            app = Application.builder().token(token).build()
            await app.initialize()
            if action=="msg":
                await app.bot.send_message(chat_id, kw["text"], reply_to_message_id=kw.get("r"))
            elif action=="nc":
                em = random.choice(EMOJIS)
                await app.bot.set_chat_title(chat_id, f"{kw['text']} {em}")
            elif action=="ping":
                await app.bot.get_me()
            await app.shutdown()
        except: pass
    await asyncio.gather(*[worker(t) for t in TOKENS])

async def menu(update, context):
    await update.message.reply_text("""DRAGY

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
    if not context.args: return await update.message.reply_text("/destroy <name>")
    destroy_name = context.args[0]
    destroy_active = True
    await update.message.reply_text(f"Destroy ON: {destroy_name}")

async def attack(update, context):
    global attack_id
    if not ok(update.effective_user.id): return
    if not update.message.reply_to_message: return await update.message.reply_text("Reply to target")
    attack_id = update.message.reply_to_message.from_user.id
    await update.message.reply_text("Attack ON")

async def stop(update, context):
    global destroy_active, attack_id, gcname_active, spam_text, destroy_name
    if not ok(update.effective_user.id): return
    destroy_active = False
    attack_id = None
    gcname_active = False
    spam_text = None
    destroy_name = None
    await update.message.reply_text("Stopped")

async def spam(update, context):
    global spam_text
    if not ok(update.effective_user.id): return
    if not update.message.reply_to_message or not update.message.reply_to_message.text: return
    spam_text = update.message.reply_to_message.text
    await update.message.reply_text("Spam ON")

async def gcname(update, context):
    global gcname_text, gcname_active
    if not ok(update.effective_user.id): return
    if not context.args: return await update.message.reply_text("/gcname <text>")
    gcname_text = " ".join(context.args)
    gcname_active = True
    await update.message.reply_text(f"GC name: {gcname_text}")
    asyncio.create_task(gcname_loop(update.effective_chat.id))

async def gcname_loop(chat_id):
    while gcname_active and gcname_text:
        await all_bots("nc", chat_id, text=gcname_text)
        await asyncio.sleep(3)

async def react(update, context):
    global react_id
    if not ok(update.effective_user.id): return
    if not context.args: return
    react_id = int(context.args[0])
    await update.message.reply_text(f"React ON: {react_id}")

async def sudo(update, context):
    if update.effective_user.id != OWNER_ID: return
    if context.args: sudo_users.add(int(context.args[0])); await update.message.reply_text("Sudo added")

async def takesudo(update, context):
    if update.effective_user.id != OWNER_ID: return
    if context.args: sudo_users.discard(int(context.args[0])); await update.message.reply_text("Sudo removed")

async def sudolist(update, context):
    await update.message.reply_text(str(sudo_users))

async def check(update, context):
    if not ok(update.effective_user.id): return
    await all_bots("ping", update.effective_chat.id)
    await update.message.reply_text("All 10 bots alive ✅")

async def handler(update, context):
    global destroy_active, destroy_name, attack_id, spam_text, react_id
    if not update.message or not update.message.from_user: return
    chat_id = update.effective_chat.id
    user_id = update.message.from_user.id
    msg_id = update.message.message_id

    if react_id and user_id == react_id:
        for t in TOKENS:
            try:
                a = Application.builder().token(t).build()
                await a.initialize()
                await a.bot.set_message_reaction(chat_id, msg_id, "👎")
                await a.shutdown()
            except: pass

    if spam_text:
        await all_bots("msg", chat_id, text=spam_text, r=msg_id)

    if destroy_active and destroy_name:
        text = random.choice(DESTROY)
        if attack_id and user_id == attack_id:
            final = f"{destroy_name} {text}"
        else:
            final = text
        for _ in range(5):
            await all_bots("msg", chat_id, text=final, r=msg_id)
            await asyncio.sleep(0.1)

    elif attack_id and user_id == attack_id and not destroy_active:
        text = random.choice(DESTROY)
        for _ in range(5):
            await all_bots("msg", chat_id, text=text, r=msg_id)
            await asyncio.sleep(0.1)

def main():
    app = Application.builder().token(TOKENS[0]).build()
    app.add_handler(CommandHandler("menu", menu))
    app.add_handler(CommandHandler("destroy", destroy))
    app.add_handler(CommandHandler("attack", attack))
    app.add_handler(CommandHandler("stop", stop))
    app.add_handler(CommandHandler("spam", spam))
    app.add_handler(CommandHandler("gcname", gcname))
    app.add_handler(CommandHandler("react", react))
    app.add_handler(CommandHandler("sudo", sudo))
    app.add_handler(CommandHandler("takesudo", takesudo))
    app.add_handler(CommandHandler("sudolist", sudolist))
    app.add_handler(CommandHandler("check", check))
    app.add_handler(MessageHandler(filters.ALL, handler))
    print("DRAGY ONLINE")
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
