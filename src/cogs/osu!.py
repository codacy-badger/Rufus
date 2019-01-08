""" osu! -- rufus.py """
import config as c
import os.path
import requests
from discord.ext import commands


class osu:
    """ osu! commands """

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def o_user(self, username, mode='osu!'):
        """ Get osu! user information.
        """
        if mode == 'osu!':
            mode = 0
        elif mode == 'taiko':
            mode = 1
        elif mode == 'ctb':
            mode = 2
        elif mode == 'mania':
            mode = 3
        URL = 'https://osu.ppy.sh/api/get_user?k={}&m={}&u={}'.format(c.osu_api_key, mode, username)
        DATA = requests.get(URL).json()
        JOIN_DATE = DATA[0]['join_date']
        await self.bot.say(JOIN_DATE)

    @commands.command(pass_context=True)
    async def skin(self, ctx):
        """ current osu! skin.
            Deprecated because docker.
        """
        osu=str("C:\\Users\\{}\\AppData\\Local\\osu!".format(getpass.getuser()))
        f=open(osu+"\\Logs\\runtime.log", "r")
        for line in f:
            line=line.replace("\\", "\\\\")
            if "skin.ini" in line:
                skin=line.split("\\\\skin.ini", 1)[0].split('Skins\\', 1)[-1]
        msg = await self.bot.say("``zipping {}...``".format(skin))
        path = (os.path.dirname(os.path.realpath(__file__)))
        shutil.make_archive(path+"\\temp\\"+skin, 'zip', osu+"\\Skins\\"+skin)
        await self.bot.edit_message(msg, "``{} zipped, getting ready for upload!``".format(skin))
        try:
            await self.bot.send_file(ctx.message.channel, path+"\\temp\\"+skin+".zip")
            await self.bot.edit_message(msg, "``{} uploaded!``".format(skin))
        except:
            await self.bot.edit_message(msg, "``Yikes! The skin file was too large to send, sorry about that.``")
        finally:
            filelist = [ f for f in os.listdir(path+"\\temp") if f.endswith(".zip") ]
            for f in filelist:
                os.remove(os.path.join(path+"\\temp", f))


def setup(bot):
    """ defines setup """
    bot.add_cog(osu(bot))
