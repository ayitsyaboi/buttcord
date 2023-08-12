import logging
import re
from typing import Optional

import aiohttp

from aiuser.prompts.base import Prompt
from aiuser.prompts.common.messagethread import MessageThread

logger = logging.getLogger("red.bz_cogs.aiuser")


class YoutubeLinkPrompt(Prompt):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def _handle_message(self) -> Optional[MessageThread]:
        self.api_key = (await self.bot.get_shared_api_tokens("youtube")).get("api_key")
        video_id = await self._get_video_id(self.message.content)
        author = self.message.author.nick or self.message.author.name

        if not video_id:
            return None

        video_title, channel_title, description = await self._get_video_details(video_id)
        if not video_title or not channel_title or not description:
            return None

        remaining_message = self.remove_youtube_links(self.message.content)

        if remaining_message:
            await self.messages.add_msg(f'User "{author}" said: {remaining_message}', self.message)

        await self.messages.add_msg(f'User "{author}" sent: [Link to Youtube video with title "{video_title}" and description "{description}" from channel "{channel_title}"]', self.message, force=True)

        return self.messages

    def remove_youtube_links(self, string):
        youtube_regex = r'(?:https?:\/\/)?(?:www\.)?(?:youtube\.com|youtu\.be)\/(?:watch\?v=)?([^\s&]+)(?:&t=[^\s&]+)?'
        result = re.sub(youtube_regex, '', string)
        return result

    async def _get_video_details(self, video_id):
        url = f"https://www.googleapis.com/youtube/v3/videos?part=snippet&id={video_id}&key={self.api_key}"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    video_data = await response.json()
                    snippet = video_data["items"][0]["snippet"]
                    video_title = snippet["title"]
                    channel_title = snippet["channelTitle"]
                    description = snippet["description"]
                    return (video_title, channel_title, description)
                else:
                    logger.warning("Request to Youtube API failed with status code:", response.status)
                    return (None, None, None)

    async def _get_video_id(self, url):
        pattern = r"(?:youtube(?:-nocookie)?\.com\/(?:[^\/\n\s]+\/\S+\/|(?:v|e(?:mbed)?)\/|\S*?[?&]v=)|youtu\.be\/|v\/|t\/\S*?\/?)([a-zA-Z0-9_-]{11})"
        match = re.search(pattern, url)

        if match:
            video_id = match.group(1)
            return video_id
        else:
            return None
