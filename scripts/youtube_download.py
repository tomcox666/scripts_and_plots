import yt_dlp
import moviepy.editor as mp
import os
import tkinter as tk
from tkinter import filedialog

def play_video(video_path):
    try:
        clip = mp.VideoFileClip(video_path)
        clip.preview()
    except Exception as e:
        print(f"Error playing video: {e}")

def download_and_play(video_url):
    try:
        ydl_opts = {
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
            'outtmpl': '%(title)s.%(ext)s',
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=True)
            video_path = ydl.prepare_filename(info)

        if os.path.exists(video_path):
            play_video(video_path)
        else:
            print("Error: Video download failed or file not found.")

    except Exception as e:
        print(f"Error: {e}")

def open_file_dialog():
    root = tk.Tk()
    root.withdraw()

    file_path = filedialog.askopenfilename(filetypes=[("Video files", "*.mp4")])
    if file_path:
        play_video(file_path)

    root.destroy()

video_url = input("Enter YouTube URL or type 'local' to open a local file: ")

if video_url.lower() == 'local':
    open_file_dialog()
else:
    download_and_play(video_url)