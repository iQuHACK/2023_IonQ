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

        self.single_gates = ['H', 'X', 'Z']

        self.tmp_circuit = QuantumCircuit(5, 5)
        self.tmp_circuit.h(0)
        self.tmp_circuit.h(1)
        self.tmp_circuit.cx(0, 1)
        # self.tmp_circuit.cx(0, 2)

        self.shop_shift = (0.5 * self.cell_len, 0.5 * self.cell_len)
        self.selected_gate = ''
        self.global_bbox = []


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
        self.shop_surface, self.shop_bbox = self.get_shop_surf()
        # processes bbox and add to globals
        for rect, callable in self.shop_bbox:
            self.global_bbox.append([
                rect.move(self.shop_shift),
                callable
            ])
            # pygame.draw.rect(self.screen, pygame.Color("red"), rect.move(self.shop_shift), 2)
        # do some display stuff

    def get_shop_surf(self):
        shop_width, shop_height = 5, 2
        assert shop_height < self.head_height
        shop_size = (shop_width * self.cell_len, shop_height * self.cell_len)
        shop_surf = pygame.Surface(shop_size, flags = pygame.SRCALPHA)
        shop_bbox = pygame.Rect((0, 0), shop_size)
        shop_surf.fill((0, 0, 0, 0))
        pygame.draw.rect(shop_surf, pygame.Color("white"), shop_bbox, 2)
        
        # (rect, callable)
        bbox_collection = []

        def get_changestate_fn(gate):
            def changestate_fn():
                print("this works")
                print(gate)
                self.selected_gate = gate
            return changestate_fn

        # place down gates
        for i, g in enumerate(self.single_gates):
            center_loc = ((i + 0.5) * self.cell_len, shop_height/2 * self.cell_len)
            self.draw_single_gate(shop_surf, g, center_loc)
            bbox_collection.append([
                pygame.Rect(i * self.cell_len, 
                            shop_size[1]/2 - self.cell_len / 2, 
                            self.cell_len, 
                            self.cell_len),
                get_changestate_fn(g)
                ])
        
        for i, g in enumerate(['CX', 'CZ']):
            self.draw_two_gate(shop_surf, g[0], g[1], 
                                ((i + 0.5 + len(self.single_gates)) * self.cell_len, shop_height/4 * self.cell_len),
                                ((i + 0.5 + len(self.single_gates)) * self.cell_len, 3 * shop_height/4 * self.cell_len))
            bbox_collection.append([
                pygame.Rect((i + len(self.single_gates)) * self.cell_len, 
                             0, 
                             self.cell_len,
                             shop_height * self.cell_len),
                get_changestate_fn(g)
            ])
        
        return shop_surf, bbox_collection

    def build_gate_surfaces(self):
        # gates: H, X, Z, Controls 

        def build_gen_surface(inner_txt, in_color, back_color):
            d = 0.8
            bounding_rect = pygame.Rect((0, 0), (d * self.cell_len, d * self.cell_len))
            surf = pygame.Surface((d * self.cell_len, d * self.cell_len))
            surf.fill(back_color)
            txt = self.font.render(inner_txt, True, in_color, back_color)
            surf.blit(txt, txt.get_rect(center = (d / 2 * self.cell_len, d / 2* self.cell_len)))
            pygame.draw.rect(surf, pygame.Color("white"), bounding_rect, 3)

            return surf
        
        d = 0.25
        small_bbox = pygame.Rect((0, 0), (d * self.cell_len, d * self.cell_len)) 
        c_surf = pygame.Surface((d * self.cell_len, d * self.cell_len), pygame.SRCALPHA)
        pygame.draw.ellipse(c_surf, pygame.Color("white"), small_bbox)


        return {"H": build_gen_surface("H", pygame.Color("white"), (0, 0, 255)),
                "X": build_gen_surface("X", pygame.Color("white"), (0, 255, 0)),
                "Z": build_gen_surface("Z", pygame.Color("white"), (255, 0, 0)),
                "C": c_surf}

    def on_loop(self):
        # do mouseover handling
        pass

    def on_render(self):
        self.screen.fill(pygame.Color('black'))
        self.screen.blit(self.base_surface, (0,0))
        self.screen.blit(self.shop_surface, self.shop_shift)
        self.screen.blit(self.get_circuit_surf(self.tmp_circuit), (0, self.head_height * self.cell_len))
        for rect, callable in self.global_bbox:
            pygame.draw.rect(self.screen, pygame.Color("red"), rect, 2)
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

    def draw_single_gate(self, dest_surf, gate, loc):
        surf = self.gate_dict[gate]
        dest_surf.blit(surf, surf.get_rect(center=loc))

    def draw_two_gate(self, dest_surf, gate1, gate2, loc1, loc2):
        pygame.draw.line(dest_surf, pygame.Color("white"), loc1, loc2, 3) 

        self.draw_single_gate(dest_surf, gate1, loc1)
        self.draw_single_gate(dest_surf, gate2, loc2)

    def draw_gate(self, circ_surf, qc: QuantumCircuit, circuit_instruction, i):
        op_name = circuit_instruction.operation.name
        qreg = qc.qregs[0]
        if len(op_name) == 1:
            target = qreg.index(circuit_instruction.qubits[0])
            loc = (((i + 1) + 0.5) * self.cell_len, (target + 0.5) * self.cell_len)
            self.draw_single_gate(circ_surf, op_name.upper(), loc)

        elif len(op_name) == 2:
            # control gate
            # from
            c_index = qreg.index(circuit_instruction.qubits[0])
            t_index = qreg.index(circuit_instruction.qubits[1])

            c_loc = (((i + 1) + 0.5) * self.cell_len, (c_index + 0.5) * self.cell_len)
            t_loc = (c_loc[0], (t_index + 0.5) * self.cell_len) 

            self.draw_two_gate(circ_surf, 'C', op_name[1].upper(), c_loc, t_loc)

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False
            print(self._running)
        if event.type == pygame.MOUSEBUTTONDOWN:
            print("clicked")
            for rect, callable in self.global_bbox:
                if rect.collidepoint(event.pos):
                    callable()
            print(self.selected_gate)

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