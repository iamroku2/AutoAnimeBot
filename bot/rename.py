import anitopy
from AnilistPython import Anilist
from .func import run_async
import requests

ANIME_QUERY = """
query ($id: Int, $idMal:Int, $search: String) {
  Media (id: $id, idMal: $idMal, search: $search, type: ANIME) {
    id
    idMal
    title {
      romaji
      english
      native
    }
    format
    status
    episodes
    duration
    countryOfOrigin
    source (version: 2)
    trailer {
      id
      site
    }
    genres
    tags {
      name
    }
    averageScore
    relations {
      edges {
        node {
          title {
            romaji
            english
          }
          id
        }
        relationType
      }
    }
    nextAiringEpisode {
      timeUntilAiring
      episode
    }
    isAdult
    isFavourite
    mediaListEntry {
      status
      score
      id
    }
    siteUrl
  }
}
"""

ANIME_DB = {}


async def return_json_senpai(query: str, vars_: dict):
    url = "https://graphql.anilist.co"
    anime = vars_["search"]
    db = ANIME_DB.get(anime)

    if db:
        return db
    data = requests.post(url, json={"query": query, "variables": vars_}).json()
    ANIME_DB[anime] = data

    return data


temp = []


async def get_anime(vars_, less):
    if 1 == 1:
        result = await return_json_senpai(ANIME_QUERY, vars_)

        error = result.get("errors")
        if error:
            error_sts = error[0].get("message")
            print([f"[{error_sts}]"])
            print(vars_)
            data = temp[0]
            temp.pop(0)
        else:
            data = result["data"]["Media"]
            temp.append(data)
        idm = data.get("id")
        title = data.get("title")
        tit = title.get("english")
        if tit == None:
            tit = title.get("romaji")

        tit = format_text(tit)
        title_img = f"https://img.anili.st/media/{idm}"

        if less == True:
            return idm, title_img, tit

        return data


async def get_anime_img(query):
    vars_ = {"search": query}

    return await get_anime(vars_, less=True)


def get_anime_name(title):
    x = title.split(" - ")[-1]
    x = title.replace(x, "").replace("-", "").strip()
    x = x.split(" ")
    x = x[:4]
    y = ""
    for i in x:
        y += i + " "
    return y


atext = """
📺 **{}**
  ({})

🎭 Genre : `{}`
🧬 Type : `{}`
📡 Status : `{}`
🗓 Episodes : `{}`
💾 Duration : `{}`
⭐️ Rating : `{}/100`
"""


async def get_anilist_data(name):
    vars_ = {"search": name}
    data = await get_anime(vars_, less=False)

    id_ = data.get("id")
    title = data.get("title")
    form = data.get("format")
    status = data.get("status")
    episodes = data.get("episodes")
    duration = data.get("duration")
    trailer = data.get("trailer")
    genres = data.get("genres")
    averageScore = data.get("averageScore")
    img = f"https://img.anili.st/media/{id_}"

    # title
    title1 = title.get("english")
    title2 = title.get("romaji")

    if title2 == None:
        title2 = title.get("native")

    if title1 == None:
        title1 = title2

    # genre

    genre = ""

    for i in genres:
        genre += i + ", "

    genre = genre[:-2]

    caption = atext.format(
        title1, title2, genre, form, status, episodes, duration, averageScore
    )

    if trailer != None:
        ytid = trailer.get("id")
        site = trailer.get("site")
    else:
        site = None

    if site == "youtube":
        caption += f"\n[Trailer](https://www.youtube.com/watch?v={ytid}) | [More Info](https://anilist.co/anime/{id_})"
    else:
        caption += f"\n[More Info](https://anilist.co/anime/{id_})"

    return img, caption
        
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
