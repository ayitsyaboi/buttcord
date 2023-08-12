from redbot.core import commands
import discord

class Cleanup(commands.Cog):
    """buttcord cog for purging channels"""

    def __init__(self, bot):
        self.bot = bot
    
    #Check for admin perm (confirmed working)
    async def cog_check(self, ctx):
        return ctx.author.guild_permissions.administrator

    @commands.command()
    async def cleanup(self, ctx, limit: int, channel: discord.TextChannel = None):
        """
        **Delete a specified number of messages in a channel.**

        This cog works for members with administrator perm **ONLY**.
        
        Example usage:

        `-cleanup 10 #bot-test` deletes the last 10 messages in #bot-test minus the command message.
        """
        #Channel to purge is channel defined, if not use current channel (ctx.channel = context channel)
        channel = channel or ctx.channel
        #Number of messages to purge defined in async for loop
        messages_to_delete = []
        
        #Set the max messages to delete in a single batch
        max_messages_per_batch = 100

        #Loop through multiple batches if necessary
        while limit > 0:
            batch_limit = min(limit, max_messages_per_batch)
            
            #Loop through messages in the current batch
            async for message in channel.history(limit=batch_limit + 1):
                #If the messages are not the command message, delete them
                if message != ctx.message:
                    messages_to_delete.append(message)
            
            #Subtract the processed messages from the remaining limit
            limit -= batch_limit

        #Check for messages
        if messages_to_delete:
            await channel.delete_messages(messages_to_delete)
            #Sends a message saying Deleted x messages (this is obvious but whatever)
            await ctx.send(f"Deleted {len(messages_to_delete)} messages.")
        #If the channel is empty of non-command context msgs, then
        else:
            await ctx.send("No messages to delete.")

