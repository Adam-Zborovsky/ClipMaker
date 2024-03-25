from moviepy.editor import VideoFileClip, AudioFileClip
import os

def create_video_clips(audio_folder, video_folder, output_folder):
    audio_files = [f for f in os.listdir(audio_folder) if f.endswith('.mp3')]

    for audio_file in audio_files:
        audio_clip = AudioFileClip(os.path.join(audio_folder, audio_file))
        audio_duration = audio_clip.duration

        # Find a video file that is long enough
        video_files = [f for f in os.listdir(video_folder) if f.endswith('.mp4')]
        video_file = None
        for vf in video_files:
            video_clip = VideoFileClip(os.path.join(video_folder, vf))
            if video_clip.duration >= audio_duration:
                video_file = vf
                break

        if not video_file:
            print(f"No suitable video found for {audio_file}")
            continue

        # Create a video clip with the same length as the audio file
        video_clip = VideoFileClip(os.path.join(video_folder, video_file))
        video_clip = video_clip.subclip(0, audio_duration)
        video_clip = video_clip.set_audio(audio_clip)
        output_path = os.path.join(output_folder, f"{audio_file[:-4]}.mp4")
        video_clip.write_videofile(output_path, codec='libx264')

        print(f"Created video clip: {output_path}")

if __name__ == '__main__':
    audio_folder = 'path/to/audio/folder'
    video_folder = 'path/to/video/folder'
    output_folder = 'path/to/output/folder'
    create_video_clips(audio_folder, video_folder, output_folder)
