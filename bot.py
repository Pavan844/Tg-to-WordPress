import pyrogram
from pyrogram import Client
from pyrogram import filters
import requests
import os
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup

app = Client(
    "Jones",
    api_id=apiid,
    api_hash="apihash",
    bot_token="Bot Token"
)


WELCOME_PHOTO = "welcome.jpeg"

key = InlineKeyboardMarkup(
    [
        [InlineKeyboardButton("🌐 Website", url="https://yoururl.com")]
    ]
)

replykey=ReplyKeyboardMarkup(
                [
                    ["start⚡️", "help📚"],
                    ["DC⚗️"],
                    ["🌐website"]
                ],
                resize_keyboard=True
            )

@app.on_message(filters.command("start") | filters.regex("start⚡️"))
def start(bot, message):
    WELCOME_MSG = (
        f"Hey {message.from_user.first_name}!,\n"
        "Welcome to our bot! I can Generate Files, Videos, Photos, Audio, Text to Link.\n"
        "To get started, Send or Forward Anything to me.\n\n"
        "If you want to see what people have uploaded then click on the website button in Menu."
    )

    bot.send_photo(
        chat_id=message.chat.id,
        photo=WELCOME_PHOTO,
        caption=WELCOME_MSG,
        reply_markup=replykey,
    )

webphoto = "website.jpeg"

@app.on_message(filters.command("website") | filters.regex("🌐website"))
def start(bot, message):
    webmessage = (
        f"Hey {message.from_user.first_name}!,\n"
        "We have created this bot so that you can share your files easily. If you want to see which files people are sharing and you want to get some ideas from them or you want to see them then you can see the sharing website.\n"
        "Sharing Website: https://yoururl.com .\n\n"
        "You can open it directly by clicking on the button below."
    )
    bot.send_photo(
        chat_id=message.chat.id,
        photo=webphoto,
        caption=webmessage,
        reply_markup=key,
    )

keyhelp = InlineKeyboardMarkup(
    [
        [InlineKeyboardButton("Channel", url="https://t.me/yourchannel")],
        [InlineKeyboardButton("Support Group", url="https://t.me/yourgroup")]
    ]
)


helpphoto = "help.png"

@app.on_message(filters.command("help") | filters.regex("help📚"))
def start(bot, message):
    helpmessage = (
        f"Hey {message.from_user.first_name}!,\n"
        "The main function of this bot is to generate files, videos and posts in links so that you can stream them easily.\n"
        "We also provide you support, which you can access by joining our channel and group and tell us about your problems and bugs.\n\n"
        "Click Below Button Join Channel & Support Group."
    )
    bot.send_photo(
        chat_id=message.chat.id,
        photo=helpphoto,
        caption=helpmessage,
        reply_markup=keyhelp,
    )
    
@app.on_message(filters.command("dc") | filters.regex("DC⚗️"))
def start(bot, message):

    dcid = message.chat.dc_id
    bot.send_message(
        chat_id=message.chat.id,
        text=f"Your Telegram Account DC ID is: {dcid}"
    )

@app.on_message(filters.command("status") | filters.regex("status📊"))
def start(bot, message):

    bot.send_message(
        chat_id=message.chat.id,
        text=f"Your Telegram Account DC ID is: {dcid}"
    )
    
@app.on_message(filters.private)
def download_and_create(client, message):
    if message.text:
       print("Text Found")
       text = message.text
       lines = text.split('\n')
       title = lines[0]
       def createPost(auth_username, auth_password, text, title):
          post_data = {
           'title': title,
           'content': text,
           'status': 'publish'
       }

          api_url = 'https://yoururl.com/wp-json/wp/v2/posts'
          response = requests.post(api_url, data=post_data, auth=(auth_username, auth_password))

          post_url = response.json().get('link')
          print(f'Post URL: {post_url}')
          return post_url

       auth_username = 'username'
       auth_password = 'password'
       post_url = createPost(auth_username, auth_password, text, title)
       reply = (
          "𝗬𝗼𝘂𝗿 𝗟𝗶𝗻𝗸 𝗚𝗲𝗻𝗲𝗿𝗮𝘁𝗲𝗱 !\n\n"
          f"📂 Title : {title}\n\n"
          f"📦 Text : {text}\n\n"
          f"📦 Post Link : {post_url}\n\n"
          "🚸 Nᴏᴛᴇ : LINK WON'T EXPIRE TILL I DELETE"
       )

       keyboard = InlineKeyboardMarkup(
           [
               [
                   InlineKeyboardButton("📦 Post Link", url=f"{post_url}"),
                   InlineKeyboardButton("🌐 Website Link", url="https://yoururl.com")
               ]
           ]
       )

       message.reply(reply, disable_web_page_preview=True, reply_markup=keyboard)
    
    elif message.caption:
       print("Caption Found")
       print(message.media)
       typefile = str(message.media)
       if typefile == "MessageMediaType.VIDEO":
          file_path = message.download()
          file_name = os.path.basename(file_path)
          file_size_bytes = os.path.getsize(file_path)
          file_size_mib = file_size_bytes / (1024 ** 2)
          text = message.caption
          lines = text.split('\n')
          title = lines[0]
          def restMediaUL(filePath, auth_username, auth_password):
              url = 'https://yoururl.com/wp-json/wp/v2/media'
              data = open(filePath, 'rb').read()
              fileName = os.path.basename(filePath)
              file_extension = os.path.splitext(filePath)[1]

              headers = {'Content-Type': f'video/{file_extension[1:]}', 'Content-Disposition': f'attachment; filename={fileName}'}
    
              res = requests.post(url=url, data=data, headers=headers, auth=(auth_username, auth_password))
    
              newDict = res.json()
              newID = newDict.get('id')
              link = newDict.get('guid').get("rendered")
              print(newID, link)
              return newID, link

          def createPost(auth_username, auth_password, text, title):
              post_data = {
                  'title': title,
                  'content': text,
                  'status': 'publish'
              }

              filePath = file_path
              file_id, file_link = restMediaUL(filePath, auth_username, auth_password)
              
              file_extension = os.path.splitext(filePath)[1]

              post_data['content'] = f'<video width="640" height="360" controls><source src="{file_link}" type="video/{file_extension[1:]}"></video>' + post_data['content']

              api_url = 'https://yoururl.com/wp-json/wp/v2/posts'
              response = requests.post(api_url, data=post_data, auth=(auth_username, auth_password))

              post_url = response.json().get('link')
              print(f'Post URL: {post_url}')
              return post_url, file_link  # Returning both post_url and file_link
          auth_username = 'username'
          auth_password = 'password'
          post_url, file_link = createPost(auth_username, auth_password, text, title)


          reply = (
           "𝗬𝗼𝘂𝗿 𝗟𝗶𝗻𝗸 𝗚𝗲𝗻𝗲𝗿𝗮𝘁𝗲𝗱 !\n\n"
           f"📂 Fɪʟᴇ ɴᴀᴍᴇ : {file_name}\n\n"
           f"📦 Fɪʟᴇ ꜱɪᴢᴇ : {file_size_mib:.2f} MiB\n\n"
           f"📥 Dᴏᴡɴʟᴏᴀᴅ : {file_link}\n\n"
           f"🖥 WATCH  : {post_url}\n\n"
           "🚸 Nᴏᴛᴇ : LINK WON'T EXPIRE TILL I DELETE"
          )
          keyboard = InlineKeyboardMarkup(
             [
                [
                   InlineKeyboardButton("🖥 WATCH", url=f"{post_url}"),
                   InlineKeyboardButton("📥 Dᴏᴡɴʟᴏᴀᴅ", url=f"{file_link}")
                ]
             ]
          )
          message.reply(reply, disable_web_page_preview=True, reply_markup=keyboard)
          os.remove(file_path)
       elif typefile == "MessageMediaType.PHOTO":
          file_path = message.download()
          file_name = os.path.basename(file_path)
          file_size_bytes = os.path.getsize(file_path)
          file_size_mib = file_size_bytes / (1024 ** 2)
          text = message.caption
          lines = text.split('\n')
          title = lines[0]
          def restMediaUL(filePath, auth_username, auth_password):
              url = 'https://yoururl.com/wp-json/wp/v2/media'
              data = open(filePath, 'rb').read()
              fileName = os.path.basename(filePath)
              file_extension = os.path.splitext(filePath)[1]

              headers = {'Content-Type': f'image/{file_extension[1:]}', 'Content-Disposition': f'attachment; filename={fileName}'}
    
              res = requests.post(url=url, data=data, headers=headers, auth=(auth_username, auth_password))
    
              newDict = res.json()
              newID = newDict.get('id')
              link = newDict.get('guid').get("rendered")
              print(newID, link)
              return newID, link

          def createPost(auth_username, auth_password, text, title):
              post_data = {
                  'title': title,
                  'content': text,
                  'status': 'publish'
              }

              filePath = file_path
              file_id, file_link = restMediaUL(filePath, auth_username, auth_password)
              file_extension = os.path.splitext(filePath)[1]
              post_data['content'] = f'<img src="{file_link}" alt="{file_name}">' + post_data['content']

              api_url = 'https://yoururl.com/wp-json/wp/v2/posts'
              response = requests.post(api_url, data=post_data, auth=(auth_username, auth_password))

              post_url = response.json().get('link')
              print(f'Post URL: {post_url}')
              return post_url, file_link  # Returning both post_url and file_link
          auth_username = 'username'
          auth_password = 'password'
          post_url, file_link = createPost(auth_username, auth_password, text, title)


          reply = (
           "𝗬𝗼𝘂𝗿 𝗟𝗶𝗻𝗸 𝗚𝗲𝗻𝗲𝗿𝗮𝘁𝗲𝗱 !\n\n"
           f"📂 Fɪʟᴇ ɴᴀᴍᴇ : {file_name}\n\n"
           f"📦 Fɪʟᴇ ꜱɪᴢᴇ : {file_size_mib:.2f} MiB\n\n"
           f"📥 Dᴏᴡɴʟᴏᴀᴅ : {file_link}\n\n"
           f"🖥 WATCH  : {post_url}\n\n"
           "🚸 Nᴏᴛᴇ : LINK WON'T EXPIRE TILL I DELETE"
          )
          keyboard = InlineKeyboardMarkup(
             [
                [
                   InlineKeyboardButton("🖥 WATCH", url=f"{post_url}"),
                   InlineKeyboardButton("📥 Dᴏᴡɴʟᴏᴀᴅ", url=f"{file_link}")
                ]
             ]
          )
          message.reply(reply, disable_web_page_preview=True, reply_markup=keyboard)
          os.remove(file_path)
       elif typefile == "MessageMediaType.AUDIO":
          file_path = message.download()
          file_name = os.path.basename(file_path)
          file_size_bytes = os.path.getsize(file_path)
          file_size_mib = file_size_bytes / (1024 ** 2)
          text = message.caption
          lines = text.split('\n')
          title = lines[0]
          def restMediaUL(filePath, auth_username, auth_password):
              url = 'https://yoururl.com/wp-json/wp/v2/media'
              data = open(filePath, 'rb').read()
              fileName = os.path.basename(filePath)
              file_extension = os.path.splitext(filePath)[1]

              headers = {'Content-Type': f'audio/{file_extension[1:]}', 'Content-Disposition': f'attachment; filename={fileName}'}
    
              res = requests.post(url=url, data=data, headers=headers, auth=(auth_username, auth_password))
    
              newDict = res.json()
              newID = newDict.get('id')
              link = newDict.get('guid').get("rendered")
              print(newID, link)
              return newID, link

          def createPost(auth_username, auth_password, text, title):
              post_data = {
                  'title': title,
                  'content': text,
                  'status': 'publish'
              }

              filePath = file_path
              file_id, file_link = restMediaUL(filePath, auth_username, auth_password)
              file_extension = os.path.splitext(filePath)[1]
              post_data['content'] = f'<audio controls><source src="{file_link}" type="audio/{file_extension[1:]}"></audio>' + post_data['content']

              api_url = 'https://yoururl.com/wp-json/wp/v2/posts'
              response = requests.post(api_url, data=post_data, auth=(auth_username, auth_password))

              post_url = response.json().get('link')
              print(f'Post URL: {post_url}')
              return post_url, file_link  # Returning both post_url and file_link
          auth_username = 'username'
          auth_password = 'password'
          post_url, file_link = createPost(auth_username, auth_password, text, title)


          reply = (
           "𝗬𝗼𝘂𝗿 𝗟𝗶𝗻𝗸 𝗚𝗲𝗻𝗲𝗿𝗮𝘁𝗲𝗱 !\n\n"
           f"📂 Fɪʟᴇ ɴᴀᴍᴇ : {file_name}\n\n"
           f"📦 Fɪʟᴇ ꜱɪᴢᴇ : {file_size_mib:.2f} MiB\n\n"
           f"📥 Dᴏᴡɴʟᴏᴀᴅ : {file_link}\n\n"
           f"🖥 WATCH  : {post_url}\n\n"
           "🚸 Nᴏᴛᴇ : LINK WON'T EXPIRE TILL I DELETE"
          )
          keyboard = InlineKeyboardMarkup(
             [
                [
                   InlineKeyboardButton("🖥 WATCH", url=f"{post_url}"),
                   InlineKeyboardButton("📥 Dᴏᴡɴʟᴏᴀᴅ", url=f"{file_link}")
                ]
             ]
          )
          message.reply(reply, disable_web_page_preview=True, reply_markup=keyboard)
          os.remove(file_path)
       elif typefile == "MessageMediaType.VOICE":
          file_path = message.download()
          file_name = os.path.basename(file_path)
          file_size_bytes = os.path.getsize(file_path)
          file_size_mib = file_size_bytes / (1024 ** 2)
          text = message.caption
          lines = text.split('\n')
          title = lines[0]
          def restMediaUL(filePath, auth_username, auth_password):
              url = 'https://yoururl.com/wp-json/wp/v2/media'
              data = open(filePath, 'rb').read()
              fileName = os.path.basename(filePath)
              file_extension = os.path.splitext(filePath)[1]

              headers = {'Content-Type': f'audio/{file_extension[1:]}', 'Content-Disposition': f'attachment; filename={fileName}'}
    
              res = requests.post(url=url, data=data, headers=headers, auth=(auth_username, auth_password))
    
              newDict = res.json()
              newID = newDict.get('id')
              link = newDict.get('guid').get("rendered")
              print(newID, link)
              return newID, link

          def createPost(auth_username, auth_password, text, title):
              post_data = {
                  'title': title,
                  'content': text,
                  'status': 'publish'
              }

              filePath = file_path
              file_id, file_link = restMediaUL(filePath, auth_username, auth_password)
              file_extension = os.path.splitext(filePath)[1]
              post_data['content'] = f'<audio controls><source src="{file_link}" type="audio/{file_extension[1:]}"></audio>' + post_data['content']

              api_url = 'https://yoururl.com/wp-json/wp/v2/posts'
              response = requests.post(api_url, data=post_data, auth=(auth_username, auth_password))

              post_url = response.json().get('link')
              print(f'Post URL: {post_url}')
              return post_url, file_link  # Returning both post_url and file_link
          auth_username = 'username'
          auth_password = 'password'
          post_url, file_link = createPost(auth_username, auth_password, text, title)


          reply = (
           "𝗬𝗼𝘂𝗿 𝗟𝗶𝗻𝗸 𝗚𝗲𝗻𝗲𝗿𝗮𝘁𝗲𝗱 !\n\n"
           f"📂 Fɪʟᴇ ɴᴀᴍᴇ : {file_name}\n\n"
           f"📦 Fɪʟᴇ ꜱɪᴢᴇ : {file_size_mib:.2f} MiB\n\n"
           f"📥 Dᴏᴡɴʟᴏᴀᴅ : {file_link}\n\n"
           f"🖥 WATCH  : {post_url}\n\n"
           "🚸 Nᴏᴛᴇ : LINK WON'T EXPIRE TILL I DELETE"
          )
          keyboard = InlineKeyboardMarkup(
             [
                [
                   InlineKeyboardButton("🖥 WATCH", url=f"{post_url}"),
                   InlineKeyboardButton("📥 Dᴏᴡɴʟᴏᴀᴅ", url=f"{file_link}")
                ]
             ]
          )
          message.reply(reply, disable_web_page_preview=True, reply_markup=keyboard)
          os.remove(file_path)
       elif typefile == "MessageMediaType.VIDEO_NOTE":
          file_path = message.download()
          file_name = os.path.basename(file_path)
          file_size_bytes = os.path.getsize(file_path)
          file_size_mib = file_size_bytes / (1024 ** 2)
          text = message.caption
          lines = text.split('\n')
          title = lines[0]
          def restMediaUL(filePath, auth_username, auth_password):
              url = 'https://yoururl.com/wp-json/wp/v2/media'
              data = open(filePath, 'rb').read()
              fileName = os.path.basename(filePath)
              file_extension = os.path.splitext(filePath)[1]

              headers = {'Content-Type': f'video/{file_extension[1:]}', 'Content-Disposition': f'attachment; filename={fileName}'}
    
              res = requests.post(url=url, data=data, headers=headers, auth=(auth_username, auth_password))
    
              newDict = res.json()
              newID = newDict.get('id')
              link = newDict.get('guid').get("rendered")
              print(newID, link)
              return newID, link

          def createPost(auth_username, auth_password, text, title):
              post_data = {
                  'title': title,
                  'content': text,
                  'status': 'publish'
              }

              filePath = file_path
              file_id, file_link = restMediaUL(filePath, auth_username, auth_password)
              
              file_extension = os.path.splitext(filePath)[1]

              post_data['content'] = f'<video width="640" height="360" controls><source src="{file_link}" type="video/{file_extension[1:]}"></video>' + post_data['content']

              api_url = 'https://yoururl.com/wp-json/wp/v2/posts'
              response = requests.post(api_url, data=post_data, auth=(auth_username, auth_password))

              post_url = response.json().get('link')
              print(f'Post URL: {post_url}')
              return post_url, file_link  # Returning both post_url and file_link
          auth_username = 'username'
          auth_password = 'password'
          post_url, file_link = createPost(auth_username, auth_password, text, title)


          reply = (
           "𝗬𝗼𝘂𝗿 𝗟𝗶𝗻𝗸 𝗚𝗲𝗻𝗲𝗿𝗮𝘁𝗲𝗱 !\n\n"
           f"📂 Fɪʟᴇ ɴᴀᴍᴇ : {file_name}\n\n"
           f"📦 Fɪʟᴇ ꜱɪᴢᴇ : {file_size_mib:.2f} MiB\n\n"
           f"📥 Dᴏᴡɴʟᴏᴀᴅ : {file_link}\n\n"
           f"🖥 WATCH  : {post_url}\n\n"
           "🚸 Nᴏᴛᴇ : LINK WON'T EXPIRE TILL I DELETE"
          )
          keyboard = InlineKeyboardMarkup(
             [
                [
                   InlineKeyboardButton("🖥 WATCH", url=f"{post_url}"),
                   InlineKeyboardButton("📥 Dᴏᴡɴʟᴏᴀᴅ", url=f"{file_link}")
                ]
             ]
          )
          message.reply(reply, disable_web_page_preview=True, reply_markup=keyboard)
          os.remove(file_path)
       elif typefile == "MessageMediaType.DOCUMENT":
          file_path = message.download()
          file_name = os.path.basename(file_path)
          file_size_bytes = os.path.getsize(file_path)
          file_size_mib = file_size_bytes / (1024 ** 2)
          text = message.caption
          lines = text.split('\n')
          title = lines[0]
          mimetype = message.document.mime_type
          def restMediaUL(filePath, auth_username, auth_password):
              url = 'https://yoururl.com/wp-json/wp/v2/media'
              data = open(filePath, 'rb').read()
              fileName = os.path.basename(filePath)
              file_extension = os.path.splitext(filePath)[1]

              headers = {'Content-Type': f'{mimetype}', 'Content-Disposition': f'attachment; filename={fileName}'}
    
              res = requests.post(url=url, data=data, headers=headers, auth=(auth_username, auth_password))
    
              newDict = res.json()
              newID = newDict.get('id')
              link = newDict.get('guid').get("rendered")
              print(newID, link)
              return newID, link

          def createPost(auth_username, auth_password, text, title):
              post_data = {
                  'title': title,
                  'content': text,
                  'status': 'publish'
              }

              filePath = file_path
              file_id, file_link = restMediaUL(filePath, auth_username, auth_password)
              
              file_extension = os.path.splitext(filePath)[1]

              post_data['content'] = f'<a href="{file_link}" target="_blank" style="display:inline-block; padding:10px 20px; background-color:#3498db; color:#fff; text-decoration:none; border-radius:5px;">Download {file_name}</a>' + post_data['content']

              api_url = 'https://yoururl.com/wp-json/wp/v2/posts'
              response = requests.post(api_url, data=post_data, auth=(auth_username, auth_password))

              post_url = response.json().get('link')
              print(f'Post URL: {post_url}')
              return post_url, file_link  # Returning both post_url and file_link
          auth_username = 'username'
          auth_password = 'password'
          post_url, file_link = createPost(auth_username, auth_password, text, title)


          reply = (
           "𝗬𝗼𝘂𝗿 𝗟𝗶𝗻𝗸 𝗚𝗲𝗻𝗲𝗿𝗮𝘁𝗲𝗱 !\n\n"
           f"📂 Fɪʟᴇ ɴᴀᴍᴇ : {file_name}\n\n"
           f"📦 Fɪʟᴇ ꜱɪᴢᴇ : {file_size_mib:.2f} MiB\n\n"
           f"📥 Dᴏᴡɴʟᴏᴀᴅ : {file_link}\n\n"
           f"🖥 WATCH  : {post_url}\n\n"
           "🚸 Nᴏᴛᴇ : LINK WON'T EXPIRE TILL I DELETE"
          )
          keyboard = InlineKeyboardMarkup(
             [
                [
                   InlineKeyboardButton("🖥 WATCH", url=f"{post_url}"),
                   InlineKeyboardButton("📥 Dᴏᴡɴʟᴏᴀᴅ", url=f"{file_link}")
                ]
             ]
          )
          message.reply(reply, disable_web_page_preview=True, reply_markup=keyboard)
          os.remove(file_path)
       elif typefile == "MessageMediaType.STICKER":
          reply = "Sticker is not Supported for Conversion"
          message.reply(reply)
          
       elif typefile == "MessageMediaType.ANIMATION":
          reply = "Animation Media is not Supported for Conversion"
          message.reply(reply)
       
       elif typefile == "MessageMediaType.LOCATION":
          reply = "Location is not Supported for Conversion"
          message.reply(reply)
       
       elif typefile == "MessageMediaType.POLL":
          reply = "Poll is not Supported for Conversion"
          message.reply(reply)
          
       elif typefile == "MessageMediaType.DICE":
          reply = "Dice is not Supported for Conversion"
          message.reply(reply)
       
       elif typefile == "MessageMediaType.GAME":
          reply = "Game is not Supported for Conversion"
          message.reply(reply)
       elif typefile == "MessageMediaType.CONTACT":
          reply = "Contact is not Supported for Conversion"
          message.reply(reply)
       else:
          reply = "This Media Type is not Supported for Conversion"
          message.reply(reply)
       
    else:
       
       print("No Text & No Caption")
       print(message.media)
       typefile = str(message.media)
       if typefile == "MessageMediaType.VIDEO":
          file_path = message.download()
          file_name = os.path.basename(file_path)
          file_size_bytes = os.path.getsize(file_path)
          file_size_mib = file_size_bytes / (1024 ** 2)
          text = file_name
          title = file_name
          def restMediaUL(filePath, auth_username, auth_password):
              url = 'https://yoururl.com/wp-json/wp/v2/media'
              data = open(filePath, 'rb').read()
              fileName = os.path.basename(filePath)
              file_extension = os.path.splitext(filePath)[1]

              headers = {'Content-Type': f'video/{file_extension[1:]}', 'Content-Disposition': f'attachment; filename={fileName}'}
    
              res = requests.post(url=url, data=data, headers=headers, auth=(auth_username, auth_password))
    
              newDict = res.json()
              newID = newDict.get('id')
              link = newDict.get('guid').get("rendered")
              print(newID, link)
              return newID, link

          def createPost(auth_username, auth_password, text, title):
              post_data = {
                  'title': title,
                  'content': text,
                  'status': 'publish'
              }

              filePath = file_path
              file_id, file_link = restMediaUL(filePath, auth_username, auth_password)
              
              file_extension = os.path.splitext(filePath)[1]

              post_data['content'] = f'<video width="640" height="360" controls><source src="{file_link}" type="video/{file_extension[1:]}"></video>' + post_data['content']

              api_url = 'https://yoururl.com/wp-json/wp/v2/posts'
              response = requests.post(api_url, data=post_data, auth=(auth_username, auth_password))

              post_url = response.json().get('link')
              print(f'Post URL: {post_url}')
              return post_url, file_link  # Returning both post_url and file_link
          auth_username = 'username'
          auth_password = 'password'
          post_url, file_link = createPost(auth_username, auth_password, text, title)


          reply = (
           "𝗬𝗼𝘂𝗿 𝗟𝗶𝗻𝗸 𝗚𝗲𝗻𝗲𝗿𝗮𝘁𝗲𝗱 !\n\n"
           f"📂 Fɪʟᴇ ɴᴀᴍᴇ : {file_name}\n\n"
           f"📦 Fɪʟᴇ ꜱɪᴢᴇ : {file_size_mib:.2f} MiB\n\n"
           f"📥 Dᴏᴡɴʟᴏᴀᴅ : {file_link}\n\n"
           f"🖥 WATCH  : {post_url}\n\n"
           "🚸 Nᴏᴛᴇ : LINK WON'T EXPIRE TILL I DELETE"
          )
          keyboard = InlineKeyboardMarkup(
             [
                [
                   InlineKeyboardButton("🖥 WATCH", url=f"{post_url}"),
                   InlineKeyboardButton("📥 Dᴏᴡɴʟᴏᴀᴅ", url=f"{file_link}")
                ]
             ]
          )
          message.reply(reply, disable_web_page_preview=True, reply_markup=keyboard)
          os.remove(file_path)
       elif typefile == "MessageMediaType.PHOTO":
          file_path = message.download()
          file_name = os.path.basename(file_path)
          file_size_bytes = os.path.getsize(file_path)
          file_size_mib = file_size_bytes / (1024 ** 2)
          text = file_name
          title = file_name
          def restMediaUL(filePath, auth_username, auth_password):
              url = 'https://yoururl.com/wp-json/wp/v2/media'
              data = open(filePath, 'rb').read()
              fileName = os.path.basename(filePath)
              file_extension = os.path.splitext(filePath)[1]

              headers = {'Content-Type': f'image/{file_extension[1:]}', 'Content-Disposition': f'attachment; filename={fileName}'}
    
              res = requests.post(url=url, data=data, headers=headers, auth=(auth_username, auth_password))
    
              newDict = res.json()
              newID = newDict.get('id')
              link = newDict.get('guid').get("rendered")
              print(newID, link)
              return newID, link

          def createPost(auth_username, auth_password, text, title):
              post_data = {
                  'title': title,
                  'content': text,
                  'status': 'publish'
              }

              filePath = file_path
              file_id, file_link = restMediaUL(filePath, auth_username, auth_password)
              file_extension = os.path.splitext(filePath)[1]
              post_data['content'] = f'<img src="{file_link}" alt="{file_name}">' + post_data['content']

              api_url = 'https://yoururl.com/wp-json/wp/v2/posts'
              response = requests.post(api_url, data=post_data, auth=(auth_username, auth_password))

              post_url = response.json().get('link')
              print(f'Post URL: {post_url}')
              return post_url, file_link  # Returning both post_url and file_link
          auth_username = 'username'
          auth_password = 'password'
          post_url, file_link = createPost(auth_username, auth_password, text, title)


          reply = (
           "𝗬𝗼𝘂𝗿 𝗟𝗶𝗻𝗸 𝗚𝗲𝗻𝗲𝗿𝗮𝘁𝗲𝗱 !\n\n"
           f"📂 Fɪʟᴇ ɴᴀᴍᴇ : {file_name}\n\n"
           f"📦 Fɪʟᴇ ꜱɪᴢᴇ : {file_size_mib:.2f} MiB\n\n"
           f"📥 Dᴏᴡɴʟᴏᴀᴅ : {file_link}\n\n"
           f"🖥 WATCH  : {post_url}\n\n"
           "🚸 Nᴏᴛᴇ : LINK WON'T EXPIRE TILL I DELETE"
          )
          keyboard = InlineKeyboardMarkup(
             [
                [
                   InlineKeyboardButton("🖥 WATCH", url=f"{post_url}"),
                   InlineKeyboardButton("📥 Dᴏᴡɴʟᴏᴀᴅ", url=f"{file_link}")
                ]
             ]
          )
          message.reply(reply, disable_web_page_preview=True, reply_markup=keyboard)
          os.remove(file_path)
       elif typefile == "MessageMediaType.AUDIO":
          file_path = message.download()
          file_name = os.path.basename(file_path)
          file_size_bytes = os.path.getsize(file_path)
          file_size_mib = file_size_bytes / (1024 ** 2)
          text = file_name
          title = file_name
          def restMediaUL(filePath, auth_username, auth_password):
              url = 'https://yoururl.com/wp-json/wp/v2/media'
              data = open(filePath, 'rb').read()
              fileName = os.path.basename(filePath)
              file_extension = os.path.splitext(filePath)[1]

              headers = {'Content-Type': f'audio/{file_extension[1:]}', 'Content-Disposition': f'attachment; filename={fileName}'}
    
              res = requests.post(url=url, data=data, headers=headers, auth=(auth_username, auth_password))
    
              newDict = res.json()
              newID = newDict.get('id')
              link = newDict.get('guid').get("rendered")
              print(newID, link)
              return newID, link

          def createPost(auth_username, auth_password, text, title):
              post_data = {
                  'title': title,
                  'content': text,
                  'status': 'publish'
              }

              filePath = file_path
              file_id, file_link = restMediaUL(filePath, auth_username, auth_password)
              file_extension = os.path.splitext(filePath)[1]
              post_data['content'] = f'<audio controls><source src="{file_link}" type="audio/{file_extension[1:]}"></audio>' + post_data['content']

              api_url = 'https://yoururl.com/wp-json/wp/v2/posts'
              response = requests.post(api_url, data=post_data, auth=(auth_username, auth_password))

              post_url = response.json().get('link')
              print(f'Post URL: {post_url}')
              return post_url, file_link  # Returning both post_url and file_link
          auth_username = 'username'
          auth_password = 'password'
          post_url, file_link = createPost(auth_username, auth_password, text, title)


          reply = (
           "𝗬𝗼𝘂𝗿 𝗟𝗶𝗻𝗸 𝗚𝗲𝗻𝗲𝗿𝗮𝘁𝗲𝗱 !\n\n"
           f"📂 Fɪʟᴇ ɴᴀᴍᴇ : {file_name}\n\n"
           f"📦 Fɪʟᴇ ꜱɪᴢᴇ : {file_size_mib:.2f} MiB\n\n"
           f"📥 Dᴏᴡɴʟᴏᴀᴅ : {file_link}\n\n"
           f"🖥 WATCH  : {post_url}\n\n"
           "🚸 Nᴏᴛᴇ : LINK WON'T EXPIRE TILL I DELETE"
          )
          keyboard = InlineKeyboardMarkup(
             [
                [
                   InlineKeyboardButton("🖥 WATCH", url=f"{post_url}"),
                   InlineKeyboardButton("📥 Dᴏᴡɴʟᴏᴀᴅ", url=f"{file_link}")
                ]
             ]
          )
          message.reply(reply, disable_web_page_preview=True, reply_markup=keyboard)
          os.remove(file_path)
       elif typefile == "MessageMediaType.VOICE":
          file_path = message.download()
          file_name = os.path.basename(file_path)
          file_size_bytes = os.path.getsize(file_path)
          file_size_mib = file_size_bytes / (1024 ** 2)
          text = file_name
          title = file_name
          def restMediaUL(filePath, auth_username, auth_password):
              url = 'https://yoururl.com/wp-json/wp/v2/media'
              data = open(filePath, 'rb').read()
              fileName = os.path.basename(filePath)
              file_extension = os.path.splitext(filePath)[1]

              headers = {'Content-Type': f'audio/{file_extension[1:]}', 'Content-Disposition': f'attachment; filename={fileName}'}
    
              res = requests.post(url=url, data=data, headers=headers, auth=(auth_username, auth_password))
    
              newDict = res.json()
              newID = newDict.get('id')
              link = newDict.get('guid').get("rendered")
              print(newID, link)
              return newID, link

          def createPost(auth_username, auth_password, text, title):
              post_data = {
                  'title': title,
                  'content': text,
                  'status': 'publish'
              }

              filePath = file_path
              file_id, file_link = restMediaUL(filePath, auth_username, auth_password)
              file_extension = os.path.splitext(filePath)[1]
              post_data['content'] = f'<audio controls><source src="{file_link}" type="audio/{file_extension[1:]}"></audio>' + post_data['content']

              api_url = 'https://yoururl.com/wp-json/wp/v2/posts'
              response = requests.post(api_url, data=post_data, auth=(auth_username, auth_password))

              post_url = response.json().get('link')
              print(f'Post URL: {post_url}')
              return post_url, file_link  # Returning both post_url and file_link
          auth_username = 'username'
          auth_password = 'password'
          post_url, file_link = createPost(auth_username, auth_password, text, title)


          reply = (
           "𝗬𝗼𝘂𝗿 𝗟𝗶𝗻𝗸 𝗚𝗲𝗻𝗲𝗿𝗮𝘁𝗲𝗱 !\n\n"
           f"📂 Fɪʟᴇ ɴᴀᴍᴇ : {file_name}\n\n"
           f"📦 Fɪʟᴇ ꜱɪᴢᴇ : {file_size_mib:.2f} MiB\n\n"
           f"📥 Dᴏᴡɴʟᴏᴀᴅ : {file_link}\n\n"
           f"🖥 WATCH  : {post_url}\n\n"
           "🚸 Nᴏᴛᴇ : LINK WON'T EXPIRE TILL I DELETE"
          )
          keyboard = InlineKeyboardMarkup(
             [
                [
                   InlineKeyboardButton("🖥 WATCH", url=f"{post_url}"),
                   InlineKeyboardButton("📥 Dᴏᴡɴʟᴏᴀᴅ", url=f"{file_link}")
                ]
             ]
          )
          message.reply(reply, disable_web_page_preview=True, reply_markup=keyboard)
          os.remove(file_path)
       elif typefile == "MessageMediaType.VIDEO_NOTE":
          file_path = message.download()
          file_name = os.path.basename(file_path)
          file_size_bytes = os.path.getsize(file_path)
          file_size_mib = file_size_bytes / (1024 ** 2)
          text = file_name
          title = file_name
          def restMediaUL(filePath, auth_username, auth_password):
              url = 'https://yoururl.com/wp-json/wp/v2/media'
              data = open(filePath, 'rb').read()
              fileName = os.path.basename(filePath)
              file_extension = os.path.splitext(filePath)[1]

              headers = {'Content-Type': f'video/{file_extension[1:]}', 'Content-Disposition': f'attachment; filename={fileName}'}
    
              res = requests.post(url=url, data=data, headers=headers, auth=(auth_username, auth_password))
    
              newDict = res.json()
              newID = newDict.get('id')
              link = newDict.get('guid').get("rendered")
              print(newID, link)
              return newID, link

          def createPost(auth_username, auth_password, text, title):
              post_data = {
                  'title': title,
                  'content': text,
                  'status': 'publish'
              }

              filePath = file_path
              file_id, file_link = restMediaUL(filePath, auth_username, auth_password)
              
              file_extension = os.path.splitext(filePath)[1]

              post_data['content'] = f'<video width="640" height="360" controls><source src="{file_link}" type="video/{file_extension[1:]}"></video>' + post_data['content']

              api_url = 'https://yoururl.com/wp-json/wp/v2/posts'
              response = requests.post(api_url, data=post_data, auth=(auth_username, auth_password))

              post_url = response.json().get('link')
              print(f'Post URL: {post_url}')
              return post_url, file_link  # Returning both post_url and file_link
          auth_username = 'username'
          auth_password = 'password'
          post_url, file_link = createPost(auth_username, auth_password, text, title)


          reply = (
           "𝗬𝗼𝘂𝗿 𝗟𝗶𝗻𝗸 𝗚𝗲𝗻𝗲𝗿𝗮𝘁𝗲𝗱 !\n\n"
           f"📂 Fɪʟᴇ ɴᴀᴍᴇ : {file_name}\n\n"
           f"📦 Fɪʟᴇ ꜱɪᴢᴇ : {file_size_mib:.2f} MiB\n\n"
           f"📥 Dᴏᴡɴʟᴏᴀᴅ : {file_link}\n\n"
           f"🖥 WATCH  : {post_url}\n\n"
           "🚸 Nᴏᴛᴇ : LINK WON'T EXPIRE TILL I DELETE"
          )
          keyboard = InlineKeyboardMarkup(
             [
                [
                   InlineKeyboardButton("🖥 WATCH", url=f"{post_url}"),
                   InlineKeyboardButton("📥 Dᴏᴡɴʟᴏᴀᴅ", url=f"{file_link}")
                ]
             ]
          )
          message.reply(reply, disable_web_page_preview=True, reply_markup=keyboard)
          os.remove(file_path)
       elif typefile == "MessageMediaType.DOCUMENT":
          file_path = message.download()
          file_name = os.path.basename(file_path)
          file_size_bytes = os.path.getsize(file_path)
          file_size_mib = file_size_bytes / (1024 ** 2)
          mimetype = message.document.mime_type
          def restMediaUL(filePath, auth_username, auth_password):
              url = 'https://yoururl.com/wp-json/wp/v2/media'
              data = open(filePath, 'rb').read()
              fileName = os.path.basename(filePath)
              file_extension = os.path.splitext(filePath)[1]

              headers = {'Content-Type': f'{mimetype}', 'Content-Disposition': f'attachment; filename={fileName}'}
    
              res = requests.post(url=url, data=data, headers=headers, auth=(auth_username, auth_password))
    
              newDict = res.json()
              newID = newDict.get('id')
              link = newDict.get('guid').get("rendered")
              print(newID, link)
              return newID, link

          def createPost(auth_username, auth_password, text, title):
              post_data = {
                  'title': title,
                  'content': text,
                  'status': 'publish'
              }

              filePath = file_path
              file_id, file_link = restMediaUL(filePath, auth_username, auth_password)
              
              file_extension = os.path.splitext(filePath)[1]

              post_data['content'] = f'<a href="{file_link}" target="_blank" style="display:inline-block; padding:10px 20px; background-color:#3498db; color:#fff; text-decoration:none; border-radius:5px;">Download {file_name}</a>' + post_data['content']

              api_url = 'https://yoururl.com/wp-json/wp/v2/posts'
              response = requests.post(api_url, data=post_data, auth=(auth_username, auth_password))

              post_url = response.json().get('link')
              print(f'Post URL: {post_url}')
              return post_url, file_link  # Returning both post_url and file_link
          auth_username = 'username'
          auth_password = 'password'
          post_url, file_link = createPost(auth_username, auth_password, text, title)


          reply = (
           "𝗬𝗼𝘂𝗿 𝗟𝗶𝗻𝗸 𝗚𝗲𝗻𝗲𝗿𝗮𝘁𝗲𝗱 !\n\n"
           f"📂 Fɪʟᴇ ɴᴀᴍᴇ : {file_name}\n\n"
           f"📦 Fɪʟᴇ ꜱɪᴢᴇ : {file_size_mib:.2f} MiB\n\n"
           f"📥 Dᴏᴡɴʟᴏᴀᴅ : {file_link}\n\n"
           f"🖥 WATCH  : {post_url}\n\n"
           "🚸 Nᴏᴛᴇ : LINK WON'T EXPIRE TILL I DELETE"
          )
          keyboard = InlineKeyboardMarkup(
             [
                [
                   InlineKeyboardButton("🖥 WATCH", url=f"{post_url}"),
                   InlineKeyboardButton("📥 Dᴏᴡɴʟᴏᴀᴅ", url=f"{file_link}")
                ]
             ]
          )
          message.reply(reply, disable_web_page_preview=True, reply_markup=keyboard)
          os.remove(file_path)
       elif typefile == "MessageMediaType.STICKER":
          reply = "Sticker is not Supported for Conversion"
          message.reply(reply)
          
       elif typefile == "MessageMediaType.ANIMATION":
          reply = "Animation Media is not Supported for Conversion"
          message.reply(reply)
       
       elif typefile == "MessageMediaType.LOCATION":
          reply = "Location is not Supported for Conversion"
          message.reply(reply)
       
       elif typefile == "MessageMediaType.POLL":
          reply = "Poll is not Supported for Conversion"
          message.reply(reply)
          
       elif typefile == "MessageMediaType.DICE":
          reply = "Dice is not Supported for Conversion"
          message.reply(reply)
       
       elif typefile == "MessageMediaType.GAME":
          reply = "Game is not Supported for Conversion"
          message.reply(reply)
       elif typefile == "MessageMediaType.CONTACT":
          reply = "Contact is not Supported for Conversion"
          message.reply(reply)
       else:
          reply = "This Media Type is not Supported for Conversion"
          message.reply(reply)




if __name__ == "__main__":
    app.run()
