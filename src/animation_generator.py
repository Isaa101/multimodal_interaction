#!/usr/bin/env python3

from moviepy import VideoFileClip
import numpy as np
import os
import sys
from PIL import Image
from datetime import timedelta

SAVING_FPS = 20

def format_timedelta(td):
    result = str(td)
    try:
        result, ms = result.split(".")
    except ValueError:
        return (result + ".00").replace(":", "-")

    ms = int(ms)
    ms = round(ms/1e4)
    return f"{result}.{ms:02}".replace(":", "-")

def main(video_file):
    video_clip = VideoFileClip(video_file)
    filename, _ = os.path.splitext(video_file)
    if not os.path.isdir(filename):
        os.mkdir(filename)

    video_fps = min(video_clip.fps, SAVING_FPS)
    step = 1/video_clip.fps if video_fps == 0 else 1/video_fps

    for current_duration in np.arange(0, video_clip.duration, step):
        frame_duration_formatted = format_timedelta(timedelta(seconds=current_duration))
        frame_filename = os.path.join(filename, f"frame{frame_duration_formatted}.jpg")
        video_clip.save_frame(frame_filename, current_duration)
        im = Image.open(frame_filename)
        width, height = im.size
        aspect_ratio = width/height
        im = im.resize((int(aspect_ratio*728),728))
        im.save(frame_filename)

if __name__=='__main__':
    main('animations/' + sys.argv[1])
