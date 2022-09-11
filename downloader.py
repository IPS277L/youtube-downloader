import logging
import os
import sys

import enlighten
from moviepy.audio.io.AudioFileClip import AudioFileClip
from pathvalidate import sanitize_filename
from pytube import Playlist

from constants import MimeType, ProcessedType, FileType

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logger = logging.getLogger()


def download_playlist(playlist_url: str, download_folder: str) -> None:
    playlist = Playlist(url=playlist_url)
    logger.info(f'Processing playlist "{playlist.title}" from "{playlist.owner}"')

    manager = enlighten.get_manager()
    progress_bar = manager.counter(total=playlist.length, desc='Downloading:', unit='video')

    processed = []
    for video in playlist.videos:
        progress_bar.update()

        file_name = sanitize_filename(filename=video.title)
        file_path = f'{download_folder}/{file_name}'

        file_path_mp3 = f'{file_path}.{FileType.MP3}'
        file_path_mp4 = f'{file_path}.{FileType.MP4}'

        if os.path.isfile(path=file_path_mp3):
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
            highest_bitrate.download(output_path=download_folder, filename=f'{file_name}.{FileType.MP4}')

            file_mp4 = AudioFileClip(filename=file_path_mp4)
            file_mp4.write_audiofile(filename=file_path_mp3, logger=None)
            file_mp4.close()

            os.remove(file_path_mp4)

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
