import asyncio, random, re, os
from datetime import datetime
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from telegram.error import RetryAfter, TimedOut

# ========== 10 TOKENS ==========
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
dead_bots = set()

EMOJIS = ["😂", "💀", "🔥", "🤡", "🐶", "💩", "⚡", "🎯", "💣", "☠️", "👻", "🤬", "👊", "💢", "🗿"]

DESTROY_TEXTS = [
    "Kya?? 😂😂 \n\n  Teri???😂😂😂\n\n    Maa???? 😂😂😂😂\n\n       Randy????? 😂😂😂😂😂",
    "▒░✍️ ₍ᐢ ᐢ₎ ₍ᐢ•ﻌ•ᐢ₎  ₍˄·͈༝·͈˄₎ ₍⑅ᐢ..ᐢ₎ teri maa ki chudai me maja aya ₍⑅ᐢﻌᐢ⑅₎ ▒░✍️",
    "⋆⭒˚.⋆🔭 𝐒ʜᴜᴛ 𝐔ᴘ 𝐑ᴀɴᴅɪᴋᴇ 𝐓ᴇʀɪ 𝐌ᴀᴀ 𝐊ɪ 𝐂ʜᴜᴅᴀɪ 𝐄ɴᴊᴏʏ 𝐊ʀ 𝐑ᴀʜᴀ 𝐓ᴇʟᴇ𝐒ᴄᴏᴘᴇ 𝐒ᴇ⋆⭒˚.⋆🔭",
    "Qbnrs uth rndyk pille tery bhen k pait me thuda marun🦧🦧🩴🩴",
    "#bAaP_sE_lAdEgA_pAgAL_⚠️☣️",
    "𝗖𝗹𝗮𝗽𝗽𝗶𝗻𝗴 𝗸𝗿𝗼 𝗯𝗲𝗰𝗮𝘂𝘀𝗲 तेरी माँ 𝗿𝗮𝗻𝗱𝘆 𝗵𝗮𝗶 👏🏻👏🏻👏🏻😁😁꙰⃟",
    "꙰⃟ ꙰⃟ ꙰⃟ ꙰⃟ ꙰⃟ ꙰⃟ ꙰⃟ ꙰⃟ ꙰⃟ ꙰⃟ ꙰⃟ ꙰⃟ ꙰⃟ ꙰⃟ ꙰⃟ ꙰⃟.  LUND LELE    ꙰⃟ ꙰⃟ ꙰⃟ ꙰⃟ ꙰⃟ ꙰⃟ ꙰⃟ ꙰⃟ ꙰⃟ ꙰⃟ ꙰⃟ ꙰⃟ ꙰⃟",
    "𝐁ʜᴀɢᴡᴀɴ 𝐍ᴀ 𝐁ᴀɴ 𝐉ᴀᴜ\n𝐈sʟɪʏᴇ TERI MA  𝐁ʜɪ CH0DTA hu",
    "No girl🚫👸🏻your mom🚫𝑀𝑦 𝑙𝑜𝑣𝑒 🌍♥️🫵🏻ᯤ⁹⁹⁹⁺🤴🏻❤️‍🔥⚜️🦅😈⃤",
    "Try maa k saar pe lund marke uska saar puncture kar du rey rndyk pille 😐",
    "ye deykho ghoda🐴 muhh me le lo iska loda",
    "Dm Pe Likho Dragy Daddy Love You So Much 😭🎀🌷",
    "Tare ma ko eagle le jaye 👧🏿",
    "Oi try maa rndy chup",
    "Try maa maar jaye agr ab msg aya Kisi ka toh",
]

destroy_name = None
destroy_active = False
attack_id = None
spam_type = None
spam_content = None
gcname_text = None
gcname_pic = None
react_id = None
apps = []

# ========== PERMS ==========
def ok(uid):
    return uid in sudo_users

# ========== BROADCAST TO ALL BOTS ==========
async def broadcast(action, chat_id, **kwargs):
    """Ek saath sab bots se action"""
    tasks_list = []
    for i, token in enumerate(TOKENS):
        if i in dead_bots:
            continue
        tasks_list.append(single_bot_action(token, action, chat_id, **kwargs))
    await asyncio.gather(*tasks_list, return_exceptions=True)

async def single_bot_action(token, action, chat_id, **kwargs):
    try:
        app = Application.builder().token(token).build()
        await app.initialize()
        if action == "text":
            await app.bot.send_message(chat_id, kwargs["text"], reply_to_message_id=kwargs.get("reply"))
        elif action == "sticker":
            await app.bot.send_sticker(chat_id, kwargs["file_id"], reply_to_message_id=kwargs.get("reply"))
        elif action == "photo":
            await app.bot.send_photo(chat_id, kwargs["file_id"], reply_to_message_id=kwargs.get("reply"))
        elif action == "react":
            await app.bot.set_message_reaction(chat_id, kwargs["msg_id"], "👎")
        elif action == "gcname":
            emoji = random.choice(EMOJIS)
            await app.bot.set_chat_title(chat_id, f"{kwargs['text']} {emoji}")
        elif action == "gcphoto":
            await app.bot.set_chat_photo(chat_id, kwargs["file_id"])
        elif action == "ping":
            await app.bot.get_me()
        await app.shutdown()
    except Exception as e:
        idx = TOKENS.index(token)
        dead_bots.add(idx)

# ========== MENU ==========
async def menu(update, context):
    await update.message.reply_text("""DRAGY COMMANDS

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

# ========== DESTROY ==========
async def destroy(update, context):
    global destroy_name, destroy_active
    if not ok(update.effective_user.id): return await update.message.reply_text("Access denied.")
    if not context.args: return await update.message.reply_text("/destroy <name>")
    destroy_name = context.args[0]
    destroy_active = True
    await update.message.reply_text(f"Destroy ON: {destroy_name}")

# ========== ATTACK ==========
async def attack(update, context):
    global attack_id
    if not ok(update.effective_user.id): return await update.message.reply_text("Access denied.")
    if not update.message.reply_to_message: return await update.message.reply_text("Reply to target.")
    attack_id = update.message.reply_to_message.from_user.id
    await update.message.reply_text("Attack mode ON.")

# ========== STOP ==========
async def stop(update, context):
    global destroy_active, attack_id, spam_type, gcname_text, react_id
    if not ok(update.effective_user.id): return await update.message.reply_text("Access denied.")
    destroy_active = False
    attack_id = None
    spam_type = None
    gcname_text = None
    react_id = None
    destroy_name = None
    await update.message.reply_text("All stopped.")

# ========== SPAM ==========
async def spam(update, context):
    global spam_type, spam_content
    if not ok(update.effective_user.id): return await update.message.reply_text("Access denied.")
    if not update.message.reply_to_message: return await update.message.reply_text("Reply to text/sticker/photo.")
    m = update.message.reply_to_message
    if m.text: spam_type, spam_content = "text", m.text
    elif m.sticker: spam_type, spam_content = "sticker", m.sticker.file_id
    elif m.photo: spam_type, spam_content = "photo", m.photo[-1].file_id
    else: return await update.message.reply_text("Nahi ho payega.")
    await update.message.reply_text("Spam ON.")

# ========== GCNAME ==========
async def gcname(update, context):
    global gcname_text, gcname_pic
    if not ok(update.effective_user.id): return await update.message.reply_text("Access denied.")
    if update.message.reply_to_message and update.message.reply_to_message.photo:
        gcname_pic = update.message.reply_to_message.photo[-1].file_id
        await broadcast("gcphoto", update.effective_chat.id, file_id=gcname_pic)
        await update.message.reply_text("GC photo updated.")
    elif context.args:
        gcname_text = " ".join(context.args)
        await update.message.reply_text(f"GC name loop: {gcname_text}")
        # Start loop
        asyncio.create_task(gcname_loop(update.effective_chat.id))
    else:
        await update.message.reply_text("/gcname <text> or reply to photo")

async def gcname_loop(chat_id):
    while gcname_text:
        await broadcast("gcname", chat_id, text=gcname_text)
        await asyncio.sleep(3)

# ========== REACT ==========
async def react(update, context):
    global react_id
    if not ok(update.effective_user.id): return await update.message.reply_text("Access denied.")
    if not context.args: return await update.message.reply_text("/react <id>")
    react_id = int(context.args[0])
    await update.message.reply_text(f"Reacting to: {react_id}")

# ========== SUDO ==========
async def sudo(update, context):
    if update.effective_user.id != OWNER_ID: return await update.message.reply_text("Owner only.")
    if not context.args: return await update.message.reply_text("/sudo <id>")
    sudo_users.add(int(context.args[0]))
    await update.message.reply_text("Sudo added.")

async def takesudo(update, context):
    if update.effective_user.id != OWNER_ID: return await update.message.reply_text("Owner only.")
    if not context.args: return await update.message.reply_text("/takesudo <id>")
    sid = int(context.args[0])
    if sid != OWNER_ID:
        sudo_users.discard(sid)
    await update.message.reply_text("Sudo removed.")

async def sudolist(update, context):
    await update.message.reply_text(f"Sudo: {sudo_users}")

# ========== CHECK ==========
async def check(update, context):
    if not ok(update.effective_user.id): return await update.message.reply_text("Access denied.")
    dead_bots.clear()
    await broadcast("ping", update.effective_chat.id)
    alive = 10 - len(dead_bots)
    await update.message.reply_text(f"Alive: {alive}/10\nDead: {list(dead_bots)}")

# ========== MESSAGE HANDLER ==========
async def handler(update, context):
    global destroy_active, destroy_name, attack_id, spam_type, spam_content, react_id
    if not update.message or not update.message.from_user: return
    chat_id = update.effective_chat.id
    user_id = update.message.from_user.id
    msg_id = update.message.message_id

    # REACT
    if react_id and user_id == react_id:
        await broadcast("react", chat_id, msg_id=msg_id)

    # SPAM
    if spam_type and spam_content:
        if spam_type == "text":
            await broadcast("text", chat_id, text=spam_content)
        elif spam_type == "sticker":
            await broadcast("sticker", chat_id, file_id=spam_content)
        elif spam_type == "photo":
            await broadcast("photo", chat_id, file_id=spam_content)

    # DESTROY
    if destroy_active and destroy_name:
        text = random.choice(DESTROY_TEXTS)
        if user_id == attack_id:
            final = f"{destroy_name} {text}"
        else:
            final = text
        await broadcast("text", chat_id, text=final, reply=msg_id)

# ========== MAIN ==========
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

