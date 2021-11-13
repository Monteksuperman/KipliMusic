from pyrogram import Client, filters, types
from solidAPI import emoji

from base.client_base import bot
from utils.functions import get_yt_details, download_yt_thumbnails

markup_keyboard = types.InlineKeyboardMarkup
button_keyboard = types.InlineKeyboardButton


@Client.on_message(filters.command("start"))
async def start_(_, message: types.Message):
    bot_username = (await bot.get_me()).username
    user_id = message.from_user.id
    if message.chat.type == "supergroup":
        return await message.reply(
            f"{emoji.SPARKLES} hi {message.from_user.mention}!\n"
            f"i'm solidmusic bot, make me as an admin, so i can play musics in this chat's"
        )
    if message.chat.type == "private":
        if len(message.command) == 1:
            await message.reply(
                f"hi {message.from_user.mention}! i can play musics on your groups through"
                "telegram voice chats\n"
                f"{emoji.LIGHT_BULB} find out all my command by clicking \"commands\" button",
                reply_markup=markup_keyboard(
                    [
                        [
                            button_keyboard(
                                f"{emoji.PLUS} add me to your chats",
                                url=f"https://t.me/{bot_username}?startgroup=true")
                        ],
                        [
                            button_keyboard(
                                f"{emoji.NOTEBOOK} commands",
                                callback_data="help_commands"
                            )
                        ],
                        [
                            button_keyboard(
                                f"{emoji.LOUDSPEAKER} channel",
                                url="https://t.me/☞katakipli"
                            )
                        ],
                        [
                            button_keyboard(
                                f"{emoji.FIRE} maintainer",
                                url="https://t.me/raflyskuy"
                            )
                        ]
                    ]
                )
            )
        elif len(message.command) == 2:
            query = message.command[1]
            if query.startswith("ytinfo_"):
                yt_link = query.split("ytinfo_")[1]
                details = get_yt_details(yt_link)
                thumb_url = details["thumbnails"]
                thumb_file = download_yt_thumbnails(thumb_url, user_id)
                result_text = (
                    f"**track information**\n\n"
                    f"{emoji.LABEL} title: {details['title']}\n"
                    f"{emoji.MEGAPHONE} channel: {details['channel']}\n"
                    f"{emoji.STOPWATCH} duration: {details['duration']}\n"
                    f"{emoji.THUMBS_UP} likes: {details['likes']}\n"
                    f"{emoji.THUMBS_DOWN} dislikes: {details['dislikes']}\n"
                    f"{emoji.STAR} rating: {details['rating']}\n"
                )
                await message.reply_photo(
                    thumb_file, caption=result_text, reply_markup=markup_keyboard(
                        [
                            [
                                button_keyboard(
                                    f"{emoji.MOVIE_CAMERA} watch on youtube",
                                    url=f"{details['link']}"
                                )
                            ],
                            [
                                button_keyboard(
                                    f"{emoji.WASTEBASKET} close",
                                    callback_data="cls"
                                )
                            ]
                        ]
                    )
                )
