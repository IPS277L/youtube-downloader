import logging
import os
import sys

import enlighten
from pathvalidate import sanitize_filename
from pytube import Playlist, YouTube

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logger = logging.getLogger()


def download_playlist(playlist_url: str, download_folder: str) -> None:
    playlist = Playlist(url=playlist_url)
    logger.info(f'Processing playlist "{playlist.title}" from "{playlist.owner}"')

    manager = enlighten.get_manager()
    progress_bar = manager.counter(total=playlist.length, desc='Downloading:', unit='video')

    skipped, errors = [], []
    for video_url in playlist.video_urls:
        progress_bar.update()

        youtube_video = YouTube(video_url)
        file_name = sanitize_filename(f'{youtube_video.title}.mp3')

        if os.path.isfile(f'{download_folder}/{file_name}'):
            logger.warning(f'File "{file_name}" already exists, skipping...')
            skipped.append({'video_url': video_url, 'file_name': file_name})
            continue

        try:
            streams = youtube_video.streams.filter(only_audio=True, mime_type='audio/mp4')
            highest_bitrate = max(streams, key=lambda x: x.bitrate)
            highest_bitrate.download(output_path=download_folder, filename=file_name)

        except Exception as exc:
            logger.error(f'File "{file_name}" can not be proceed, skipping...')
            errors.append({'video_url': video_url, 'file_name': file_name, 'errors': [str(exc)]})

    logger.info(f'Skipped: {len(skipped)}, errors: {len(errors)}')
