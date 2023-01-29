import numpy as np
import copy
from PIL import Image, ImageFilter
import random
import matplotlib as mpl
import matplotlib.cm as cm


def scale_region(img_path, region, scale_factor, direction=[1,0]):
    
    """ 
    this function scale a specific region of the original image given input region and scale_factor in a specific direction:
    img_path (str): path of the original image
    region (array or list): list of all points in a triangle, or the upper left point and lower buttom point of a rectangle
    scale_factor (float): the scale factor
    direction (list): the 2D direction of the scaling
    """
    
    # open the original image
    image = Image.open(img_path)
    
    # set a base_size so that the wing or beak will not be unrealistic small
    base_size = 25
    
    # the rectangle case
    if len(region)==2:
        
        # Get a box of the portion you want to magnify
        box = (region[0][0], region[0][1], region[1][0], region[1][1])
        portion = image.crop(box)
        
        # Resize the portion to double the size
        magnified = portion.resize((base_size + int((region[1][0]-region[0][0]) * scale_factor), \
                                                base_size + int((region[1][1]-region[0][1]) * scale_factor)))
        for_shape = np.array(magnified)
        pixdata = image.load()
        for px in range(region[0][0], region[1][0]-23):
            for py in range(region[0][1], region[1][1]-20):
                # the inequation generated from the original image
                if px < -0.87*py + 520:
                    pixdata[px, py] = (255,255,255)
        # to not allow the wing to be unrealistically small
        if scale_factor < 0.5:
            return image
        
        # Paste the magnified portion back on to the original image
        image.paste(magnified, (region[1][0] - for_shape.shape[0]-10, region[1][1] - for_shape.shape[0]-25))
     
    # the triangle case
    elif len(region)==3:
        scale_factor *= 7
        
        # Get a box of the portion you want to magnify
        box = (region[0][0], region[0][1], region[2][0], region[1][1]+ base_size * scale_factor)
        portion = image.crop(box)

        # Resize the portion to double the size
        magnified = portion.resize((60 + int(base_size * scale_factor), 50 + int(base_size * scale_factor)))

        # Paste the magnified portion back on to the original image
        image.paste(magnified, (447, 230)) # the second parameter is the upper left corner              
        
    return image

def expand_unevenly(img_path, fattness_r):
    
    """ 
    this function expand a specific region of the original image unevenly (related to position of pixels) 
    given input fattness factor in a specific direction:
    img_path (str): path of the original image
    fattness_f (float): the fattness factor
    """
    
    image = Image.open(img_path)
    pixdata = image.load()
    
    # the outer loop is iterating in the y-axis because we are doing in-place updating
    for py in range(image.size[1]-1,0,-1):
        for px in range(image.size[0]-1,0,-1):
            # the inequation generated from the original image
            if py > -0.6*px + 537.94:
                if px > 380: continue
                pixdata[min(px + int(px*0.06*fattness_r*2), image.size[0]-1), \
                        min(py + int(px*0.03*fattness_r*1.5), image.size[1]-1)] = pixdata[px, py]
                
    # the magic numbers comes from the original image
    box = (251, 332, image.size[0]-1, image.size[1]-1)
    portion = image.crop(box)
    portion = portion.filter(ImageFilter.GaussianBlur(radius=2))
    image.paste(portion, (251, 332))
    return image

def color(img_path, x):
    
    """ 
    this function color the finch given input position x in the colormap:
    img_path (str): path of the original image
    fattness_f (float): the fattness factor
    """

    norm = mpl.colors.Normalize(vmin=0, vmax=1)
    cmap = cm.hot
    scalar_map = cm.ScalarMappable(norm=norm, cmap=cmap)
    rgba = scalar_map.to_rgba(x)

    img = Image.open(img_path)
    img = img.convert("RGB")

    d = img.getdata()

    new_image = []
    for item in d:

        # change all white (also shades of whites)
        # pixels to yellow
        if item[0] not in list(range(200, 256)) and item[0] not in list(range(0,80)):
            new_image.append(tuple([np.uint8(i*255) for i in rgba]))
        else:
            new_image.append(item)

    # update image data
    img.putdata(new_image)

    # save new image
    return img

def visualize_1_evolution(image_path, output_name, color_r, beak_r, wingspan_r, fatness_r):
    
    """ 
    this function visualize the evolution result of each iteration, by calling the above function:
    image_path (str): path of the original image
    output_name (str): the output file name
    color_r (float): the color evolution
    beak_r (float): the new beak factor
    wingspan_r (float): the new wingspan factor
    fatness_r (float): the new fatness factor
    """
    
    # after got the quantum output
    # start the visualization part

    img_size_x, img_size_y = 612, 533 # the second dimension is the one changing vertically

    # beak triangle
    beak_tri_1_x =  447
    beak_tri_1_y = 230
    beak_tri_2_x = 447
    beak_tri_2_y = 270
    beak_tri_3_x = 480
    beak_tri_3_y = 252

    #wing rectangle:
    left_up_x,left_up_y = 88, 84
    right_down_x, right_down_y = 349, 358
    
    new_img = scale_region(image_path, [[beak_tri_1_x, beak_tri_1_y],[beak_tri_2_x, beak_tri_2_y],[beak_tri_3_x, beak_tri_3_y]], beak_r, [1,0])
    new_img.save("gen_image_tri.png")
    new_img = scale_region("gen_image_tri.png", [[left_up_x,left_up_y],[right_down_x, right_down_y]], wingspan_r)
    new_img.save("gen_image_rect.png")
    
    #new_img = scale_region("gen_image_rect.png", [[276-50, 354-50],[276 + 50, 354 + 50]], fatness_r)
    new_img = expand_unevenly("gen_image_rect.png", fatness_r)
    new_img.save("gen_image_fatter.png")

    new_img = color("gen_image_fatter.png", color_r)
    new_img.save(output_name)