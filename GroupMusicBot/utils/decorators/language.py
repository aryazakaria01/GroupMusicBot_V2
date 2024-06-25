from GroupMusicBot.config import SUPPORT_GROUP
from strings import get_string

from GroupMusicBot import app
from GroupMusicBot.misc import SUDOERS
from GroupMusicBot.utils.database import get_lang, is_maintenance

def language(mystic):
    async def wrapper(_, message, **kwargs):
        if await is_maintenance() is False:
            if message.from_user.id not in SUDOERS:
                return await message.reply_text(
                    text=f"{app.mention} is under maintenance, visit <a href={SUPPORT_GROUP}>support chat</a> for knowing the reason.",
                    disable_web_page_preview=True,
                )
        try:
            await message.delete()
        except(ValueError, AttributeError):
            pass

        try:
            language = await get_lang(message.chat.id)
            language = get_string(language)
        except(ValueError, AttributeError):
            language = get_string("en")
        return await mystic(_, message, language)

    return wrapper


def languageCB(mystic):
    async def wrapper(_, CallbackQuery, **kwargs):
        if await is_maintenance() is False:
            if CallbackQuery.from_user.id not in SUDOERS:
                return await CallbackQuery.answer(
                    f"{app.mention} ɪis under maintenance, visit support chat for knowing the reason.",
                    show_alert=True,
                )
        try:
            language = await get_lang(CallbackQuery.message.chat.id)
            language = get_string(language)
        except(ValueError, AttributeError):
            language = get_string("en")
        return await mystic(_, CallbackQuery, language)

    return wrapper


def LanguageStart(mystic):
    async def wrapper(_, message, **kwargs):
        try:
            language = await get_lang(message.chat.id)
            language = get_string(language)
        except(ValueError, AttributeError):
            language = get_string("en")
        return await mystic(_, message, language)

    return wrapper
