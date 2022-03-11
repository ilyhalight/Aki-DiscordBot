import aiohttp
import urllib.parse as ul


from datetime import datetime, timedelta
from core.bot import bot

class DiscordRequest():

    def __init__(self, bot):
        self.bot = bot

    bot.session = aiohttp.ClientSession()

    async def user_timeout(user_id: int, guild_id: int, until, reason: str = None):
        if reason is not None:
            headers = {
                "Authorization": f"Bot {bot.http.token}",
                "X-Audit-Log-Reason": ul.quote_plus(reason)
            }
        else:
            headers = {
                "Authorization": f"Bot {bot.http.token}"
            }
        url = f"https://discord.com/api/v9/guilds/{guild_id}/members/{user_id}"
        if type(until) is int:
            timeout = (datetime.utcnow() + timedelta(minutes = until)).isoformat()
        else:
            timeout = None
        json = {'communication_disabled_until': timeout}
        async with bot.session.patch(url, json = json, headers = headers) as session:
            if session.status in range(200, 299):
                return True
            return False