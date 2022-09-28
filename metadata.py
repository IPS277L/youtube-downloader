from argparse import Namespace
from typing import Optional

import requests
from mutagen.id3 import ID3, APIC, TIT2, TRCK, TPE1, TALB, TPE2, TYER, Encoding

from constants import MimeType, FileType, MetadataSource
from spotify import MetadataCrawler, SpotifyCrawler


def get_metadata_crawler(args: Namespace) -> Optional[MetadataCrawler]:
    crawlers = {
        MetadataSource.SPOTIFY: SpotifyCrawler
    }

    crawler_class = crawlers.get(args.metadata_source)
    if not crawler_class:
        return

    crawler_instance = crawler_class(args=args)
    return crawler_instance


def attach_mp3_metadata(args: Namespace, file_path: str) -> None:
    metadata_crawler = get_metadata_crawler(args)
    if not metadata_crawler:
        return

    id3 = ID3(file_path)
    file_name = id3.filename.split(f'.{FileType.MP3}')[0].split('/')[-1]

    metadata = metadata_crawler.search(name=file_name)
    if not metadata:
        return

    id3_frames = [
        TRCK(encoding=Encoding.UTF8, text=metadata['track_number']),
        TIT2(encoding=Encoding.UTF8, text=metadata['name']),
        TPE1(encoding=Encoding.UTF8, text=metadata['artist']),
        TALB(encoding=Encoding.UTF8, text=metadata['album']),
        TPE2(encoding=Encoding.UTF8, text=metadata['album_artist']),
        TYER(encoding=Encoding.UTF8, text=metadata['release_date'])
    ]

    cover_url = metadata.get('cover_url')
    if cover_url:
        cover_data = requests.get(cover_url).content
        apic = APIC(encoding=Encoding.UTF8, mimetype=MimeType.IMAGE_JPEG, type=3, desc='Front cover', data=cover_data)
        id3_frames.append(apic)

    for frame in id3_frames:
        id3.add(frame)

    id3.save(v2_version=3)
