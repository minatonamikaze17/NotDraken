import logging 
import os 
from telethon import TelegramClient, events, Button
from telethon.sessions import StringSession
from telethon import errors
from telethon.tl.types import InputMessagesFilterDocument, InputMessagesFilterVideo
from telethon.tl.types import ChannelParticipantsAdmins
import asyncio 

print("Starting....")

#variables 

draken_token = os.environ.get('BOT_TOKEN')
api_id = int(os.environ.get('API_ID'))
api_hash = os.environ.get('API_HASH')
string = os.environ.get('STRING_SESSION')
bot_name = os.environ.get('BOT_NAME', 'NotDraken')

loop = asyncio.get_event_loop()

draken = TelegramClient('bot', api_id, api_hash).start(bot_token=draken_token)

takemichi = TelegramClient(StringSession(string), api_id, api_hash)

if takemichi:
  print("takemichi connected!!")

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level = logging.INFO)

logger = logging.getLogger("__name__")

#commands
admins = []

async def get_all_admins(chat_id):
  async for admin in draken.iter_participants(chat_id, filter=ChannelParticipantsAdmins):
    admins.append(admin.id)

async def user_admin(the_fuc):
  async def check_admin(mikey):
    if slime.sender_id in admins:
      return await the_fuc(mikey)
    else:
      pass

@user_admin
#@draken.on(events.NewMessage(incoming=True,pattern=r'^\/admincache'))
async def admincache(mikey):
  await get_all_admins(mikey.chat_id)
  await mikey.reply('Done!')
  
@draken.on(events.NewMessage(incoming=True,pattern=r'^/search(.*)'))  
@draken.on(events.NewMessage(incoming=True, pattern=r'^#(.*)'))
async def request(mikey):
  chat = -1001167438192
  if mikey.message.text.startswith('/search'):
    try:
      query = mikey.message.text.split(' ', 1)[1]
    except IndexError:
      await mikey.reply('What to search?')
  else:
    query = mikey.message.text[1:]
  if query == '':
    return
  if mikey.reply_to_msg_id:
    mikey = await mikey.get_reply_message()
  keybo = []
  count = 0
  text = ''
  phto = None
  txt = None
  link = None
  keybo = []
  async for message in takemichi.iter_messages(chat, search=query):
    #phto = hek.photo
    txt = message.raw_text.split('|')[0][1:]
    link = f'https://t.me/c/{chat[4:]}/{message.id}'
    keybo.append([Button.url(text=txt, url=link)])
  await mikey.reply(f'Resuluts for {query}', buttons=keybo)
  
  
@draken.on(events.NewMessage(incoming=True, pattern=r'^/start(.*)|/start@DrakenKunRoBot$')) 
async def start(mikey):
  if mikey.is_private:
    await mikey.message.reply(f"Im {bot_name} a bot, \n\nMade for @animebite")
  else:
    await mikey.reply("Im up and working!")


@draken.on(events.InlineQuery)
async def inline_search(mikey):
  if mikey.text == '':
    await mikey.answer([], switch_pm='Search in @animebite', switch_pm_param='start')
  the_text = mikey.text 
  keybo = []
  async for message in takemichi.iter_messages(-1001167438192, search=the_text):
      if len(keybo) > 30:
        await mikey.answer([], switch_pm='Try to be a little specific...', switch_pm_param='')
        return
      msg_id = message.id 
      link = f"https://t.me/c/1167438192/{str(msg_id)}" 
      title = message.raw_text.split('\n\n')[0]
      description = message.raw_text.replace('\n', '|')
      keybo.append(
        mikey.builder.article(
          title=f'{title}',
          description=f'{description}......',
          text=f'{message.text}',
          link_preview=False,
          )
        )
  await mikey.answer(keybo)


print('Im online!!!')

#loop.run_until_complete(get_all_admins(-1001422855927))

takemichi.start()
draken.start()
draken.run_until_disconnected()
takemichi.run_until_disconnected()