import tkinter as tk
from tkinter import filedialog
from pygame import mixer
import threading

mixer.init()  # Initialize the mixer

class MusicPlayer:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple MP3 Player")

        self.playlist = []
        self.current_song_index = 0
        self.paused = False

        # GUI Components
        self.add_button = tk.Button(root, text="Add Song", command=self.add_song)
        self.add_button.pack()

        self.play_button = tk.Button(root, text="Play", command=self.play_song)
        self.play_button.pack()

        self.pause_button = tk.Button(root, text="Pause", command=self.pause_song)
        self.pause_button.pack()

        self.stop_button = tk.Button(root, text="Stop", command=self.stop_song)
        self.stop_button.pack()

    def add_song(self):
        files = filedialog.askopenfilenames(filetypes=[("MP3 files", "*.mp3")])
        for file in files:
            self.playlist.append(file)

    def play_song(self):
        if not self.playlist:
            return
        if self.paused:
            mixer.music.unpause()
            self.paused = False
        elif not mixer.music.get_busy():
            print("hi")
            mixer.music.load(self.playlist[self.current_song_index])
            mixer.music.play()
        

    def pause_song(self):
        if mixer.music.get_busy():
            mixer.music.pause()
            self.paused = True

    def stop_song(self):
        mixer.music.stop()


root = tk.Tk()
player = MusicPlayer(root)
root.mainloop()