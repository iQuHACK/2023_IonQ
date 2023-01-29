def avg_color(img_file):
    """Returns the average rgb value of the all the pixels
    of an image in decimal form"""
    import numpy as np
    from PIL import Image
    
    # Read image into np array
    img = Image.open(img_file)
    array = np.array(img)
    
    # Find average for each of RGB
    avg_row = []
    for row in array:
        avg = np.average(row, axis=0)

        avg_row.append(avg)
        
    avg_rgb = np.average(avg_row, axis=0).astype(int)
    
    # Convert rgb to hex
    hex_c = '%02x%02x%02x' % tuple(avg_rgb)
    
    return int(hex_c, 16)
    