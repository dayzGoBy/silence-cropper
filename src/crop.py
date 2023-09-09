import sys
import subprocess as sp
from os import linesep
from moviepy.editor import VideoFileClip, concatenate_videoclips
from pytube import YouTube as yt


minimum_duration = 1.0
threshold = -40

def download(link):
    with yt(link) as video:
        stream = video.streams.filter(mime_type="video/mp4", res="720p")[0]
        name = "/input/" + str(hash(link)) + ".mp4"
        stream.download(name)
        
        return name

def get_silence(file_in):
    output = sp.run(["ffmpeg", "-hide_banner", "-vn", "-i", file_in,
             "-af","silencedetect=n=" + str(threshold) + "dB:d=1",
             "-f","null","-"], capture_output=True)
    
    lines = output.stderr.decode("utf-8").split(linesep)
    tmp = []

    for line in lines:
        if ("silencedetect" in line):
            words = line.split(" ")
            for i in range (len(words)):
                if ("silence_start" in words[i]):
                    tmp.append(float(words[i + 1]))
                if "silence_end" in words[i]:
                    tmp.append(float(words[i + 1]))
    
    return list(zip(tmp[::2], tmp[1::2]))

def main():
    file_in = sys.argv[1]
    file_out = sys.argv[2]

    with VideoFileClip(file_in) as video:
        last = 0.0
        clips = []

        for start, end in get_silence(file_in):
            clips.append(video.subclip(last, start))
            last = end

        processed_video = concatenate_videoclips(clips)
        processed_video.write_videofile(
            file_out,
            fps=30,
            preset='ultrafast', # should be medium for better size
            codec='libx264',
            #threads=12,
        )

if __name__ == "__main__":
    main()