import ctypes.wintypes
import argparse
import os
import ffmpeg
from pathlib import Path


def main():
    args = setup()
    scan_dir = Path(args.video_directory)
    vids = get_all_shadowplay_videos(scan_dir)
    print(f"Found {len(vids)} Shadowplay files in {scan_dir}")
    # num_vids_to_process = min(len(vids), 1)
    # try:
    #     num_vids_to_process = int(
    #         input(
    #             f"Please enter how many of the found videos to convert. ([1]-{len(vids)}): "
    #         )
    #     )
    # except:
    #     print("Invalid ")
    # print(f"\nSelected {num_vids_to_process} recordings to convert to MP3")
    # concat = (
    #     input(
    #         "This tool can join recent recordings together into single audio files, join selected recordings into a single file? y/[N]: "
    #     ).lower()
    #     == "y"
    # )
    # concatenate_audio_files(vids[:5])
    convert_audio_files(vids[:5])


def setup():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-v",
        "--video-directory",
        help="Pass in a custom video directory to scan for Shadowplay recordings. Default: Your user's 'Videos' Library",
        default=get_user_videos_dir(),
    )
    return parser.parse_args()


def get_all_shadowplay_videos(path):
    return sorted(path.glob("**/*.DVR.mp4"), key=os.path.getmtime, reverse=True)


def get_audio_streams(video):
    return list(
        filter(lambda s: s["codec_type"] == "audio", ffmpeg.probe(video)["streams"])
    )


def concatenate_audio_files(videos):
    for v in videos:
        streams = len(get_audio_streams)


def concatenate_audio_files(videos):
    # Get all files' audio metadata: ffprobe
    video_stream_counts = {video: len(get_audio_streams(video)) for video in videos}
    max_streams = max(video_stream_counts.values())
    # ffmpeg -i input0 -i input1 -i input2 -t 1 -f lavfi -i anullsrc=r=48000:cl=stereo -filter_complex \
    # "[0:v][0:a][1:v][1:a][2:v][3:a]concat=n=3:v=1:a=1[v][a]" \
    # -map "[v]" -map "[a]" output

    for v in videos:
        print(f"Need to add {max_streams - video_stream_counts[v]} stream(s)")
    # Use 2xstereo tracks channel layout as the output
    # Make a dict of each file with the number of tracks
    # Assign L then R
    # If < 2 channels, use anullsrc to create the missing audio channel and repeat above
    # Run ffmpeg and concat with generated params based on dict values
    pass


def get_user_videos_dir():
    CSIDL_PERSONAL = 14  # My Videos
    SHGFP_TYPE_CURRENT = 0  # Get current, not default value

    CSIDL_PERSONAL
    buf = ctypes.create_unicode_buffer(ctypes.wintypes.MAX_PATH)
    ctypes.windll.shell32.SHGetFolderPathW(
        None, CSIDL_PERSONAL, None, SHGFP_TYPE_CURRENT, buf
    )

    return buf.value


if __name__ == "__main__":
    main()
