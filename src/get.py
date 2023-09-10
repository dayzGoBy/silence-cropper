import sys
from pytube import YouTube as yt


def download(link, defpath=None):
    video = yt(link)
    stream = video.streams.filter(mime_type="video/mp4", res="720p")[0]
    name = ("input/YOUTUBE"
            if defpath is None else defpath)
    stream.download(name)

    return name + "/" + stream.title


if __name__ == "__main__":
    if len(sys.argv) == 1:
        exit("No arguments given")

    print("Downloading")
    loc = download(sys.argv[1], defpath=(
        None if len(sys.argv) == 2 else sys.argv[2]))
    print("Video saved as " + loc)
