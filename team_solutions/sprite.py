from PIL import Image
import numpy as np
import random


# helper functions

def bits_to_int(bits):
    return sum([bit * 2 ** i for i, bit in enumerate(bits)])

class RandomWalker:

    def __init__(self, walk_space, start_point=None):
        if start_point is None:
            start_point = len(walk_space) // 2
        self.walk_space = walk_space
        self.current_point = start_point

    def step(self, direction_bit):
        if self.current_point == 0:
            self.current_point = 1
        elif self.current_point == len(self.walk_space) - 1:
            self.current_point = len(self.walk_space) - 2
        else:
            self.current_point += (1 if direction_bit == 1 else -1)

        return self.walk_space[self.current_point]

            

class Sprite:

    BITS_PER_COLOR_COMPONENT = 3
    NUM_COLORS = 2
    BITS_PER_LOCATION = 2 # should be 1 + log2(NUM_COLORS)
    PIXEL_SIZE = 64

    def __init__(self, random_array, size = 5):
        assert size % 2 == 1

        self.random_array = random_array
        self.img_array = None
        self.dims = (size, size)

        self.generate()

    def distribute_randomness(self):
        if len(self.random_array) >= self.NUM_COLORS * self.BITS_PER_COLOR_COMPONENT * 3 + self.BITS_PER_LOCATION * ((self.dims[0] // 2) + 1) * self.dims[1]:
            self.color_randomness = self.random_array[:self.NUM_COLORS * self.BITS_PER_COLOR_COMPONENT * 3]
            self.location_randomness = self.random_array[self.NUM_COLORS * self.BITS_PER_COLOR_COMPONENT * 3: self.NUM_COLORS * self.BITS_PER_COLOR_COMPONENT * 3 + self.BITS_PER_LOCATION * ((self.dims[0] // 2) + 1) * self.dims[1]]
        else:
            print("Warning: not enough randomness provided to Sprite constructor, repeating randomness")
            # ah we have low randomness, we can duplicate the randomness to make it more random
            self.color_randomness = []
            while len(self.color_randomness) < self.NUM_COLORS * self.BITS_PER_COLOR_COMPONENT * 3:
                self.color_randomness += self.random_array
                self.random_array = self.random_array[::-1]
                # flip the bits
                self.random_array = [1 - bit for bit in self.random_array]
            self.color_randomness = self.color_randomness[:self.NUM_COLORS * self.BITS_PER_COLOR_COMPONENT * 3]

            self.random_array = self.random_array[::-1]

            self.location_randomness = []
            while len(self.location_randomness) < self.BITS_PER_LOCATION * ((self.dims[0] // 2) + 1) * self.dims[1]:
                self.location_randomness += self.random_array
                self.random_array = self.random_array[::-1]
            self.location_randomness = self.location_randomness[:self.BITS_PER_LOCATION * ((self.dims[0] // 2) + 1) * self.dims[1]]

    def get_random_color(self, random_bits):
        assert len(random_bits) == self.BITS_PER_COLOR_COMPONENT * 3
        def get_color_component(bits):
            MIN_VAL = 64
            MAX_VAL = 255
            return int(MIN_VAL + (MAX_VAL - MIN_VAL) * bits_to_int(bits) / (2 ** self.BITS_PER_COLOR_COMPONENT - 1))
        return (get_color_component(random_bits[0:3]), get_color_component(random_bits[3:6]), get_color_component(random_bits[6:9]))

    def get_image_elements(self, random_bits):
        assert len(random_bits) == self.BITS_PER_LOCATION * ((self.dims[0] // 2) + 1) * self.dims[1]
        # returns a size x size array of integers in the range [0, self.NUM_COLORS]
        # where 0 has probability 1/2 and other values have probability 1/(2 * self.NUM_COLORS)
        # the array is symmetric about the vertical axis
        element_array = [[0 for _ in range(self.dims[1])] for _ in range(self.dims[0])]

        self.random_walker = None

        for i in range(self.dims[0]//2 + 1):
            for j in range(self.dims[1]):
                bits = random_bits[(i * self.dims[1] + j) * self.BITS_PER_LOCATION:(i * self.dims[1] + j + 1) * self.BITS_PER_LOCATION]
                element_array[i][j] = self.get_element_random_walk(bits)
                element_array[self.dims[0] - i - 1][j] = element_array[i][j]

        return element_array

    
    def get_element(self, bits):
        return 0 if bits[0] == 0 else ((bits_to_int(bits[1:]) % self.NUM_COLORS) + 1)

    def get_element_random_walk(self, bits):
        # Needs only one bit, fix later
        if self.random_walker is None:
            self.random_walker = RandomWalker([i for i in range(1, self.NUM_COLORS + 1)])

        element = self.random_walker.step(bits[1])
        
        if bits[0] == 0:
            return 0
        else:
            return element



    def get_color_palette(self, random_bits, gradient_size=0):
        assert len(random_bits) == self.NUM_COLORS * self.BITS_PER_COLOR_COMPONENT * 3
        color_palette = [self.get_random_color(random_bits[i * self.BITS_PER_COLOR_COMPONENT * 3:(i + 1) * self.BITS_PER_COLOR_COMPONENT * 3]) for i in range(self.NUM_COLORS)]
        
        if gradient_size > 0:
            color_palette = [color_palette[0]] + [tuple([int(color_palette[0][i] + (color_palette[1][i] - color_palette[0][i]) * j / gradient_size) for i in range(3)]) for j in range(1, gradient_size + 1)] + [color_palette[1]]
        
        color_palette.insert(0, (0, 0, 0))
        return color_palette



    def generate(self):
        self.img_array = [[(0, 0, 0) for _ in range(self.dims[1])] for _ in range(self.dims[0])]

        self.distribute_randomness()

        self.color_palette = self.get_color_palette(self.color_randomness, gradient_size=0)
        self.image_elements = self.get_image_elements(self.location_randomness)

        for i in range(self.dims[0]):
            for j in range(self.dims[1]):
                self.img_array[i][j] = self.color_palette[self.image_elements[i][j]]

        

    def save(self, filename):
        image = self.render()
        image.save(filename)

    def render(self):
        if self.img_array is None:
            self.generate()

        # we want to have zoomed in version of the image. So each pixel in the image is a square of size PIXEL_SIZE
        self.image = Image.new('RGB', (self.dims[0] * self.PIXEL_SIZE, self.dims[1] * self.PIXEL_SIZE))
        for i in range(self.dims[0]):
            for j in range(self.dims[1]):
                for k in range(self.PIXEL_SIZE):
                    for l in range(self.PIXEL_SIZE):
                        self.image.putpixel((i * self.PIXEL_SIZE + k, j * self.PIXEL_SIZE + l), self.img_array[i][j])
        
        self.black_square = Image.new('RGB', (3*self.dims[0] * self.PIXEL_SIZE, 3*self.dims[1] * self.PIXEL_SIZE))
        for i in range(3*self.dims[0]):
            for j in range(3*self.dims[1]):
                for k in range(self.PIXEL_SIZE):
                    for l in range(self.PIXEL_SIZE):
                        self.black_square.putpixel((i * self.PIXEL_SIZE + k, j * self.PIXEL_SIZE + l), (0, 0, 0))
        self.inside_square = Image.new('RGB', (2*self.dims[0] * self.PIXEL_SIZE, 2*self.dims[1] * self.PIXEL_SIZE))
        for i in range(2*self.dims[0]):
            for j in range(2*self.dims[1]):
                for k in range(self.PIXEL_SIZE):
                    for l in range(self.PIXEL_SIZE):
                        self.inside_square.putpixel((i * self.PIXEL_SIZE + k, j * self.PIXEL_SIZE + l), (0, 0, 0))
        x = 0
        while x < self.inside_square.size[0]:
            y = 0
            while y < self.inside_square.size[1]:
                if y == self.image.size[1]:
                    self.inside_square.paste(self.image.rotate(180), (x, y))
                else:
                    self.inside_square.paste(self.image, (x, y))
                y += self.image.size[1]
            x += self.image.size[0]
        self.inside_square.thumbnail(self.image.size, Image.ANTIALIAS)

        if random.randint(1, 10) <= 5:
            locations = [(self.image.size[0], 0), (0, self.image.size[1]), (self.image.size[0], 2*self.image.size[1]), (2*self.image.size[0], self.image.size[1])]
            for (i, location) in enumerate(locations):
                if i != 0:
                    self.image = self.image.rotate(90)
                self.black_square.paste(self.image, location)
        else: 
            locations = [(0, 0), (2*self.image.size[0], 0), (0, 2*self.image.size[1]), (2*self.image.size[0], 2*self.image.size[1])]
            for (i, location) in enumerate(locations):
                if i > 1:
                    self.black_square.paste(self.image.rotate(180), location)
                else: 
                    self.black_square.paste(self.image, location)
        self.black_square.paste(self.inside_square, self.image.size)
        return self.black_square

    def get_image(self):
        if self.img_array is None:
            self.generate()
        return self.img_array

if __name__ == "__main__":
    for i in range(50, 60):
        random_arr = [random.getrandbits(1) for _ in range(9)]
        sprite = Sprite(random_arr)
        sprite.save(f"sprites_random_walk/sprite_{i}.png")
        print(f"Saved sprite {i}")
    

    