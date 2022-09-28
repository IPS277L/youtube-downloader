from argparse import Namespace
from typing import Optional

from spotipy import Spotify, SpotifyClientCredentials


class MetadataCrawler:
    def __init__(self, args: Namespace):
        ...

    def _serialize(self, metadata: dict) -> dict:
        raise NotImplemented

    def search(self, name: str) -> Optional[dict]:
        raise NotImplemented


class SpotifyCrawler(MetadataCrawler):
    _client_id = None
    _client_secret = None

    _client = None

    def __init__(self, args: Namespace):
        super().__init__(args=args)

        self._client_id = args.spotify[0]
        self._client_secret = args.spotify[1]

        auth_manager = SpotifyClientCredentials(client_id=self._client_id, client_secret=self._client_secret)
        self._client = Spotify(auth_manager=auth_manager)

    def _serialize(self, metadata: dict) -> dict:
        serialized = {
            'track_number': str(metadata.get('track_number', '')),
            'name': metadata.get('name', ''),
            'artist': metadata.get('artists', [{}])[0].get('name', ''),
            'album': metadata.get('album').get('name', ''),
            'album_artist': metadata.get('album', {}).get('artists', [{}])[0].get('name', ''),
            'release_date': metadata.get('album', {}).get('release_date', '')
        }

        cover = max(metadata.get('album', {}).get('images', [{}]), key=lambda x: x.get('height'))
        if cover:
            serialized['cover_url'] = cover.get('url')

        return serialized

    def search(self, name: str) -> Optional[dict]:
        search_results = self._client.search(q=name, limit=1)
        if search_results.get('tracks', {}).get('total', 0) == 0:
            return

        metadata = search_results.get('tracks', {}).get('items', [{}])[0]
        serialized = self._serialize(metadata=metadata)

        return serialized
