from .testing import testing


async def setup(bot):
    await bot.add_cog(testing(bot))