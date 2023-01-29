import taichi as ti


@ti.data_oriented
class IsingField:
    def __init__(self, lx: ti.i32, ly: ti.i32):
        self.lx = lx
        self.ly = ly

        self.npts = self.lx * self.ly

        self.spin_config = ti.field(dtype=ti.i32, shape=(lx, ly))

        self.spin_img = ti.field(dtype=ti.f32, shape=(lx, ly))
        self.cor = ti.field(dtype=ti.f32, shape=(lx // 2, ly // 2))

    @ti.kernel
    def field_init(self):
        for i, j in ti.ndrange(self.lx, self.ly):
            if ti.random() > 0.5:
                self.spin_config[i, j] = 1
            else:
                self.spin_config[i, j] = -1

    @ti.kernel
    def off_set(self):
        for i, j in self.spin_config:
            self.spin_img[i, j] = (self.spin_config[i, j] + 1) / 2

    @ti.kernel
    def energy(self, k: ti.f32, h: ti.f32) -> ti.f32:
        int_temp = 0
        ext_temp = 0

        for i, j in ti.ndrange(self.lx, self.ly):
            ext_temp += h * self.spin_config[i, j]
            int_temp += k * self.spin_config[i, j] * \
                        (self.spin_config[(i + 1) % self.lx, j] +
                         self.spin_config[i, (j + 1) % self.ly])
        return int_temp + ext_temp

    @ti.kernel
    def correlation_distribution(self):
        for i, j in ti.ndrange(self.lx // 2, self.ly // 2):
            self.cor[i, j] = self.correlation(i, j)

    @ti.func
    def correlation(self, ip, jp) -> ti.f32:
        cor = 0.0
        for i, j in ti.ndrange(self.lx, self.ly):
            cor += self.spin_config[i, j] * self.spin_config[(i + ip) % self.lx, (j + jp) % self.ly]
        # <s_i s_j>
        cor /= self.npts
        # <s_i>
        s0 = self.magnetization()
        return cor - s0 * s0

    @ti.kernel
    def mag_py(self) -> ti.f32:
        return self.magnetization()

    @ti.func
    def magnetization(self) -> ti.f32:
        m = 0
        for i, j in ti.ndrange(self.lx, self.ly):
            m += self.spin_config[i, j]
        return m / self.npts
