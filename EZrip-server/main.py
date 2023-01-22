import subprocess
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from yt_dlp import YoutubeDL
import json
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware import Middleware


# CORS STUFF
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:5173",
    "http://127.0.0.1:5173"
]

middleware = [
    Middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"]
    )
]

app = FastAPI(middleware=middleware)


async def fake_video_streamer():
    for i in range(10):
        yield b"some fake video bytes"


def real_video_streamer(v):
    proc = subprocess.Popen(["./yt-dlp", "-o", "-", "https://www.youtube.com/watch?v=" + v],
                            stdout=subprocess.PIPE)
    return proc.stdout


@app.get("/")
async def main(v):
    return StreamingResponse(real_video_streamer(v), media_type="application/octet-stream")


@app.get("/get_metadata")
async def get_video_metadata(v):
    url = 'https://www.youtube.com/watch?v=' + v

    # ℹ️ See help(yt_dlp.YoutubeDL) for a list of available options and public functions
    ydl_opts = {}
    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)

        # ℹ️ ydl.sanitize_info makes the info json-serializable
        return json.dumps(ydl.sanitize_info(info))
