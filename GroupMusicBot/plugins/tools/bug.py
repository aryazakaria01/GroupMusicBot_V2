import os
from typing import Optional

from pyrogram import filters
from pyrogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)
from GroupMusicBot import app1
from config import COMMAND_PREFIXES as cmd, LOG_GROUP_ID


def get_text(message: Message) -> Optional[str]:
    text_to_return = message.text
    if not text_to_return:
        return None
    return " ".join(message.command[1:])


@app1.on_message(filters.command("bug", prefixes=cmd))
async def bug(_, message: Message):
    chat_id = message.chat.id
    memek = await app1.export_chat_invite_link(message.chat.id)
    bugnya = get_text(message)
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    mention = f"[{user_name}](tg://user?id={str(user_id)})"

    if not bugnya:
        await app1.send_message(
            chat_id,
            text="Please provide a description of the bug.",
            disable_web_page_preview=True,
        )
        return
    else:
        await app1.send_message(
            chat_id,
            text="Bug report sent! Thank you for your feedback.",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("Close", callback_data="cls")]]
            ),
        )
        await app1.send_message(
            LOG_GROUP_ID,
            f"📣 New bug report\n\n"
            f"**Chat:** [{message.chat.title}]({memek})\n"
            f"**Name:** {mention}\n"
            f"**User ID:** {message.from_user.id}\n"
            f"**Username:** @{message.from_user.username}\n\n"
            f"**Bug Report:** {bugnya}",
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton("View Message", url=f"{message.link}")],
                    [InlineKeyboardButton("Close", callback_data="cls")],
                ]
            ),
        )
