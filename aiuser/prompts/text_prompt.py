import logging
import re
from typing import Optional

from discord import Message

from aiuser.common.constants import MAX_MESSAGE_LENGTH, MIN_MESSAGE_LENGTH
from aiuser.prompts.base import Prompt
from aiuser.prompts.common.helpers import format_text_content
from aiuser.prompts.common.messagethread import MessageThread

logger = logging.getLogger("red.bz_cogs.aiuser")


class TextPrompt(Prompt):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def _handle_message(self) -> Optional[MessageThread]:
        if not self._is_acceptable_message(self.message):
            return None

        await self.messages.add_msg(format_text_content(self.message), self.message)

        return self.messages

    @staticmethod
    def _is_acceptable_message(message: Message) -> bool:
        mention_pattern = re.compile(r'^<@!?&?(\d+)>$')

        if not message.content:
            logger.debug(f"Skipping empty message {message.id} in {message.guild.name}")
            return False

        if mention_pattern.match(message.content):
            logger.debug(f"Skipping singular mention message {message.id} in {message.guild.name}")
            return False

        if len(message.content) < MIN_MESSAGE_LENGTH:
            logger.debug(
                f"Skipping short message {message.id} in {message.guild.name}")
            return False

        if len(message.content.split()) > MAX_MESSAGE_LENGTH:
            logger.debug(
                f"Skipping long message {message.id} in {message.guild.name}")
            return False

        return True