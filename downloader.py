import logging
import os
import sys
from time import sleep

import enlighten
from pathvalidate import sanitize_filename
from pytube import Playlist

from constants import MimeType, ProcessedType

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logger = logging.getLogger()


def download_playlist(playlist_url: str, download_folder: str, timeout: int) -> None:
    playlist = Playlist(url=playlist_url)
    logger.info(f'Processing playlist "{playlist.title}" from "{playlist.owner}"')

    manager = enlighten.get_manager()
    progress_bar = manager.counter(total=playlist.length, desc='Downloading:', unit='video')

    processed = []
    for video in playlist.videos:
        progress_bar.update()

        file_name = sanitize_filename(f'{video.title}.mp3')

        if os.path.isfile(f'{download_folder}/{file_name}'):
            logger.warning(f'File "{file_name}" already exists, skipping...')
            processed.append({
                'video_id': video.video_id,
                'file_name': file_name,
                'type': ProcessedType.SKIPPED
            })

            continue

        try:
            streams = video.streams.filter(only_audio=True, mime_type=MimeType.AUDIO_MP4)
            highest_bitrate = max(streams, key=lambda x: x.bitrate)
            highest_bitrate.download(output_path=download_folder, filename=file_name)

            logger.info(f'File "{file_name}" successfully downloaded')
            result = {
                'video_id': video.video_id,
                'file_name': file_name,
                'type': ProcessedType.DOWNLOADED
            }

        except Exception as exc:
            logger.error(f'File "{file_name}" can not be proceed: {str(exc)}')
            result = {
                'video_id': video.video_id,
                'file_name': file_name,
                'type': ProcessedType.ERROR,
                'errors': [str(exc)]
            }

        processed.append(result)
        sleep(timeout)
