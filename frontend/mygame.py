import sys, pygame
from qiskit import QuantumCircuit
from composer_dummy import Composer
from typing import Tuple
import itertools

pygame.init()

# size = width, height = 320, 240
# speed = [2, 2]
# black = 0, 0, 0

# screen = pygame.display.set_mode(size)

# ball = pygame.image.load("intro_ball.gif")
# ballrect = ball.get_rect()

class QuaganiniGUI():

    def __init__(self, composer: Composer):
        # setup composer, start a new note
        self.composer = composer
        self.n_qubits : int = composer.num_qubits
        self.composer.new_note()

        # setup pygame metadata
        self._running : bool = True

        self.cell_len : int = 64

        self.head_height = 3
        self.circ_height = self.n_qubits

        self.board_size = self.board_width, self.board_height = 10, self.head_height + self.circ_height
        self.size: Tuple[int, int] = self.board_width * self.cell_len, self.board_height * self.cell_len 

        self.width, self.height = self.size

        self.font = pygame.font.SysFont('', 32)

        self.tmp_circuit = QuantumCircuit(5, 5)
        self.tmp_circuit.h(0)
        self.tmp_circuit.h(1)
        # self.tmp_circuit.cx(0, 1)
        # self.tmp_circuit.cx(0, 2)

    def on_init(self):
        pygame.init()
        self.screen = pygame.display.set_mode(self.size)
        self.clock = pygame.time.Clock()

        # generate gridsurface
        self.base_surface = pygame.Surface(self.size)
        for x, y in itertools.product(range(self.board_width), range(self.board_height)):
            rect = pygame.Rect(x * self.cell_len, y * self.cell_len, self.cell_len, self.cell_len)
            pygame.draw.rect(self.base_surface, pygame.Color('white'), rect, width = 1)

        self.gate_dict = self.build_gate_surfaces()
        # should setup the item selector area

        # do some display stuff

    def build_gate_surfaces(self):
        # gates: H, X, Z, Controls 

        bounding_rect = pygame.Rect((0, 0), (self.cell_len, self.cell_len))


        def build_gen_surface(inner_txt, in_color, back_color):
            surf = pygame.Surface((self.cell_len, self.cell_len))
            surf.fill(back_color)
            txt = self.font.render(inner_txt, True, in_color, back_color)
            surf.blit(txt, txt.get_rect(center = (0.5 * self.cell_len, 0.5 * self.cell_len)))
            pygame.draw.rect(surf, pygame.Color("white"), bounding_rect, 3)

            return surf
        
        return {"H": build_gen_surface("H", pygame.Color("white"), (0, 0, 255)),
                "X": build_gen_surface("X", pygame.Color("white"), (0, 255, 0)),
                "Z": build_gen_surface("Z", pygame.Color("white"), (255, 0, 0)),}

    def on_loop(self):
        # do mouseover handling
        pass

    def on_render(self):
        self.screen.fill(pygame.Color('black'))
        self.screen.blit(self.base_surface, (0,0))
        self.screen.blit(self.get_circuit_surf(self.tmp_circuit), (0, self.head_height * self.cell_len))
        pygame.display.flip()

    def get_circuit_surf(self, qc: QuantumCircuit):
        assert self.n_qubits == len(qc._qubits)

        circ_width, circ_height = self.width, self.circ_height * self.cell_len
        circ_surf = pygame.Surface((circ_width, circ_height), flags = pygame.SRCALPHA)
        circ_surf.fill((0, 0, 0, 0))

        bounding_rect = pygame.Rect(0, 0, circ_width, circ_height)
        pygame.draw.rect(circ_surf, pygame.Color("red"), bounding_rect, width = 1)

        # draw starting lines
        for i in range(self.n_qubits):
            pygame.draw.line(circ_surf, pygame.Color("white"), (0.5 * self.cell_len, (i + 0.5) * self.cell_len), 
                                (self.width - 0.5 * self.cell_len, (i + 0.5) * self.cell_len), 2)

        # draw starting letters
        for i in range(self.n_qubits):
            symb = self.font.render(f"q_{i + 1}", True, pygame.Color("white"), pygame.Color("black"))
            tmp_pos = (0.5 * self.cell_len, (i + 0.5) * self.cell_len)
            circ_surf.blit(symb, symb.get_rect(center=tmp_pos))


        # draw gates
        for i, circuit_instruction in enumerate(qc._data):
            self.draw_gate(circ_surf, qc, circuit_instruction, i)

        return circ_surf

    def draw_gate(self, circ_surf, qc: QuantumCircuit, circuit_instruction, i):
        op_name = circuit_instruction.operation.name
        qreg = qc.qregs[0]
        if len(op_name) == 1:
            target = qreg.index(circuit_instruction.qubits[0])
            surf = self.gate_dict[op_name.upper()]
            loc = (((2 * i + 2) + 0.5) * self.cell_len, (target + 0.5) * self.cell_len)
            circ_surf.blit(surf, surf.get_rect(center=loc))
        else:
            raise NotImplementedError

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False
            print(self._running)

    def on_cleanup(self):
        print("exited")
        sys.exit()
        pygame.quit()

    def on_execute(self):
        self.on_init()

        while( self._running == True ):
            # print('looped')
            for event in pygame.event.get():
                self.on_event(event)

            self.on_loop()
            self.on_render()
            self.clock.tick(60)
        self.on_cleanup()

while True:
    composer = Composer(5)
    qgui = QuaganiniGUI(composer)
    qgui.on_execute()