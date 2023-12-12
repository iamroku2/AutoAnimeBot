#    This file is part of the AutoAnime distribution.
#    Copyright (c) 2023 Kaif_00z
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, version 3.
#
#    This program is distributed in the hope that it will be useful, but
#    WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
#    General Public License for more details.
#
# License can be found in <
# https://github.com/kaif-00z/AutoAnimeBot/blob/main/LICENSE > .

from AnilistPython import Anilist
import anitopy
import asyncio
from .func import run_async

def your_function():
    # Some condition based on which you return anime[0] or None
    if some_condition:
        return anime[0]
    else:
        return None

# Function to create the caption
async def create_anime_caption(anime_name):
    anime_details = await get_anime_details(anime_name)
    if anime_details:
anilist = Anilist()
        caption = """


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
""".format(
            anime_details['title']['romaji'], 
            anime_details['format'], 
            anime_details['averageScore'], 
            anime_details['status'], 
            anime_details['startDate']['year'], 
            anime_details['endDate']['year'] if anime_details['endDate'] else "Ongoing",
            anime_details['duration'] + " mins" if anime_details['duration']
            else "Unknown",
            anime_details['episodes'] if anime_details['episodes'] else "Unknown",
            anime_details['description'] if anime_details['description'] else "Not available"
        )
        return caption
    else:
        return "Anime not found"

# Example usage
async def main():
    anime_name = "YourAnimeTitle"  # Replace with the actual anime title
    caption = await create_anime_caption(anime_name)
    print(caption)  # You can then use this caption for your messaging platform


@run_async
def get_poster(name):
    try:
        anime_name = get_proper_name_for_func(name)
        if anime_name:
            anime_id = anilist.get_anime_id(anime_name)
            return f"https://img.anili.st/media/{anime_id}"
    except Exception as error:
        print(error)
        return None
        
@run_async
def get_cover(name):
    try:
        # Returns the custom image URL directly
        return "https://telegra.ph/file/4f5ecffbedab637ec2a2b.jpg"
    except Exception as error:
        print(error)
        return None

@run_async
def get_caption(name):
    try:
        anime_name = get_proper_name_for_func(name)
        if anime_name:
            anime = anilist.get_anime(anime_name)
            desc = anime.get("desc").strip()
            return CAPTION.format(
                anime.get("name_english").strip() or "",
                desc if len(desc) < 763 else desc[:760] + "...",
            )
    except BaseException:
        return ""




def get_proper_name_for_func(name):
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
    except BaseException:
        return None


async def _rename(name, og=None):
    try:
        data = anitopy.parse(name)
        anime_name = data.get("anime_title")
        if anime_name and data.get("episode_number"):
            return (
                f"[S{data.get('anime_season') or 1}-{data.get('episode_number') or ''}] {(await get_english(anime_name))} [1080p] @OngoingAnime_Supernova.mkv".replace(
                    "‘", ""
                )
                .replace("’", "")
                .strip()
            )
        if anime_name:
            return (
                f"{(await get_english(anime_name))} [1080p] @OngoingAnime_Supernova.mkv".replace(
                    "‘", ""
                )
                .replace("’", "")
                .strip()
            )
        return name
    except Exception as error:
        print(error)
        return name
