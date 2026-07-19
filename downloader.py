import yt_dlp
import os
import uuid


def download_video(url):

    folder = "downloads"

    if not os.path.exists(folder):
        os.mkdir(folder)

    filename = os.path.join(
        folder,
        str(uuid.uuid4()) + ".%(ext)s"
    )

    options = {
        "outtmpl": filename,
        "format": "best",
        "noplaylist": True
        "proxy": "http://185.195.122.2:8080
    }

    with yt_dlp.YoutubeDL(options) as ydl:
        info = ydl.extract_info(url, download=True)
        file_path = ydl.prepare_filename(info)

    return file_path
