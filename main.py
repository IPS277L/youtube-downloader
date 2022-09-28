import argparse

from constants import MetadataSource
from downloader import download_playlist

parser = argparse.ArgumentParser()
parser.add_argument('--playlist-url', type=str, required=True)
parser.add_argument('--download-folder', type=str, default='youtube', required=False)

parser.add_argument('--metadata-source', type=str, choices=[MetadataSource.SPOTIFY], required=False)
parser.add_argument('--spotify', type=str, nargs=2, required=False)


def main() -> None:
    args = parser.parse_args()
    download_playlist(args=args)


if __name__ == "__main__":
    main()
