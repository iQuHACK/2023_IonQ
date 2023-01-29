import taichi as ti
from .spin_config import IsingField


@ti.data_oriented
class MonteCarloDynamics:
    def __init__(self, ising_field: IsingField):
        self.ising_field = ising_field

    @ti.kernel
    def dynamics(self, k: ti.f32, h: ti.f32):
        for sig in ti.static(range(2)):
            for i, j in ti.ndrange(self.ising_field.lx, self.ising_field.ly):
                if (i + j) % 2 == sig:
                    self.flipping(i, j, k, h)

    @ti.func
    def flipping(self, i: ti.i32, j: ti.i32, k: ti.f32, h: ti.f32):

        ip = (i + 1) % self.ising_field.lx
        im = (i - 1) % self.ising_field.lx

        jp = (j + 1) % self.ising_field.ly
        jm = (j - 1) % self.ising_field.ly

        spin = self.ising_field.spin_config[i, j]

        rand_sgn_k = 1

        if ti.random() < 0.5:
            rand_sgn_k = 1
        else:
            rand_sgn_k = 1

        rand_sgn_h = 1

        if ti.random() < 0.5:
            rand_sgn_h = 1
        else:
            rand_sgn_h = 1

        dE = -2 * spin * \
             (rand_sgn_h * h + rand_sgn_k * k * (
                     self.ising_field.spin_config[ip, j] +
                     self.ising_field.spin_config[im, j] +
                     self.ising_field.spin_config[i, jp] +
                     self.ising_field.spin_config[i, jm]))

        if ti.random() < ti.exp(dE):
            self.ising_field.spin_config[i, j] *= -1
