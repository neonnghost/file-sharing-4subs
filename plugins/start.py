import asyncio
import random
import string
import time

from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import FloodWait, UserIsBlocked, InputUserDeactivated

from config import (
    ADMINS,
    FORCE_MSG,
    START_MSG,
    CUSTOM_CAPTION,
    IS_VERIFY,
    VERIFY_EXPIRE,
    SHORTLINK_API,
    SHORTLINK_URL,
    DISABLE_CHANNEL_BUTTON,
    PROTECT_CONTENT,
    TUT_VID,
)
from helper_func import subscribed, get_messages, get_shortlink, get_verify_status, update_verify_status, get_exp_time
from database.database import add_user, del_user, full_userbase, present_user

# Initialize your bot instance
Bot = Client("my_bot", api_id=12345, api_hash="your_api_hash", bot_token="your_bot_token")

@Bot.on_message(filters.command('start') & filters.private & subscribed)
async def start_command(client: Client, message: Message):
    id = message.from_user.id
    owner_id = ADMINS  # Fetch the owner's ID from config

    if id == owner_id:
        await message.reply("You are the owner! Additional actions can be added here.")
    else:
        if not await present_user(id):
            try:
                await add_user(id)
            except:
                pass

        verify_status = await get_verify_status(id)
        if verify_status['is_verified'] and VERIFY_EXPIRE < (time.time() - verify_status['verified_time']):
            await update_verify_status(id, is_verified=False)

        if "verify_" in message.text:
            _, token = message.text.split("_", 1)
            if verify_status['verify_token'] != token:
                return await message.reply("Your token is invalid or expired. Generate a new one with /start.")
            
            await update_verify_status(id, is_verified=True, verified_time=time.time())
            link = await get_shortlink(SHORTLINK_URL, SHORTLINK_API, f'https://telegram.dog/{client.username}?start=verify_{token}')
            btn = [
                [InlineKeyboardButton("Click here", url=link)],
                [InlineKeyboardButton('How to use the bot', url=TUT_VID)]
            ]

            await message.reply(
                f"""🚨 Ads token expired! 🚨\n
                Refresh your token and try again. ⏳ Token Timeout: {get_exp_time(VERIFY_EXPIRE)} \n
                Pass 1 ad to use the bot for 16 hours.\n
                Token generation takes 1-2 minutes. 🎥✨\n
                Need help? Watch our video tutorial! 📹\n
                Facing issues? Contact @i_am_yamraj 📩""",
                reply_markup=InlineKeyboardMarkup(btn),
                protect_content=False,
                quote=True
            )

        elif len(message.text) > 7 and verify_status['is_verified']:
            try:
                base64_string = message.text.split(" ", 1)[1]
                _string = await decode(base64_string)
                argument = _string.split("-")
                
                if len(argument) == 3:
                    start = int(int(argument[1]) / abs(client.db_channel.id))
                    end = int(int(argument[2]) / abs(client.db_channel.id))
                    ids = range(start, end+1)
                elif len(argument) == 2:
                    ids = [int(int(argument[1]) / abs(client.db_channel.id))]
                else:
                    return

                temp_msg = await message.reply("Please wait...")
                messages = await get_messages(client, ids)
                await temp_msg.delete()

                snt_msgs = []
                for msg in messages:
                    if bool(CUSTOM_CAPTION) and bool(msg.document):
                        caption = CUSTOM_CAPTION.format(previouscaption="" if not msg.caption else msg.caption.html, filename=msg.document.file_name)
                    else:
                        caption = "" if not msg.caption else msg.caption.html

                    if DISABLE_CHANNEL_BUTTON:
                        reply_markup = msg.reply_markup
                    else:
                        reply_markup = None

                    try:
                        snt_msg = await msg.copy(chat_id=message.from_user.id, caption=caption, parse_mode=ParseMode.HTML, reply_markup=reply_markup, protect_content=PROTECT_CONTENT)
                        snt_msgs.append(snt_msg)
                    except FloodWait as e:
                        await asyncio.sleep(e.x)
                        snt_msg = await msg.copy(chat_id=message.from_user.id, caption=caption, parse_mode=ParseMode.HTML, reply_markup=reply_markup, protect_content=PROTECT_CONTENT)
                        snt_msgs.append(snt_msg)
                    except:
                        pass

            except Exception as e:
                await message.reply_text("Something went wrong...")

        elif verify_status['is_verified']:
            reply_markup = InlineKeyboardMarkup(
                [[InlineKeyboardButton("About Me", callback_data="about"),
                  InlineKeyboardButton("Close", callback_data="close")]]
            )
            await message.reply_text(
                text=START_MSG.format(
                    first=message.from_user.first_name,
                    last=message.from_user.last_name,
                    username='@' + message.from_user.username if message.from_user.username else '',
                    mention=message.from_user.mention,
                    id=message.from_user.id
                ),
                reply_markup=reply_markup,
                disable_web_page_preview=True,
                quote=True
            )

        else:
            if IS_VERIFY and not verify_status['is_verified']:
                token = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
                await update_verify_status(id, verify_token=token, link="")
                link = await get_shortlink(SHORTLINK_URL, SHORTLINK_API, f'https://telegram.dog/{client.username}?start=verify_{token}')
                btn = [
                    [InlineKeyboardButton("Click here", url=link)],
                    [InlineKeyboardButton('How to use the bot', url=TUT_VID)]
                ]

                await message.reply(
                    f"""🚨 Ads token expired! 🚨\n
                    Refresh your token and try again. ⏳ Token Timeout: {get_exp_time(VERIFY_EXPIRE)} \n
                    Pass 1 ad to use the bot for 16 hours.\n
                    Token generation takes 1-2 minutes. 🎥✨\n
                    Need help? Watch our video tutorial! 📹\n
                    Facing issues? Contact @i_am_yamraj 📩""",
                    reply_markup=InlineKeyboardMarkup(btn),
                    protect_content=False,
                    quote=True
                )

#=====================================================================================##

WAIT_MSG = "<b>Processing ...</b>"

REPLY_ERROR = "<code>Use this command as a replay to any telegram message without any spaces.</code>"

#=====================================================================================##

@Bot.on_message(filters.command('start') & filters.private)
async def not_joined(client: Client, message: Message):
    buttons = [
        [
            InlineKeyboardButton(text="Join Channel", url=client.invitelink),
            InlineKeyboardButton(text="Join Channel", url=client.invitelink2),
        ],
        [
            InlineKeyboardButton(text="Join Channel", url=client.invitelink3),
            InlineKeyboardButton(text="Join Channel", url=client.invitelink4),
        ]
    ]

    try:
        buttons.append(
            [
                InlineKeyboardButton(
                    text='Try Again',
                    url=f"https://t.me/{client.username}?start={message.command[1]}"
                )
            ]
        )
    except IndexError:
        pass

    await message.reply(
        text=FORCE_MSG.format(
            first=message.from_user.first_name,
            last=message.from_user.last_name,
            username='@' + message.from_user.username if message.from_user.username else '',
            mention=message.from_user.mention,
            id=message.from_user.id
        ),
        reply_markup=InlineKeyboardMarkup(buttons),
        quote=True,
        disable_web_page_preview=True
    )

@Bot.on_message(filters.command('users') & filters.private & filters.user(ADMINS))
async def get_users(client: Bot, message: Message):
    msg = await client.send_message(chat_id=message.chat.id, text=WAIT_MSG)
    users = await full_userbase()
    await msg.edit(f"{len(users)} users are using this bot")

@Bot.on_message(filters.private & filters.command('broadcast') & filters.user(ADMINS))
async def send_text(client: Bot, message: Message):
    if message.reply_to_message:
        query = await full_userbase()
        broadcast_msg = message.reply_to_message
        total = 0
        successful = 0
        blocked = 0
        deleted = 0
        unsuccessful = 0

        pls_wait = await message.reply("<i>Broadcasting Message.. This will Take Some Time</i>")
        for chat_id in query:
            try:
                await broadcast_msg.copy(chat_id)
                successful += 1
            except FloodWait as e:
                await asyncio.sleep(e.x)
                await broadcast_msg.copy(chat_id)
                successful += 1
            except UserIsBlocked:
                await del_user(chat_id)
                blocked += 1
            except InputUserDeactivated:
                await del_user(chat_id)
                deleted += 1
            except Exception as e:
                unsuccessful += 1
                logging.error(f"Error broadcasting message to {chat_id}: {str(e)}")
            
            total += 1

        status = f"""<b><u>Broadcast Completed</u>

    Total Users: <code>{total}</code>
    Successful: <code>{successful}</code>
    Blocked Users: <code>{blocked}</code>
    Deleted Accounts: <code>{deleted}</code>
    Unsuccessful: <code>{unsuccessful}</code></b>"""

        await pls_wait.edit(status)

    else:
        msg = await message.reply(REPLY_ERROR)
        await asyncio.sleep(8)
        await msg.delete()

