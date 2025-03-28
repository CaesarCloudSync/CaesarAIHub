from pydantic import  BaseModel,computed_field
from typing import List,Optional,Union
import PTN
from pathlib import Path
import re
class StreamItem(BaseModel):
    filename:str
    hoster:str
    # This is a possible link with japanes and english subtitles. https://31.stream.real-debrid.com/t/FEWQEDJFTRDMI20/jp1/eng1/eac3/full.mpd
{
    "filename": "Dragon Ball DAIMA",
    "hoster": "rd",
    "link": "https://real-debrid.com/d/L26O4XSWGAYI62D2",
    "type": "show",
    "season": "01",
    "episode": "06",
    "year": "none",
    "duration": 1435.776,
    "bitrate": 5318327,
    "size": 954490822,
    "details": {
        "video": {
            "und1": {
                "stream": "0:0",
                "lang": "Unknown",
                "lang_iso": "und",
                "codec": "h264",
                "colorspace": "yuv420p",
                "width": 0,
                "height": 0
            }
        },
        "audio": {
            "eng1": {
                "stream": "0:1",
                "lang": "English",
                "lang_iso": "eng",
                "codec": "eac3",
                "sampling": 48000,
                "channels": 2
            },
            "jpn1": {
                "stream": "0:2",
                "lang": "Japanese",
                "lang_iso": "jpn",
                "codec": "eac3",
                "sampling": 48000,
                "channels": 2
            }
        },
        "subtitles": {
            "eng1": {
                "stream": "0:3",
                "lang": "English",
                "lang_iso": "eng",
                "type": "SRT"
            }
        }
    },
    "poster_path": "https://image.tmdb.org/t/p/w185/8tpLyWAmYhe1D0d62gV3CWFDu2f.jpg",
    "backdrop_path": "https://image.tmdb.org/t/p/w1280/oUmWLyeko3kYdUr8DBLIsxwcugl.jpg",
    "baseUrl": "https://31.stream.real-debrid.com/t/FEWQEDJFTRDMI20/eng1/none/aac/full",
    "availableFormats": {
        "apple": "m3u8",
        "dash": "mpd",
        "liveMP4": "mp4",
        "h264WebM": "webm"
    },
    "availableQualities": {
        "Original": "full"
    },
    "modelUrl": "https://31.stream.real-debrid.com/t/FEWQEDJFTRDMI20/{audio}/{subtitles}/{audioCodec}/{quality}.{format}",
    
    "host": "31.stream.real-debrid.com"
}