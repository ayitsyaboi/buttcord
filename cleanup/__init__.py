from .cleanup import Cleanup


async def setup(bot):
    await bot.add_cog(Cleanup(bot))