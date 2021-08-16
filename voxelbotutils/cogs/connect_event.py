from datetime import datetime as dt
from time import time

import discord

from . import utils


def try_id(item):
    """
    Try and get the ID from an item, otherwise returning None.
    """

    try:
        return item.id
    except AttributeError:
        return None


def try_username(bot):
    try:
        return bot.user.name
    except Exception:
        return bot.application_id


class ConnectEvent(utils.Cog):

    async def send_webhook(self, event_name: str, text: str, username: str, logger: str) -> bool:
        """
        Send a webhook to the bot specified event webhook url.
        """

        event_webhook: discord.Webhook = self.bot.get_event_webhook(event_name)
        if not event_webhook:
            return False
        try:
            avatar_url = str(self.bot.user.avatar_url)
        except Exception:
            avatar_url = None
        try:
            await event_webhook.send(
                text,
                username=username,
                avatar_url=avatar_url,
                allowed_mentions=discord.AllowedMentions.none(),
            )
        except discord.HTTPException as e:
            self.logger.error(f"Failed to send webhook for event {event_name} - {e}")
            return False
        except Exception as e:
            self.logger.error(e)
            raise e
            return False
        self.logger.info(logger)
        return True

    @utils.Cog.listener()
    async def on_shard_connect(self, shard_id: int):
        """
        Ping a given webhook when the shard ID is connected.
        """

        application_id = self.bot.application_id
        await self.send_webhook(
            "shard_connect",
            f"Shard connect event just pinged for shard ID `{shard_id}` - <t:{int(time())}>",
            f"{try_username(self.bot)} - Shard Connect",
            f"Sent webhook for on_shard_connect event in shard `{shard_id}`",
        )

    @utils.Cog.listener()
    async def on_shard_ready(self, shard_id: int):
        """
        Ping a given webhook when the shard ID becomes ready.
        """

        application_id = self.bot.application_id
        await self.send_webhook(
            "shard_ready",
            f"Shard ready event just pinged for shard ID `{shard_id}` - <t:{int(time())}>",
            f"{try_username(self.bot)} - Shard Ready",
            f"Sent webhook for on_shard_ready event in shard `{shard_id}`",
        )

    @utils.Cog.listener()
    async def on_ready(self):
        """
        Ping a given webhook when the bot becomes ready.
        """

        application_id = self.bot.application_id
        await self.send_webhook(
            "bot_ready",
            f"Bot ready event just pinged for instance with shards `{self.bot.shard_ids}` - <t:{int(time())}>",
            f"{try_username(self.bot)} - Ready",
            "Sent webhook for on_ready event",
        )

    @utils.Cog.listener()
    async def on_shard_disconnect(self, shard_id: int):
        """
        Ping a given webhook when the shard ID is disconnected.
        """

        application_id = self.bot.application_id
        await self.send_webhook(
            "shard_disconnect",
            f"Shard disconnect event just pinged for shard ID `{shard_id}` - <t:{int(time())}>",
            f"{try_username(self.bot)} - Shard Disconnect",
            f"Sent webhook for on_shard_disconnect event in shard `{shard_id}`",
        )

    @utils.Cog.listener()
    async def on_disconnect(self):
        """
        Ping a given webhook when the bot is disconnected.
        """

        application_id = self.bot.application_id
        await self.send_webhook(
            "bot_disconnect",
            f"Bot disconnect event just pinged for instance with shards `{self.bot.shard_ids or [0]}` - <t:{int(time())}>",
            f"{try_username(self.bot)} - Disconnect",
            "Sent webhook for on_disconnect event",
        )

    @utils.Cog.listener()
    async def on_shard_resumed(self, shard_id: int):
        """
        Ping a given webhook when the shard ID is resumed.
        """

        application_id = self.bot.application_id
        await self.send_webhook(
            "shard_connect",
            f"Shard resumed event just pinged for shard ID `{shard_id}` - <t:{int(time())}>",
            f"{try_username(self.bot)} - Shard Resumed",
            f"Sent webhook for on_shard_resumed event in shard `{shard_id}`",
        )

    @utils.Cog.listener()
    async def on_resumed(self):
        """
        Ping a given webhook when the bot is resumed.
        """

        application_id = self.bot.application_id
        await self.send_webhook(
            "bot_connect",
            f"Bot resumed event just pinged for instance with shards `{self.bot.shard_ids or [0]}` - <t:{int(time())}>",
            f"{try_username(self.bot)} - Resumed",
            "Sent webhook for on_resumed event",
        )

    @utils.Cog.listener()
    async def on_guild_join(self, guild: discord.Guild):
        """
        Ping a given webhook when the bot is added to a guild.
        """

        application_id = self.bot.application_id
        await self.send_webhook(
            "guild_join",
            f"Added to new guild - ``{guild.name}``/``{guild.id}`` (`{guild.member_count}` members)",
            f"{try_username(self.bot)} - Guild Join",
            "Sent webhook for on_guild_join event",
        )

    @utils.Cog.listener()
    async def on_guild_remove(self, guild: discord.Guild):
        """
        Ping a given webhook when the bot is removed from a guild.
        """

        application_id = self.bot.application_id
        if guild.me:
            try:
                member_count = guild.member_count
                text = f"Removed from guild - ``{guild.name}``/``{guild.id}`` (`{member_count}` members; `{utils.TimeValue((dt.utcnow() - guild.me.joined_at).total_seconds()).clean_full}` guild duration) - <t:{int(time())}>"
            except Exception:
                text = f"Removed from guild - ``{guild.name}``/``{guild.id}`` (`{utils.TimeValue((dt.utcnow() - guild.me.joined_at).total_seconds()).clean_full}` guild duration) - <t:{int(time())}>"
            await self.send_webhook(
                "guild_remove",
                text,
                f"{try_username(self.bot)} - Guild Remove",
                "Sent webhook for on_guild_remove event",
            )
        else:
            try:
                member_count = guild.member_count
                text = f"Removed from guild - ``{guild.name}``/``{guild.id}`` (`{member_count}` members)"
            except Exception:
                text = f"Removed from guild - ``{guild.name}``/``{guild.id}``"
            await self.send_webhook(
                "guild_remove",
                text,
                f"{try_username(self.bot)} - Guild Remove",
                "Sent webhook for on_guild_remove event",
            )


def setup(bot: utils.Bot):
    x = ConnectEvent(bot)
    bot.add_cog(x)
