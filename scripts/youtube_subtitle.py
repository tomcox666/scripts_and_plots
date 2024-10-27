import yt_dlp
from pydub import AudioSegment
import speech_recognition as sr
import os


def transcribe_youtube_video(youtube_url):
    """
    Transcribes the first 30 seconds of a YouTube video.

    Args:
        youtube_url: The URL of the YouTube video.

    Returns:
        A string containing the transcribed text.
    """

    # Download the audio as an MP3 file
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'audio.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([youtube_url])

    # Find the downloaded MP3 file
    mp3_file = None
    for file in os.listdir('.'):
        if file.startswith('audio') and file.endswith('.mp3'):
            mp3_file = file
            break

    if not mp3_file:
        raise FileNotFoundError("MP3 file not found after downloading.")

    # Load the MP3 file and trim to the first 30 seconds
    audio = AudioSegment.from_mp3(mp3_file)
    audio = audio[:30000]  # 30 seconds = 30000 milliseconds

    # Convert to WAV format
    audio.export("audio.wav", format="wav")

    # Transcribe the WAV file
    recognizer = sr.Recognizer()
    with sr.AudioFile("audio.wav") as source:
        audio_data = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio_data)
        except sr.UnknownValueError:
            text = "Could not understand audio"
        except sr.RequestError as e:
            text = f"Could not request results from Google Speech Recognition service; {e}"

    # Save the transcription to a text file
    with open("transcription.txt", "w") as f:
        f.write(text)

    # Clean up temporary files
    os.remove(mp3_file)
    os.remove("audio.wav")

    return text


# Example usage
youtube_url = input("Enter the YouTube URL: ")
transcription = transcribe_youtube_video(youtube_url)
print("Transcription saved to transcription.txt")
