from moviepy.editor import VideoFileClip, AudioFileClip
import os

script_dir = os.path.dirname(os.path.realpath(__file__))
audio_folder = script_dir + '/resources/audio'
video_folder = script_dir + '/resources/video'
output_folder = script_dir + '/output'


def crop_video(input_path, output_path, aspect_ratio=(9, 16)):
    # Load the video
    video_clip = VideoFileClip(input_path)

    # Calculate the cropping dimensions
    width, height = video_clip.size
    new_width = min(width, height * aspect_ratio[0] / aspect_ratio[1])
    new_height = min(height, width * aspect_ratio[1] / aspect_ratio[0])
    x_offset = (width - new_width) / 2
    y_offset = (height - new_height) / 2

    # Crop and save the video
    cropped_clip = video_clip.crop(x_center=x_offset + new_width / 2, y_center=y_offset + new_height / 2, width=new_width, height=new_height)
    cropped_clip.write_videofile(output_path, codec='libx264')
    

def create_video_clips():
    audio_files = os.listdir(audio_folder)

    for audio_file in audio_files:
        audio_clip = AudioFileClip(os.path.join(audio_folder, audio_file))
        audio_duration = audio_clip.duration

        #Check if Video is long enough and set Video_file
        video_files = os.listdir(video_folder)
        video_file = video_files[0]
        video_file_duration = VideoFileClip(video_folder +'/'+ video_file).duration
        
        #Get start time for video
        start_time=0
        with open("last_end_time.txt", "r") as f:  
            file_content = f.read().strip() 
            try:
                start_time = float(file_content)
            except ValueError:
                print(f"Error: Invalid value in last_end_time.txt: '{file_content}'")
                start_time = 0

        if video_file_duration - start_time  < audio_duration:
            if len(video_files) > 1:
                video_file = video_files[1]
            else:
                print('No Video file')
            if video_file_duration - start_time < 30:
                os.remove(video_file)
                with open("last_end_time.txt", "w") as f:   
                    f.write("10")
        
        # Create a video clip with the same length as the audio file
        video_clip = VideoFileClip(video_folder +'/'+ video_file)
        video_clip_subclip = video_clip.subclip(start_time, start_time + audio_duration)
        video_clip_subclip = video_clip_subclip.set_audio(audio_clip)
        video_clip_subclip.write_videofile("To_Crop.mp4", codec='libx264')
   
        # Set aspect ratio for mobile and crop the middle part
        output_path = output_folder +'/'+ f"{audio_file.split('.')[0]}.mp4"
        crop_video("To_Crop.mp4", output_path)
        os.remove("To_Crop.mp4")

        with open("last_end_time.txt", "w") as f:   
            f.write(str(start_time+audio_duration))

        print(f"Created video clip: {output_path}")
        os.remove(audio_folder +'/'+ audio_file)

if __name__ == '__main__':
    for folder in [audio_folder, video_folder, output_folder]:
        if not os.path.exists(folder):
            os.makedirs(folder)

    input('Prees enter when resources are ready')
    if os.listdir(video_folder) == []:
        print('Resource Video Folder Is Empty')
    if os.listdir(audio_folder) == []:
        print('Resource Audio Folder Is Empty')
    if os.listdir(video_folder) != [] and os.listdir(audio_folder) != []:
        create_video_clips()
