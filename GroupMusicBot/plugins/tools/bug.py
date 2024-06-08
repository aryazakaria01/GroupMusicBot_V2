from config import API_ID, API_HASH, BOT_TOKEN
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

app1 = Client(
    name="group",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    in_memory=True,
)

@app1.on_message(filters.command("bug") & filters.me)
async def bug(_, message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    mention = f"[{user_name}](tg://user?id={user_id})"

    # Extracting bug description from message
    bug_description = message.text.split(maxsplit=1)[1] if len(message.text.split()) > 1 else None

    if not bug_description:
        await message.reply_text("Please provide a description of the bug.")
        return

    # Sending confirmation message to user
    await message.reply_text("Bug report sent! Thank you for your feedback.",
                             reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Close", callback_data="cls")]]))

    # Sending bug report to log group
    log_message = (f"📣 New bug report\n\n"
                   f"**Chat:** {message.chat.title}\n"
                   f"**Name:** {mention}\n"
                   f"**User ID:** {user_id}\n"
                   f"**Username:** @{message.from_user.username}\n\n"
                   f"**Bug Report:** {bug_description}")
    await app1.send_message(LOG_GROUP_ID, log_message,
                            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("View Message", url=message.link)],
                                                              [InlineKeyboardButton("Close", callback_data="cls")]]))
