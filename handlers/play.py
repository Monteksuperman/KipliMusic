from pyrogram import Client, filters, types
from solidAPI import emoji

from utils.functions import group_only
from utils.pyro_utils import music_result, yt_search
from base.player import player

button_keyboard = types.InlineKeyboardButton


def play_keyboard(user_id: int):
    i = 0
    for j in range(5):
        i += 1
        yield button_keyboard(f"{i}", callback_data=f"play {j}|{user_id}")
        j += 1


@Client.on_message(filters.command("play") & group_only)
async def play_(client: Client, message: types.Message):
    proc = await message.reply(f"{emoji.MAGNIFYING_GLASS_TILTED_LEFT} searching...")
    bot_username = (await client.get_me()).username
    query = " ".join(message.command[1:])
    user_id = message.from_user.id
    yts = yt_search(query)
    cache = []
    chat_id = message.chat.id
    music_result[chat_id] = []
    for count, j in enumerate(yts, start=1):
        cache.append(j)
        if count % 5 == 0:
            music_result[chat_id].append(cache)
            cache = []
        if count == len(yts):
            music_result[chat_id].append(cache)
    yts.clear()
    results = "\n"
    k = 0
    for i in music_result[chat_id][0]:
        k += 1
        results += f"{k}. [{i['title'][:35]}...]({i['url']})\n"
        results += f"┣ {emoji.LIGHT_BULB} duration - {i['duration']}\n"
        results += f"┣ {emoji.FIRE} [More Information](https://t.me/{bot_username}?start=ytinfo_{i['id']})\n"
        results += "┗ powered by Zaen project\n\n"

    temps = []
    keyboards = []
    in_board = list(play_keyboard(user_id))
    for count, j in enumerate(in_board, start=1):
        temps.append(j)
        if count % 3 == 0:
            keyboards.append(temps)
            temps = []
        if count == len(in_board):
            keyboards.append(temps)
    await proc.delete()
    await client.send_message(
        chat_id,
        f"{results}",
        reply_markup=types.InlineKeyboardMarkup(
            [
                keyboards[0],
                keyboards[1],
                [
                    button_keyboard(f"next {emoji.RIGHT_ARROW}", f"next|{user_id}"),
                    button_keyboard(f"close {emoji.WASTEBASKET}", f"close|{user_id}"),
                ],
            ]
        ),
        disable_web_page_preview=True,
    )


@Client.on_message(filters.command("playlist") & group_only)
async def playlist_(client: Client, message: types.Message):
    chat_id = message.chat.id
    bot_username = (await client.get_me()).username
    reply = message.reply
    try:
        current, queued = player.send_playlist(chat_id)
        current_user_id = current["user_id"]
        mention_current_user = (await message.chat.get_member(current_user_id)).user.mention
        if current and not queued:
            return await reply(
                f"now playing\n"
                f"📌 title: [{current['title']}](https://t.me/{bot_username}?start=ytinfo_{current['yt_id']})\n"
                f"⏱ duration: {current['duration']}\n"
                f"🙌 requested by: {mention_current_user}"
            )
        if current and queued:
            ques = "\n"
            for i in queued:
                title = i["title"]
                duration = i["duration"]
                req_by = i["user_id"]
                yt_id = i["yt_id"]
                mention_user = (await message.chat.get_member(req_by)).user.mention
                ques += f"📌 title: [{title}](https://t.me/{bot_username}?start=ytinfo_{yt_id})\n"
                ques += f"⏱ duration: {duration}\n"
                ques += f"🙌 requested by: {mention_user}\n\n"
            return await reply(
                f"now playing\n"
                f"📌 title: [{current['title']}](https://t.me/{bot_username}?start=ytinfo_{current['yt_id']})\n"
                f"⏱ duration: {current['duration']}\n"
                f"🙌 requested by: {mention_current_user}\n\n\n"
                f"💬 in queue\n{ques}",
                disable_web_page_preview=True
            )
        return
    except KeyError:
        return await reply("not playing") 
