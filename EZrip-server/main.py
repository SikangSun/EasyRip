import subprocess

from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from yt_dlp import YoutubeDL

app = FastAPI()


async def fake_video_streamer():
    for i in range(10):
        yield b"some fake video bytes"


def real_video_streamer(v):
    proc = subprocess.Popen(["./yt-dlp_macos", "-o", "-", "https://www.youtube.com/watch?v=" + v],
                            stdout=subprocess.PIPE)
    return proc.stdout


@app.get("/")
async def main(v):
    return StreamingResponse(real_video_streamer(v), media_type="application/octet-stream")


@app.get("/test")
async def main():
    URLS = ['https://www.youtube.com/watch?v=BaW_jenozKc']
    with YoutubeDL() as ydl:
        ydl.download(URLS)
    return
