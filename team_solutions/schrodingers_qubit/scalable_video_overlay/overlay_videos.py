# Import moviepy editor library, which gives us the editing functions
from moviepy.editor import *

# Function to read the file of opacity inputs
def read_input():
    # Defining and array of the opacity levels for each clip
    opacities = []
    file = open("inputs.txt")
    # Reads the content of the file
    contents = file.readlines()
    # Iterates through file inputs
    for i in range(len(contents)):
        # Parses the input format and stores in variable
        placeholder = contents[i].rstrip()
        # Adds the float value to the list of opacity levels
        opacities.append(float(placeholder))
    # Closes the file once it's been read
    file.close()
    # Finally, returns our array of opacities
    return opacities

# Initializes list of video clips
videos = []
# Takes list of opacity levels from input function
opacities = read_input()
# Iterates through videos and assigns opacities
for i in range(len(opacities)): 
    # Initializes video clip from file
    videos.append(VideoFileClip("video_" + str(i+1) + ".webm"))
    # Sets the opacity level of the video
    videos[i] = videos[i].set_opacity(opacities[i])
# Combines our array of videos into a composite clip
final_video = CompositeVideoClip(videos) 
# Writes our final video to a .webm file
final_video.write_videofile("final_video.webm")
