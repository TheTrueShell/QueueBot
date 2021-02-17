from logging import warning
import discord
from discord import channel
from discord import guild
from discord.ext import commands
import asyncio


class MyClient(discord.Client):
    waitingQueue = [] #Holds all members waiting in the queue
    roomIDs = [809454410543530014, 809454540504039424, 809454553790545950] #The IDs of the Lab "Rooms"
    staffList = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.bg_task = self.loop.create_task(self.loopQueue())

    async def on_ready(self): #Runs on ready
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')
        await self.getStaff()

    async def loopQueue(self):
        await self.wait_until_ready()
        while not self.is_closed():
            for cID in self.roomIDs:
                if len(self.waitingQueue) == 0:
                    break
                for member in self.waitingQueue:
                    channel = discord.utils.get(client.guild.voice_channels, id=cID)
                    if len(channel.members) == 1:
                        for staffmember in channel.members:
                            if self.staffList.__contains__(staffmember):
                                await member.move_to(channel)
                                self.waitingQueue.pop(0)
                await asyncio.sleep(60)

    async def getStaff(self):
        self.staffList.clear()
        for member in self.get_all_members():
            for role in member.roles:
                if str(role) == "Helper" and not self.staffList.__contains__(member):
                    self.staffList.append(member)

    async def checkPermissions(self, message):
        return message.author.id == 618876946830589963
        #Can be made so it checks for a role        

    async def on_message(self, message):
        if message.author.id == self.user.id: #Stops the bot responding to itself
            return

        if message.channel.id != 809454274392227870: #Restrains commands to a single channel
            return

        if message.content.startswith("!queue") or message.content.startswith("!q"): #Queues members
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

        if message.content.startswith("!pos") or message.content.startswith("!position") or message.content.startswith("!p"): #Shows those queued their position
            if self.waitingQueue.__contains__(message.author):
                await message.channel.send(message.author.mention + ": You are position ``" + str(self.waitingQueue.index(message.author) + 1) + "``.")
            else:
                await message.channel.send((message.author.mention + ": You are not in the queue."))

        if message.content.startswith("!vc") and await self.checkPermissions(message): #Temporary command. Will become automatic
            await self.wait_until_ready()
            while not self.is_closed():
                for cID in self.roomIDs:
                    if len(self.waitingQueue) == 0:
                        break
                    for member in self.waitingQueue:
                        channel = discord.utils.get(message.guild.voice_channels, id=cID)
                        if len(channel.members) == 1:
                            for staffmember in channel.members:
                                if self.staffList.__contains__(staffmember):
                                    await member.move_to(channel)
                                    self.waitingQueue.pop(0)
                await asyncio.sleep(60)

        if message.content.startswith("!clear") and await self.checkPermissions(message): #Clears the channel and shows the help dialog box at the start of the channel.
            await message.channel.send("Deleting... Please wait, depending on the number of messages this may take a minute.")
            await message.channel.purge()
            embed=discord.Embed(title="Commands", description="QueueBot Commands", color=0xedcf07)
            embed.add_field(name="!queue / !q", value="Enters you into the queue for labs", inline=False)
            embed.add_field(name="!position / !p", value="Shows current position in the queue", inline=False)
            await message.channel.send(embed=embed)

        if message.content.startswith("!help"): #Shows the help dialogue
            embed=discord.Embed(title="Commands", description="QueueBot Commands", color=0xedcf07)
            embed.add_field(name="!queue / !q", value="Enters you into the queue for labs", inline=False)
            embed.add_field(name="!position / !p", value="Shows current position in the queue", inline=False)
            await message.channel.send(embed=embed)


client=MyClient()
ftoken = open("token", "r") #Reads in the token needed for bot authentication
token = ftoken.read().strip("\n") 
client.run(token)
