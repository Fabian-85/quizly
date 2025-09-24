import yt_dlp

ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": "./audio/%(id)s.%(ext)s",
        "quiet": True,
        "noplaylist": True,
    }

def download_audio_from_youtube(url):

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            return info['requested_downloads'][0]['filepath']
        
    except Exception as e:
        raise Exception(f"Error downloading audio: {str(e)}")