
from sprite import Sprite
import random


def generate_correlated_bits(n=60):
    rand1_bits = [random.getrandbits(1) for i in range(n)]
    rand2_bits = [(rand1_bits[i] if random.random() < 0.1 else 1 - rand1_bits[i]) for i in range(n)]
    return rand1_bits, rand2_bits

r1, r2 = generate_correlated_bits()
sp1, sp2 = Sprite(r1), Sprite(r2)

sp1.save('sp1.png')
sp2.save('sp2.png')