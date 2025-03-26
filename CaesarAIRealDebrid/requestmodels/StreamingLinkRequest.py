from pydantic import BaseModel,root_validator
from typing import Optional
class StreamingLinkRequest(BaseModel):
    magnet_link:Optional[str] = None
    torrent_link:Optional[str] = None

    @root_validator(pre=True)
    def validate_links(cls, values):
        magnet_link = values.get("magnet_link")
        torrent_link = values.get("torrent_link")

        if not magnet_link and not torrent_link:
            raise ValueError("Either 'magnet_link' or 'torrent_link' must be provided.")
        
        return values