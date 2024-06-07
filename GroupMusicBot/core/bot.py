import sys
import config

from pyrogram import Client, errors
from pyrogram.enums import ChatMemberStatus, ParseMode

from GroupMusicBot.logging import LOGGER


class GMB(Client):
    def __init__(self):
        LOGGER(__name__).info("Starting Bot...")
        super().__init__(
            name="GroupMusicBot",
            in_memory=True,
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            bot_token=config.BOT_TOKEN,
            parse_mode=ParseMode.HTML,
            max_concurrent_transmissions=7,
        )

    async def start(self):
        await super().start()
        self.id = self.me.id
        self.name = self.me.first_name + " " + (self.me.last_name or "")
        self.username = self.me.username
        self.mention = self.me.mention

        try:
            await self.send_message(
                chat_id=config.LOG_GROUP_ID,
                text=f"<u><b>» {self.mention} bot started :</b><u>\n\nUser ID: <code>{self.id}</code>\nName: {self.name}\nUsername: @{self.username}",
            )
        except (errors.ChannelInvalid, errors.PeerIdInvalid):
            LOGGER(__name__).error(
                "Bot has failed to access the log group/channel. Make sure that you have added your bot to your log group/channel."
            )
            exit()
        except Exception as ex:
            LOGGER(__name__).error(
                f"Bot has failed to access the log group/channel.\nReason: {type(ex).__name__}."
            )
            exit()

        a = await self.get_chat_member(config.LOG_GROUP_ID, self.id)
        if a.status != ChatMemberStatus.ADMINISTRATOR:
            LOGGER(__name__).error(
                "Please promote your bot as an admin in your log group/channel."
            )
            sys.exit()
        LOGGER(__name__).info(f"Music bot started as {self.name}")

    async def stop(self):
        await super().stop()
