from lib import tts, videosearcher, videoeditor, utils
from termcolor import colored
from dotenv import load_dotenv
from moviepy.config import change_settings
from uuid import uuid4
import os
from moviepy.editor import *

load_dotenv(".env")
change_settings({"IMAGEMAGICK_BINARY": os.getenv("IMAGEMAGICK_BINARY")})

        # Clean
utils.clean_dir("./temp/")
utils.clean_dir("./subtitles/")

with open('./scripts/1.txt', 'r') as arquivo:
    script = arquivo.read()

video_paths = []
print(colored('[-] \t Procurando videos', 'blue', 'on_white', ['bold', 'blink']))
search_terms = ["programming", "coding", "computer"]

video_urls = []
for search_term in search_terms: 
    video_urls.append(videosearcher.search_for_stock_videos(search_term))

for video_url in video_urls:
        try:
            saved_video_path = videoeditor.save_video(video_url)
            video_paths.append(saved_video_path)
        except Exception as e:
            print(colored("[-] Could not download video: " + video_url, "red"))
print(colored("[+] Videos downloaded!", "green"))

print(colored('[-] \t Gerando audio', 'blue', 'on_white', ['bold', 'blink']))
# Split script into sentences
sentences = script.split(". ")
# Remove empty strings
sentences = list(filter(lambda x: x != "", sentences))
paths = []
# Generate TTS for every sentence
for sentence in sentences:
    current_tts_path = f"./temp/{uuid4()}.mp3"
    tts.tts(sentence, "br_001", filename=current_tts_path)
    audio_clip = AudioFileClip(current_tts_path)
    paths.append(audio_clip)
print(colored('[+] \t Áudio Gerado', 'green', 'on_white', ['bold', 'blink']))

# Combine all TTS files using moviepy
final_audio = concatenate_audioclips(paths)
tts_path = f"./temp/{uuid4()}.mp3"
final_audio.write_audiofile(tts_path)
print(colored('[+] \t Áudio Combinado', 'green', 'on_white', ['bold', 'blink']))

# Generate subtitles
subtitles_path = videoeditor.generate_subtitles(tts_path)

# Concatenate videos
temp_audio = AudioFileClip(tts_path)
combined_video_path = videoeditor.combine_videos(video_paths, temp_audio.duration)

# Put everything together
final_video_path = videoeditor.generate_video(combined_video_path, tts_path, subtitles_path)

# Let user know
print(colored("[+] Video generated!", "green"))

print(colored(f"[+] Path: {final_video_path}", "green"))