import os
import PySimpleGUI as sg
from pytube import YouTube, Playlist
from moviepy.editor import AudioFileClip

# Define your default download path here
default_download_path = os.path.join(os.path.expanduser("~"), "Downloads")

layout = [
    [sg.Text('YouTube Video or Playlist URL:'), sg.InputText(key='URL'), sg.FolderBrowse('Select Folder', target='FOLDER'), sg.InputText(default_text=default_download_path, key='FOLDER')],
    [sg.Button('Download Video', key='DOWNLOAD_VIDEO'), sg.Button('Download Playlist', key='DOWNLOAD_PLAYLIST')],
    [sg.Output(size=(60, 10))]
]

window = sg.Window('YouTube Playlist to MP3 Converter', layout)

def download_and_convert_video(url, download_path):
    video = YouTube(url)
    print(f'Downloading: {video.title}')
    stream = video.streams.filter(only_audio=True).first()
    out_file = stream.download(output_path=download_path)
    mp3_file = os.path.join(download_path, stream.default_filename.replace(".mp4", ".mp3"))
    video_clip = AudioFileClip(out_file)
    video_clip.write_audiofile(mp3_file)
    video_clip.close()
    os.remove(out_file)  # Remove the .mp4 file after conversion
    print(f'Downloaded and converted: {mp3_file}')

def download_and_convert_playlist(url, download_path):
    playlist = Playlist(url)
    print(f'Downloading: {playlist.title}')
    for video in playlist.videos:
        stream = video.streams.filter(only_audio=True).first()
        out_file = stream.download(output_path=download_path)
        mp3_file = os.path.join(download_path, stream.default_filename.replace(".mp4", ".mp3"))
        video_clip = AudioFileClip(out_file)
        video_clip.write_audiofile(mp3_file)
        video_clip.close()
        os.remove(out_file)  # Remove the .mp4 file after conversion
        print(f'Downloaded and converted: {mp3_file}')

while True:
    event, values = window.read()
    if event == sg.WINDOW_CLOSED:
        break
    elif event == 'DOWNLOAD_VIDEO':
        url = values['URL']
        download_path = values['FOLDER']
        if not url:
            print('Please enter a YouTube Video URL')
        else:
            try:
                download_and_convert_video(url, download_path)
            except Exception as e:
                print(f'Failed to download and convert.\n{e}')
    elif event == 'DOWNLOAD_PLAYLIST':
        url = values['URL']
        download_path = values['FOLDER']
        if not url:
            print('Please enter a YouTube Playlist URL')
        else:
            try:
                download_and_convert_playlist(url, download_path)
            except Exception as e:
                print(f'Failed to download and convert.\n{e}')

window.close()