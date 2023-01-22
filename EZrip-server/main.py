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


def video_streamer(v, f):
    if f == 0:
        proc = subprocess.Popen(["./yt-dlp", "-o", "-", "https://www.youtube.com/watch?v=" + v],
                                stdout=subprocess.PIPE)
    else:
        proc = subprocess.Popen(["./yt-dlp", "-o", "-", "-f", str(f), "https://www.youtube.com/watch?v=" + v],
                                stdout=subprocess.PIPE)

    return proc.stdout


@app.get("/get_video")
async def get_video(v, f: int = 0):
    return StreamingResponse(video_streamer(v, f), media_type="application/octet-stream")


@app.get("/get_metadata")
async def get_video_metadata(v):
    url = 'https://www.youtube.com/watch?v=' + v

    # ℹ️ See help(yt_dlp.YoutubeDL) for a list of available options and public functions
    ydl_opts = {}
    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)

        # ℹ️ ydl.sanitize_info makes the info json-serializable
        metadata = ydl.sanitize_info(info)
        # print(metadata)
        return_json = {'formats': [], 'title': metadata['title'], 'uploader': metadata['uploader'],
                       'duration_string': metadata['duration_string'], 'like_count': metadata['like_count'],
                       'upload_date': metadata['upload_date'], 'view_count': metadata['view_count']}
        for f in metadata['formats']:
            # skips videos without audio
            # does not take into account videos without audio in the first place ???
            # check if height is integer
            if isinstance(f['height'], int):
                height = f['height']
                is_video = True
            else:
                height = 0
                is_video = False

            format_id = f['format_id']

            # exclude storyboards
            if f['format_note'] == "storyboard":
                continue

            if f['vcodec'] != "none" and f['acodec'] == "none":
                if height <= 720:
                    continue
                else:
                    # height greater than 720 but has no audio
                    format_id = str(f['format_id']) + "+" + "bestaudio"

            i = f['format'].index(' ')
            desc = f['format'][f['format'].index(' ', i + 1) + 1:]
            ext = f['ext']

            return_json['formats'].append({'desc': desc, 'ext': ext, 'id': format_id, 'is_video': is_video})

        return return_json
