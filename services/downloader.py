import yt_dlp

def download_audio_from_youtube(url):
    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": "./audio/%(id)s.%(ext)s",
        "quiet": True,
        "noplaylist": True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        return info['requested_downloads'][0]['filepath']