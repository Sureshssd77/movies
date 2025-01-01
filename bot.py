import logging
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from database.jsreferdb import referdb
from utils import get_readable_time
from Script import script
import pytz
from datetime import datetime as dt

# Setup logging
logger = logging.getLogger(__name__)

# Constants
VERIFY_IMG = "https://graph.org/file/75fa3914579071acedfe1-f9c83b1ced674991a9.jpg"
TWO_VERIFY_GAP = 5  # 5 minutes
U_NAME = "#ssd_movies_providerbot"
DATABASE_URI = "mongodb+srv://sureshjaat2612:dilip261210@ssd.7oyrv.mongodb.net/?retryWrites=true&w=majority&appName=SSD"
VERIFY_COMPLETE_TEXT = "You are verified, now you can request movies."
ADMIN = "@suresh_jaat_7"

# Helper function to handle verification
async def handle_verification(client, message, user_id, verify_id):
    try:
        verify_id_info = await db.get_verify_id_info(user_id, verify_id)
        if not verify_id_info or verify_id_info["verified"]:
            await message.reply("<b>ʟɪɴᴋ ᴇxᴘɪʀᴇᴅ ᴛʀʏ ᴀɢᴀɪɴ...</b>")
            return False
        return True
    except Exception as e:
        logger.error(f"Error while handling verification for user {user_id}: {str(e)}")
        await message.reply("Error occurred during verification process.")
        return False

# Helper function to send the verification completion message
async def send_verification_message(client, message, user_id, verify_id, file_id, settings, num):
    btn = [[
        InlineKeyboardButton("‼️ ᴄʟɪᴄᴋ ʜᴇʀᴇ ᴛᴏ ɢᴇᴛ ꜰɪʟᴇ ‼️", url=f"https://telegram.me/{U_NAME}?start=file_{settings['group_id']}_{file_id}"),
    ]]
    reply_markup = InlineKeyboardMarkup(btn)
    msg = VERIFY_COMPLETE_TEXT
    await message.reply_photo(
        photo=VERIFY_IMG,
        caption=msg.format(message.from_user.mention, get_readable_time(TWO_VERIFY_GAP)),
        reply_markup=reply_markup,
        parse_mode="HTML"
    )

# Command to generate invite link
@Client.on_message(filters.command("invite") & filters.private & filters.user(ADMIN))
async def invite(client, message):
    toGenInvLink = message.command[1]
    if len(toGenInvLink) != 14:
        await message.reply("Invalid chat id\nAdd -100 before chat id if You did not add any yet.")
        return

    try:
        link = await client.export_chat_invite_link(toGenInvLink)
        await message.reply(link)
    except Exception as e:
        logger.error(f"Error generating invite link for chat {toGenInvLink}: {e}")
        await message.reply(f"Error generating invite link: {e}")

# Start command with verification
@Client.on_message(filters.command("start") & filters.incoming)
async def start(client: Client, message):
    user_id = message.from_user.id
    pm_mode = False

    try:
        data = message.command[1]
        if data.startswith('pm_mode_'):
            pm_mode = True
    except:
        pass

    # Verification Process
    if len(message.command) == 2 and message.command[1].startswith('notcopy'):
        _, userid, verify_id, file_id = message.command[1].split("_", 3)
        user_id = int(userid)
        grp_id = temp.CHAT.get(user_id, 0)

        # Handle verification logic
        if await handle_verification(client, message, user_id, verify_id):
            settings = await get_settings(grp_id)
            num = 2
            await send_verification_message(client, message, user_id, verify_id, file_id, settings, num)
        return

    # Referral Process
    if len(message.command) == 2 and message.command[1].startswith("reff_"):
        user_id = int(message.command[1].split("_")[1])

        if user_id == message.from_user.id:
            await message.reply_text("
