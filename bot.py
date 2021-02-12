from logging import warning
import discord
from discord import channel
from discord import guild
from discord.ext import commands
import asyncio


class MyClient(discord.Client):
    waitingQueue = []
    roomIDs = [809454410543530014, 809454540504039424, 809454553790545950]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # create the background task and run it in the background
        # self.bg_task = self.loop.create_task(self.CSVLoopCheck())

    async def on_ready(self):
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')

    async def check_free_room(self):
        await self.wait_until_ready()
        while not self.is_closed():
            VC = discord.utils.get(channel.VoiceChannel, id=809454410543530014)
            print(VC.members)

    async def on_message(self, message):
        if message.author.id == self.user.id:
            return

        if message.content.startswith("!queue") or message.content.startswith("!q"):
            if not self.waitingQueue.__contains__(message.author):
                if message.author.voice is None:
                    await message.channel.send((message.author.mention + ": Please join ``🔈 waiting-room`` to queue."))
                elif message.author.voice.channel.id == 809454365164568626:
                    self.waitingQueue.append(message.author)
                    await message.add_reaction("✅")
                else:
                    await message.channel.send((message.author.mention + ": Please join ``🔈 waiting-room`` to queue."))
            elif self.waitingQueue.__contains__(message.author):
                await message.delete()

        if message.content.startswith("!pos") or message.content.startswith("!position") or message.content.startswith("!p"):
            if self.waitingQueue.__contains__(message.author):
                await message.channel.send(message.author.mention + ": You are position ``" + str(self.waitingQueue.index(message.author) + 1) + "``.")
            else:
                await message.channel.send((message.author.mention + ": You are not in the queue."))

        if message.content.startswith("!vc"):
            for cID in self.roomIDs:
                if len(self.waitingQueue) == 0:
                    break
                for member in self.waitingQueue:
                    channel = discord.utils.get(message.guild.voice_channels, id=cID)
                    if len(channel.members) < 1:
                        await member.move_to(channel)
                        self.waitingQueue.pop(0)

        if message.content.startswith("!clear"):
            deleted = await message.channel.purge()
            embed=discord.Embed(title="Commands", description="QueueBot Commands", color=0xedcf07)
            embed.add_field(name="!queue / !q", value="Enters you into the queue for labs", inline=False)
            embed.add_field(name="!position / !p", value="Shows current position in the queue", inline=False)
            await message.channel.send(embed=embed)

        if message.content.startswith("!help"):
            embed=discord.Embed(title="Commands", description="QueueBot Commands", color=0xedcf07)
            embed.add_field(name="!queue / !q", value="Enters you into the queue for labs", inline=False)
            embed.add_field(name="!position / !p", value="Shows current position in the queue", inline=False)
            await message.channel.send(embed=embed)


client=MyClient()
ftoken = open("token", "r")
token = ftoken.read().strip("\n")
client.run(token)
