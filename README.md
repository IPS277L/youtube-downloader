# YouTube Downloader

Python script providing functionality to download YouTube Playlists as .mp3 files.

## Requirements

Python 3.

## Installation
    
    git clone git@github.com:IPS277L/youtube-downloader.git
    cd youtube-downloader
    pip install -r requirements.txt

## Usage

    python main.py --playlist-url=https://www.youtube.com/playlist?list=PLx0sYbCqOb8TBPRdmBHs5Iftvv9TPboYG --download-folder=music/youtube

### kwargs
- --playlist-url - YouTube Playlist link, required.
- --download-folder - folder path where .mp3 will be saved, default value "youtube".
