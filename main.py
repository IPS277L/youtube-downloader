import argparse

from downloader import download_playlist

parser = argparse.ArgumentParser()
parser.add_argument('--playlist-url', type=str, required=True)
parser.add_argument('--download-folder', type=str, required=False, default='youtube')


def main() -> None:
    args = parser.parse_args()
    download_playlist(playlist_url=args.playlist_url, download_folder=args.download_folder)


if __name__ == "__main__":
    main()
