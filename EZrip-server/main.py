import subprocess
from fastapi import FastAPI, Response
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
    "http://127.0.0.1:5173",
    "https://easy-rip-sses.vercel.app",
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
        print(f)
        f = f.replace(" ", "+")
        proc = subprocess.Popen(["./yt-dlp", "-o", "-", "-f", str(f), "--ffmpeg-location", ".",
                                 "https://www.youtube.com/watch?v=" + v],
                                stdout=subprocess.PIPE)

    return proc.stdout


@app.get("/get_video")
async def get_video(v, f, n=None):
    url = 'https://www.youtube.com/watch?v=' + v

    ydl_opts = {}
    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        metadata = ydl.sanitize_info(info)

    ext = "mkv"

    for frm in metadata['formats']:
        if frm['format_id'] == f:
            ext = frm['ext']

    if n is None:
        filename = metadata['title'] + "." + ext
    else:
        filename = n + "." + ext
    return StreamingResponse(video_streamer(v, f), media_type="application/octet-stream",
                             headers={"Content-Disposition": "filename=\"{filename}\"".format(filename=filename)})


@app.get("/get_metadata")
async def get_video_metadata(v):
    url = 'https://www.youtube.com/watch?v=' + v

    # ?????? See help(yt_dlp.YoutubeDL) for a list of available options and public functions
    ydl_opts = {}
    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)

        # ?????? ydl.sanitize_info makes the info json-serializable
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
            filesize = f['filesize']

            return_json['formats'].append(
                {'desc': desc, 'ext': ext, 'id': format_id, 'is_video': is_video, 'is_default': False,
                 'height': height, 'filesize': filesize})

        highest_res_no_combine_height = 0
        highest_res_no_combine_id = 0
        for f in return_json['formats']:
            if f['is_video']:
                if f['height'] > highest_res_no_combine_height and "+" not in f['id']:
                    highest_res_no_combine_height = f['height']
                    highest_res_no_combine_id = f['id']

        # search for that id
        for idx, f in enumerate(return_json['formats']):
            if f['id'] == highest_res_no_combine_id:
                return_json['formats'][idx]['is_default'] = True

        return return_json
