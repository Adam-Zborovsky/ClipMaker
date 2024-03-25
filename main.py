from moviepy.editor import VideoFileClip, AudioFileClip
import os

script_dir = os.path.dirname(os.path.realpath(__file__))
audio_folder = script_dir + '/resources/audio'
video_folder = script_dir + '/resources/video'
output_folder = script_dir + '/output'


def create_video_clips():
    audio_files = os.listdir(audio_folder)

    for audio_file in audio_files:
        audio_clip = AudioFileClip(os.path.join(audio_folder, audio_file))
        audio_duration = audio_clip.duration

        #Check if Video is long enough and set Video_file
        video_files = os.listdir(video_folder)
        video_file = video_files[0]
        video_file_duration = VideoFileClip(video_folder +'/'+ video_file).duration
        
        if video_file_duration < audio_duration:
            video_file = video_files[1]
            if video_file_duration < 30:
                os.remove(video_file)
        

        # Create a video clip with the same length as the audio file
        video_clip = VideoFileClip(video_folder +'/'+ video_file)
        video_clip = video_clip.subclip(0, audio_duration)
        video_clip = video_clip.set_audio(audio_clip)
        output_path = os.path.join(output_folder, f"{audio_file[:-4]}.mp4")
        video_clip.write_videofile(output_path, codec='libx264')
        
        # Modify the original video by removing the used segment
        remaining_video_clip = video_clip.subclip(audio_duration)
        remaining_video_clip.write_videofile(os.path.join(video_folder, video_file), codec='libx264')

        print(f"Created video clip: {output_path}")
        os.remove(audio_file)

if __name__ == '__main__':
    for folder in [audio_folder, video_folder, output_folder]:
        if not os.path.exists(folder):
            os.makedirs(folder)


    create_video_clips()
