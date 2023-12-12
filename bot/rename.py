import tracemalloc
tracemalloc.start()

from AnilistPython import Anilist
import anitopy
import asyncio
from .func import run_async
anilist = Anilist()

CAPTION = """
<b><i>{}</i></b>

‣ <b>Type :</b> {}
‣ <b>Average Rating :</b> {}
‣ <b>Status :</b> {}
‣ <b>First aired :</b> {}
‣ <b>Last aired :</b> {}
‣ <b>Runtime :</b> {}
‣ <b>No of Episodes :</b> {}

‣ <b>Synopsis :</b> {}

‣ <b>Powered By :</b> @Roofiverse & @FuZionX
"""

async def get_english(anime_name):
    try:
        anime = anilist.get_anime(anime_name)
        x = anime.get("name_english")
        return x.strip() or anime_name
    except Exception as error:
        print(error)
        return anime_name.strip()

async def get_poster(name):
    try:
        anime_name = get_proper_name_for_func(name)
        if anime_name:
            anime_id = anilist.get_anime_id(anime_name)
            return f"https://img.anili.st/media/{anime_id}"
    except Exception as error:
        print(error)
        return None

async def get_cover(name):
    try:
        return "https://te.legra.ph/file/797fd901302402cd1a7c1.jpg"
    except Exception as error:
        print(error)
        return None

async def get_caption(name):
    try:
        anime_name = get_proper_name_for_func(name)
        if anime_name:
            anime = anilist.get_anime(anime_name)
            desc = anime.get("desc").strip()
            return CAPTION.format(
                anime.get("name_english").strip() or "",
                anime.get("airing_format").strip() or "",
                anime.get("average_score").strip() or "0",
                anime.get("airing_status").strip() or "",
                anime.get("starting_time").strip() or "",
                anime.get("ending_time").strip() or "",
                anime.get("duration").strip() or "",
                anime.get("airing_episodes").strip() or "",
                desc if len(desc) < 200 else desc[:200] + "...",
            )
    except Exception as error:
        print(error)
        return ""

async def get_proper_name_for_func(name):
    try:
        data = anitopy.parse(name)
        anime_name = data.get("anime_title")
        if anime_name and data.get("episode_number"):
            return (
                f"{anime_name} S{data.get('anime_season')}"
                if data.get("anime_season")
                else anime_name
            )
        return anime_name
    except Exception as error:
        print(error)
        return None

async def _rename(name, og=None):
    try:
        data = anitopy.parse(name)
        anime_name = data.get("anime_title")
        if anime_name and data.get("episode_number"):
            return (
                f"[S{data.get('anime_season') or 1}-{'E'+str(data.get('episode_number')) if data.get('episode_number') else ''}] {(await get_english(anime_name))} [Sub] @Roofiverse.mkv"
            )
        if anime_name:
            return (
                f"{(await get_english(anime_name))} [Sub] @Roofiverse.mkv"
                .replace("‘", "")
                .strip()
            )
        return name
    except Exception as error:
        print(error)
        return name
