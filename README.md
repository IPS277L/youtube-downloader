# YouTube Downloader

Python script providing functionality to download YouTube Playlists as .mp3 files


## Installation
    
    git clone git@github.com:IPS277L/youtube-downloader.git
    cd youtube-downloader
    pip install -r requirements.txt


## Usage

    python main.py
    --playlist-url https://www.youtube.com/playlist?list=PLx0sYbCqOb8TBPRdmBHs5Iftvv9TPboYG
    --download-folder music/youtube
    --metadata-source spotify
    --spotify client-id client-secret


### **kwargs

- --playlist-url - string, required;
- --download-folder - string, default value "youtube";
- --metadata-source - string, available options: "spotify";
- --spotify - multi string, client-id and client-secret;


## Metadata Crawling

All downloaded .mp3 files have empty id tags. To fix it you can use metadata crawling functionality. 
Currently, only Spotify is supported. Due to private API restrictions please use this guide to get client-id and
client-secret for usage: [App Settings | Spotify for Developers](https://developer.spotify.com/documentation/general/guides/authorization/app-settings/)


## Known Issues

- "... is age restricted, and can't be accessed without logging in". Required YouTube authorization, 
probably will be added in future releases;
- "KeyError: streamingData". The rare issue caused by "pytube" library, will be investigated;


## TODO

- Metadata crawling from different sources;
- Metadata crawling as a standalone module;
- YouTube authorization;
- Pipeline for builds;

