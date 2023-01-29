import os
import cv2
import numpy as np


def vid_params(vid_file):
    """Generates average frame color and average obj_count for
        a video."""
    # Initializing frame avg. color array
    # & object count array
    color_ar = []
    obj_c = []

    # Process video frame by frame
    cap = cv2.VideoCapture(vid_file)
    while (cap.isOpened()):
        ret, frame = cap.read()
        if ret == True:
            # Find average color of frame
            color_ar.append(avg_fColor(frame))

            # Use a canny edge detector
            # & count objects
            canny = cv2.Canny(frame, 80, 150)
            contours, hierarchy = cv2.findContours(canny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            obj_c.append(len(contours))

            # Exit
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            break

    # Exit the video
    cap.release()
    cv2.destroyAllWindows()

    return color_ar, obj_c


def avg_fColor(array):
    """Returns the average rgb value of the all the pixels
    of an image in decimal form"""

    # Find average for each of RGB
    avg_row = []
    for row in array:
        avg = np.average(row, axis=0)

        avg_row.append(avg)

    avg_rgb = np.average(avg_row, axis=0).astype(int)

    # Convert rgb to hex
    hex_c = '%02x%02x%02x' % tuple(avg_rgb)

    return int(hex_c, 16)


def batch_process(folder):
    """Runs vid_params for each video in folder &
        outputs an array of arrays for each parameter"""

    # List of files
    files = []

    # Iterate through each file in folder
    for filename in os.listdir(folder):
        f = os.path.join(folder, filename)

        # Checking if it is a file
        if os.path.isfile(f):
            files.append(f)

    # Array of parameters
    paramA = []
    paramB = []
    for filename in files:
        param1, param2 = vid_params(filename)

        paramA.append(param1)
        paramB.append(param2)
        print('Done!')

    return paramA, paramB


# https://www.geeksforgeeks.org/how-to-normalize-an-array-in-numpy-in-python/
def normalize(arr, t_min, t_max):
    norm_arr = []
    diff = t_max - t_min
    diff_arr = max(arr) - min(arr)
    for i in arr:
        temp = (((i - min(arr)) * diff) / diff_arr) + t_min
        norm_arr.append(temp)
    return norm_arr


def q_array(paramA, paramB, step=30, end=760):
    """Shapes & normalizes the params array
        for quantum processing"""

    for i in range(len(paramA)):
        paramA[i] = normalize(paramA[i], 0, 2 * np.pi)

    for i in range(len(paramB)):
        paramB[i] = normalize(paramB[i], 0, 2 * np.pi)

    new_paramA = []
    new_paramB = []

    for i in range(0, end, step):
        t_a = [item[i] for item in paramA]
        t_b = [item[i] for item in paramB]

        new_paramA.append(t_a)
        new_paramB.append(t_b)

    return new_paramA, new_paramB
