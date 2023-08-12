from redbot.core import commands

class testing(commands.Cog):
    """base template for creating a new cog because I am dumb"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def test(self, ctx):
        """description goes here"""
        # Your code will go here
        await ctx.send("this means it worked, congrats idiot")