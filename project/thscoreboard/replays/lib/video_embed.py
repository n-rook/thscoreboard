from urllib.parse import urlparse, parse_qs, ParseResult


def _get_twitch_embed_link(split_url: ParseResult):
    path = split_url.path.strip("/").split("/")
    if path[0] == "videos":
        video_id = path[1]
        return f"https://player.twitch.tv/?video=v{video_id}&parent=www.silentselene.net&autoplay=false"
    if path[1] == "clip" and len(path) == 3:
        clip_id = path[2]
        return f"https://clips.twitch.tv/embed?clip={clip_id}&parent=www.silentselene.net&autoplay=false"


def _get_yt_embed_link(split_url: ParseResult):
    path = split_url.path[1:].split("/")

    if path[0] not in ["watch", "shorts"]:
        return

    # Having a ?v=video_id_2 at the end of a /shorts/video_id URL will redirect to /watch?v=video_id_2
    query = parse_qs(split_url.query)
    if "v" in query:
        # If v is specified multiple times in the query string, YouTube will always pick the first one
        # Doing weird things with slashes and question marks after the video ID does not affect embedding
        video_id = query["v"][0]
        return f"https://www.youtube.com/embed/{video_id}"
    elif path[0] == "shorts":
        video_id = path[1]
        return f"https://www.youtube.com/embed/{video_id}"


def _get_bilibili_embed_link(split_url: ParseResult):
    path = split_url.path.strip("/").split("/")
    if path[0] == "video" and len(path) == 2:
        video_id = path[1]
        return f"https://player.bilibili.com/player.html?bvid={video_id}&autoplay=false"

"""
Constructs an embed link from a video URL from any of the supported video websites.
Returns None if no embed link can be generated
"""
def get_video_embed_link(url: str):
    try:
        split_url = urlparse(url)
        if split_url.hostname == "youtu.be":
            # youtu.be/video_id/random_other_junk is perfectly valid
            path = split_url.path[1:].split("/")
            video_id = path[0]
            return f"https://www.youtube.com/embed/{video_id}"
        elif split_url.hostname == "www.youtube.com":
            return _get_yt_embed_link(split_url)
        elif split_url.hostname == "www.twitch.tv":
            return _get_twitch_embed_link(split_url)
        elif split_url.hostname == "www.bilibili.com":
            return _get_bilibili_embed_link(split_url)
    except (KeyError, IndexError):
        return
