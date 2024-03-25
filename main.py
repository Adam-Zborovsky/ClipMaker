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
                with open("last_end_time.txt", "w") as f:   
                    f.write("0")
        
        #Get start time for video
        start_time = 0
        with open("last_end_time.txt", "r") as f:  
            file_content = f.read().strip() 
            try:
                start_time = float(file_content)
            except ValueError:
                print(f"Error: Invalid value in last_end_time.txt: '{file_content}'")
                start_time = 0

        # Create a video clip with the same length as the audio file
        video_clip = VideoFileClip(video_folder +'/'+ video_file)
        video_clip_subclip = video_clip.subclip(start_time, start_time + audio_duration)
        video_clip_subclip = video_clip_subclip.set_audio(audio_clip)
        

        # Set aspect ratio for mobile and crop the middle part
        mobile_aspect_ratio = (9, 16)
        video_clip = video_clip.resize(height=mobile_aspect_ratio[1])
        video_clip = video_clip.crop(
            x_center=video_clip.w / 2,
            y_center=video_clip.h / 2,
            width=video_clip.h * mobile_aspect_ratio[0] / mobile_aspect_ratio[1],
            height=video_clip.h
        )

        output_path = os.path.join(output_folder, f"{audio_file[:-4]}.mp4")
        video_clip_subclip.write_videofile(output_path, codec='libx264')
    
        with open("last_end_time.txt", "w") as f:   
            f.write(str(start_time+audio_duration))

        print(f"Created video clip: {output_path}")
        os.remove(audio_file)

if __name__ == '__main__':
    for folder in [audio_folder, video_folder, output_folder]:
        if not os.path.exists(folder):
            os.makedirs(folder)

    input('Prees enter when resources are ready')
    create_video_clips()
