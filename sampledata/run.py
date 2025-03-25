# importing element tree
# under the alias of ET
import xml.etree.ElementTree as ET
import requests
from io import BytesIO
from typing import Optional
from CaesarAITorrentParsers.CaesarAIJackett import CaesarAIJackett
from CaesarAIRealDebird import CaesarAIRealDebrid
import asyncio
url = "http://localhost:9117/api/v2.0/indexers/all/results/torznab?apikey=fyx7w7eb8ymo3h4kd6bgrvajtf2ljndo&t=tvsearch&q=Solo Leveling&season=1&ep=7"
url2 = "http://localhost:9117/api/v2.0/indexers/all/results/torznab?apikey=fyx7w7eb8ymo3h4kd6bgrvajtf2ljndo&t=tvsearch&q=The Seven Deadly Sins: Four Knights of the Apocalypse&season=2&ep=1"
url3 = "http://localhost:9117/api/v2.0/indexers/all/results/torznab?apikey=fyx7w7eb8ymo3h4kd6bgrvajtf2ljndo&t=tvsearch&q=classroom of the elite&season=3&ep=9"

async def main():
    response = requests.get(url)
    caejackett = CaesarAIJackett(response.content)
    caejackett.get_torrent_info()
    torrentinfo = caejackett.get_single_episodes()
    magnet_url = torrentinfo[0].magnet_link
    crd = CaesarAIRealDebrid()
    _id = crd.add_magnet(magnet_url)
    print(crd.get_progress_and_status(_id))
    crd.select_files(_id)
    print(crd.get_progress_and_status(_id))
    response = await crd.get_streaming_links(_id)
    print(response)

asyncio.run(main())
#print(f"Name:{torrentinfo[0].displayname}\nTitle:{torrentinfo[0].title}\nSeason:{torrentinfo[0].season}\nEpisode:{torrentinfo[0].episode}\nLanguage:{torrentinfo[0].languages}\nResults:{len(torrentinfo)}\nMagnet:{torrentinfo[0].magnet_link}")