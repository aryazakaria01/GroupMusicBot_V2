import os
from typing import Optional

from pyrogram import filters
from pyrogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)
from GroupMusicBot import userbot
from config import COMMAND_PREFIXES as cmd, LOG_GROUP_ID


def get_text(message: Message) -> Optional[str]:
    text_to_return = message.text
    if message.text is None:
        return None
    if " " not in text_to_return:
        return None
    try:
        return message.text.split(None, 1)[1]
    except IndexError:
        return None


@userbot.on_message(filters.regex(f"^{cmd}bug"))
async def bug(_, message: Message):
    chat_id = message.chat.id
    memek = await app.export_chat_invite_link(message.chat.id)
    bugnya = get_text(message)
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    mention = f"[{user_name}](tg://user?id={str(user_id)})"
    if not bugnya:
        await app.send_message(
            chat_id,
            text=_["bug_spt"],
            disable_web_page_preview=True,
        )
        return
    else:
        await app.send_message(
            chat_id,
            text=_["bug_sended"].format(bugnya),
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton(_["CLOSE_BUTTON"], callback_data="cls")]]
            ),
        )
        await app.send_message(
            LOG_GROUP_ID,
            "📣 New bug reporting\n\n"
            f"**Chat:** [{message.chat.title}]({memek})\n"
            f"**Name:** {mention}\n"
            f"**User ID:** {message.from_user.id}\n"
            f"**Username:** @{message.from_user.username}\n\n"
            f"**Contents of the report:** {bugnya}",
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton(_["bug_btn"], url=f"{message.link}")],
                    [InlineKeyboardButton(_["CLOSE_BUTTON"], callback_data="cls")],
                ]
            ),
        )
