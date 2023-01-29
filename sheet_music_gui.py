import sys, pygame
from qiskit import QuantumCircuit
from music import Composer, Sandbox_CLI
from generate_jazz import play_generated_jazz
from typing import Tuple
import itertools

pygame.init()

class SheetMusicGUI():
    def __init__(self, composer: Composer):
        # setup composer, start a new note
        self.composer = composer
        self.n_qubits : int = composer.num_qubits

        # setup pygame metadata
        self._running : bool = True

        self.cell_len : int = 64

        self.head_height = 3
        self.circ_height = self.n_qubits

        self.board_size = self.board_width, self.board_height = 21, self.head_height + self.circ_height
        self.size: Tuple[int, int] = self.board_width * self.cell_len, self.board_height * self.cell_len 

        self.width, self.height = self.size

        self.font = pygame.font.SysFont('', 32)
        self.small_font = pygame.font.SysFont('', 24)

        self.single_gates_wparam = ['RX', 'RY', 'RZ']
        self.single_gates_nparam = ['H', 'X', 'Y', 'Z']
        self.single_gates = self.single_gates_nparam + self.single_gates_wparam
        self.double_gates = ['CX', 'CZ']

        self.curr_count = 0

        self.shop_shift = (0.5 * self.cell_len, 0.5 * self.cell_len)
        self.selected_gate = ''
        self.selected_control_y = None
        self.rotation_box_y = ""
        self.curr_rot_txt = ""
        self.mode = "neutral"
        # modes: neutral, selected, control, rotation
        # allowed: neutral -> *, selected -> neutral, selected -> control
        # not allowed: control -> selected
        self.global_bbox = []


    def on_init(self):
        pygame.init()
        self.screen = pygame.display.set_mode(self.size)
        self.clock = pygame.time.Clock()

        # generate gridsurface
        self.base_surface = pygame.Surface(self.size)

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
        self.overlay_surface = None
        # do some display stuff

    def get_shop_surf(self):
        shop_width, shop_height = self.board_width - 1, 2
        assert shop_height < self.head_height
        shop_size = (shop_width * self.cell_len, shop_height * self.cell_len)
        shop_surf = pygame.Surface(shop_size, flags = pygame.SRCALPHA)
        shop_bbox = pygame.Rect((0, 0), shop_size)
        shop_surf.fill((0, 0, 0, 0))
        # pygame.draw.rect(shop_surf, pygame.Color("white"), shop_bbox, 2)
        
        # (rect, callable)
        bbox_collection = []

        def get_changestate_fn(gate):
            def changestate_fn():
                print("this works")
                print(gate)
                if self.mode != 'control':
                    self.selected_gate = gate
                    self.mode = 'selected'
            return changestate_fn

        # place down gates
        for i, g in enumerate(self.single_gates):
            center_loc = ((i + 0.5) * self.cell_len, shop_height/2 * self.cell_len)
            if g in self.single_gates_wparam:
                self.draw_single_gate(shop_surf, g + 's', center_loc)
            else:
                self.draw_single_gate(shop_surf, g, center_loc)
            bbox_collection.append([
                pygame.Rect(i * self.cell_len, 
                            shop_size[1]/2 - self.cell_len / 2, 
                            self.cell_len, 
                            self.cell_len),
                get_changestate_fn(g)
                ])
        
        for i, g in enumerate(self.double_gates):
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

        # add new note button
        new_note_dims = (2, 1)
        new_note_box = pygame.Rect(shop_bbox.right - 0.5 * self.cell_len - new_note_dims[0] * self.cell_len, 
                                   shop_bbox.centery - new_note_dims[1] * self.cell_len/2, 
                                   new_note_dims[0] * self.cell_len, 
                                   new_note_dims[1] * self.cell_len)
        bbox_collection.append([
            new_note_box,
            self.new_note
        ])
        new_note_text = self.font.render("New Note", True, pygame.Color("white"), pygame.Color("red"))
        pygame.draw.rect(shop_surf, pygame.Color("red"), new_note_box)
        pygame.draw.rect(shop_surf, pygame.Color("white"), new_note_box, 3)
        shop_surf.blit(new_note_text, new_note_text.get_rect(center=new_note_box.center))

        # add play music button
        play_dims = (2, 1)
        play_box = new_note_box.move(-(play_dims[0] + .5) * self.cell_len, 0)
        bbox_collection.append([
            play_box,
            self.play_music
        ])
        play_text = self.font.render("Play Music", True, pygame.Color("white"), pygame.Color("red"))
        pygame.draw.rect(shop_surf, pygame.Color("red"), play_box)
        pygame.draw.rect(shop_surf, pygame.Color("white"), play_box, 3)
        shop_surf.blit(play_text, play_text.get_rect(center=play_box.center))

        # add qaganini button
        qag_dims = (2, 0.6)
        qag_box = play_box.move(-(qag_dims[0] + .5) * self.cell_len, 0)
        qag_box.height = qag_box.height * 3/5
        qag_box.top = 0

        for i, qg in enumerate(["Qaganini", "Qaganini?", "QAGANINI!"]):
            bbox_collection.append([
                qag_box,
                self.qaganini_level(i)
            ])
            qag_text = self.font.render(qg, True, pygame.Color("white"), pygame.Color("red"))
            pygame.draw.rect(shop_surf, pygame.Color("red"), qag_box)
            pygame.draw.rect(shop_surf, pygame.Color("white"), qag_box, 3)
            shop_surf.blit(qag_text, qag_text.get_rect(center=qag_box.center))
            qag_box = qag_box.move(0, ((2 * self.cell_len) - qag_box.height) / 2)
 
        # play jazz button
        pj_dims = (2, 1)
        pj_box = qag_box.move(-(pj_dims[0] + .5) * self.cell_len, 0)
        pj_box.height *= 5/3
        pj_box.centery = self.cell_len
        bbox_collection.append([
            pj_box,
            self.play_jazz
        ])
        pj_text = self.font.render("Play Jazz", True, pygame.Color("white"), pygame.Color("red"))
        pygame.draw.rect(shop_surf, pygame.Color("red"), pj_box)
        pygame.draw.rect(shop_surf, pygame.Color("white"), pj_box, 3)
        shop_surf.blit(pj_text, pj_text.get_rect(center=pj_box.center))

        # maybe prev and next


        # counter of which circuit you're currently viewing
        
        return shop_surf, bbox_collection

    def build_gate_surfaces(self):
        # gates: H, X, Z, Controls 

        def build_gen_surface(inner_txt, in_color, back_color, text_shift = (0,0)):
            d = 0.8
            bounding_rect = pygame.Rect((0, 0), (d * self.cell_len, d * self.cell_len))
            surf = pygame.Surface((d * self.cell_len, d * self.cell_len))
            surf.fill(back_color)
            txt = self.font.render(inner_txt, True, in_color, back_color)
            surf.blit(txt, txt.get_rect(center = (d / 2 * self.cell_len, d / 2* self.cell_len)).move(text_shift))
            pygame.draw.rect(surf, in_color, bounding_rect, 3)

            return surf

        def build_param_surface(inner_txt, in_color, back_color, text_shift = (0, 0)):
            surf = build_gen_surface(inner_txt, in_color, back_color, text_shift)
            txt_width, txt_height = 0.6 * self.cell_len, 0.2 * self.cell_len
            txt_rect = pygame.Rect(0, 0, txt_width, txt_height)
            txt_rect.center = surf.get_rect().center
            pygame.draw.rect(surf, pygame.Color("white"), txt_rect.move(0, 0.2 * self.cell_len), 1) 
            return surf
        
        d = 0.25
        small_bbox = pygame.Rect((0, 0), (d * self.cell_len, d * self.cell_len)) 
        c_surf = pygame.Surface((d * self.cell_len, d * self.cell_len), pygame.SRCALPHA)
        pygame.draw.ellipse(c_surf, pygame.Color("white"), small_bbox)

        o_surf = pygame.Surface((d * self.cell_len, d * self.cell_len), pygame.SRCALPHA)
        pygame.draw.ellipse(o_surf, pygame.Color("red"), small_bbox, 2)

        s_shift = (0, -0.1 * self.cell_len)

        return {"H": build_gen_surface("H", pygame.Color("white"), (0, 0, 255)),
                "X": build_gen_surface("X", pygame.Color("white"), (0, 255, 0)),
                "Y": build_gen_surface("Y", pygame.Color("white"), (221,160,221)),
                "Z": build_gen_surface("Z", pygame.Color("white"), (255, 0, 0)),
                "RX": build_gen_surface("RX", pygame.Color("white"), (0, 0, 0), s_shift),
                "RY": build_gen_surface("RY", pygame.Color("white"), (0, 0, 0), s_shift),
                "RZ": build_gen_surface("RZ", pygame.Color("white"), (0, 0, 0), s_shift),
                "RXs": build_param_surface("RX", pygame.Color("white"), (0, 0, 0), s_shift),
                "RYs": build_param_surface("RY", pygame.Color("white"), (0, 0, 0), s_shift),
                "RZs": build_param_surface("RZ", pygame.Color("white"), (0, 0, 0), s_shift),
                "C": c_surf,
                "O": o_surf,
                "B": build_gen_surface("", pygame.Color("red"), (0, 0, 0))}

    def get_mouse_box(self, mouse_pos = None):
        # only works in the circuit area
        if mouse_pos is None:
            mouse_pos = pygame.Vector2(pygame.mouse.get_pos()) 

        # print("called")
        if mouse_pos[1] < self.head_height * self.cell_len or self.mode == 'neutral':
            return (None, None)
        rel_pos = mouse_pos[0], mouse_pos[1] - self.head_height * self.cell_len
        x = rel_pos[0] // self.cell_len
        y = rel_pos[1] // self.cell_len
        return (x, y)

    def get_overlay_surface(self,):
        overlay_surface = pygame.Surface(self.size, pygame.SRCALPHA)
        overlay_surface.fill((0,0,0,0))
        sel_ctrl_center = None

        if self.mode == 'rotation':
            # we need to open up text box
            txt_width, txt_height = 0.7 * self.cell_len, 0.3 * self.cell_len
            txt_rect = pygame.Rect(0, 0, txt_width, txt_height)
            txt_rect.center = ((self.curr_count + 1.5) * self.cell_len, (self.rotation_box_y + self.head_height + .5) * self.cell_len)
            self.draw_single_gate(overlay_surface, self.selected_gate, txt_rect.center)
            pygame.draw.rect(overlay_surface, pygame.Color("white"), txt_rect.move(0, 0.2 * self.cell_len), 1)
            txt = self.small_font.render(self.curr_rot_txt, True, pygame.Color('white'), pygame.Color('black'))
            overlay_surface.blit(txt, txt.get_rect(center = txt_rect.move(0, 0.2 * self.cell_len).center))


        if self.selected_control_y is not None:
            # draw the filled in block
            sel_ctrl_center = ((self.curr_count + 1.5) * self.cell_len, (self.selected_control_y + 0.5 + self.head_height) * self.cell_len)
            self.draw_single_gate(overlay_surface, 'C', sel_ctrl_center)
            # draw the line to cursor position

        # do mouseover handling
        (x, y) = self.get_mouse_box()

        if x is None:
            return overlay_surface

        center_pos = (self.cell_len * (self.curr_count + 1 + 0.5), self.cell_len * (y + self.head_height) + 0.5 * self.cell_len)
        if self.mode == 'selected':
            if self.selected_gate in self.double_gates:
                # do something with circle
                self.draw_single_gate(overlay_surface, 'O', center_pos)
            else:
                # do something with red square
                self.draw_single_gate(overlay_surface, 'B', center_pos)
        
        if self.mode == 'control':
            if y == self.selected_control_y:
                return overlay_surface

            if y > self.selected_control_y:
                pygame.draw.line(overlay_surface, pygame.Color('red'), 
                                    (sel_ctrl_center[0], sel_ctrl_center[1] + 0.3 * self.cell_len),
                                    ((self.curr_count + 1.5) * self.cell_len, (y + 0.5 + self.head_height) * self.cell_len),
                                    2)
            if y < self.selected_control_y:
                pygame.draw.line(overlay_surface, pygame.Color('red'), 
                                    (sel_ctrl_center[0], sel_ctrl_center[1] - 0.3 * self.cell_len),
                                    ((self.curr_count + 1.5) * self.cell_len, (y + 0.5 + self.head_height) * self.cell_len),
                                    2)
            self.draw_single_gate(overlay_surface, 'B', center_pos)
        
        return overlay_surface

    def on_loop(self):
        self.overlay_surface = self.get_overlay_surface()

    def on_render(self):
        self.screen.fill(pygame.Color('black'))
        self.screen.blit(self.base_surface, (0,0))
        self.screen.blit(self.shop_surface, self.shop_shift)
        self.screen.blit(self.get_circuit_surf(self.composer.circ), (0, self.head_height * self.cell_len))
        if self.overlay_surface is not None:
            self.screen.blit(self.overlay_surface, (0,0))
        # TODO: remove these
        # for rect, callable in self.global_bbox:
        #     pygame.draw.rect(self.screen, pygame.Color("red"), rect, 2)
        pygame.display.flip()

    def get_circuit_surf(self, qc: QuantumCircuit):
        assert self.n_qubits == len(qc._qubits)

        circ_width, circ_height = self.width, self.circ_height * self.cell_len
        circ_surf = pygame.Surface((circ_width, circ_height), flags = pygame.SRCALPHA)
        circ_surf.fill((0, 0, 0, 0))

        bounding_rect = pygame.Rect(0, 0, circ_width, circ_height)
        # pygame.draw.rect(circ_surf, pygame.Color("red"), bounding_rect, width = 1)

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
    
    def draw_single_gate_wparam(self, dest_surf, gate, loc, param):
        surf = self.gate_dict[gate]
        dest_surf.blit(surf, surf.get_rect(center = loc))
        txt = self.small_font.render(str(param)[:4], True, pygame.Color('white'), pygame.Color('black'))
        dest_surf.blit(txt, txt.get_rect(center = loc).move(0, 0.2 * self.cell_len))

    def draw_two_gate(self, dest_surf, gate1, gate2, loc1, loc2):
        pygame.draw.line(dest_surf, pygame.Color("white"), loc1, loc2, 3) 

        self.draw_single_gate(dest_surf, gate1, loc1)
        self.draw_single_gate(dest_surf, gate2, loc2)

    def new_note(self):
        self.curr_count = 0
        self.composer.new_note()

    def play_music(self):
        self.composer.run_job()
        self.composer.generate_audio()

    def qaganini_level(self, i):
        def qag_callable():
            ranges = [1, 5, self.board_width - self.curr_count - 2]
            print(self.curr_count)
            for _ in range(ranges[i]):
                self.qaganini()
        return qag_callable

    def qaganini(self):
        # just do one random gate for them
        command = Sandbox_CLI().random_command(self.n_qubits)
        op = command[0].upper()
        if op in self.single_gates_nparam:
            self.composer.add_single_qubit_gate(op, int(command[1]))
        elif op in self.single_gates_wparam:
            self.composer.add_single_qubit_gate_wparam(op, int(command[1]), float(command[2]))
        else:
            self.composer.add_two_qubit_gate(op, int(command[1]), int(command[2]))
        self.curr_count += 1

    def play_jazz(self):
        play_generated_jazz()

    def draw_gate(self, circ_surf, qc: QuantumCircuit, circuit_instruction, i):
        op_name = circuit_instruction.operation.name
        qreg = qc.qregs[0]
        if op_name.upper() in self.single_gates_nparam:
            target = qreg.index(circuit_instruction.qubits[0])
            loc = (((i + 1) + 0.5) * self.cell_len, (target + 0.5) * self.cell_len)
            self.draw_single_gate(circ_surf, op_name.upper(), loc)
        elif op_name.upper() in self.single_gates_wparam:
            target = qreg.index(circuit_instruction.qubits[0])
            loc = (((i + 1) + 0.5) * self.cell_len, (target + 0.5) * self.cell_len)
            self.draw_single_gate_wparam(circ_surf, op_name.upper(), loc, circuit_instruction.operation.params[0])
        elif op_name.upper() in self.double_gates:
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
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.process_mousedown(event)
        if event.type == pygame.KEYDOWN:
            self.process_keydown(event)
    
    def process_mousedown(self, event):
        x, y = self.get_mouse_box(event.pos)

        if x is None:
            # shop area click
            for rect, callable in self.global_bbox:
                if rect.collidepoint(event.pos):
                    callable()
                    break
        else: 
            # circuit area click
            if self.mode == "selected":
                self.selected_circuit_click(y)
                    
            if self.mode == "control":
                self.control_circuit_click(y)

    def process_keydown(self, event):
        if self.mode == "rotation":
            print(event.key)
            if event.key == pygame.K_RETURN:
                self.composer.add_single_qubit_gate_wparam(self.selected_gate, self.rotation_box_y, float(self.curr_rot_txt))
                self.curr_rot_txt = ""
                self.curr_count += 1
                self.mode = 'neutral'
            elif event.key == pygame.K_BACKSPACE or event.key == pygame.K_DELETE:
                if len(self.curr_rot_txt) == 0:
                    return
                self.curr_rot_txt = self.curr_rot_txt[:-1]
            else:
                if len(self.curr_rot_txt) < 4:
                    self.curr_rot_txt += event.unicode

    def selected_circuit_click(self, y):
        if self.selected_gate in self.single_gates:
            if self.selected_gate in self.single_gates_nparam:
                # add the gate to the composer circuit
                self.composer.add_single_qubit_gate(self.selected_gate, y)
                # change mode to neutral
                self.mode = 'neutral'
                self.curr_count += 1
            else:
                self.rotation_box_y = y
                self.mode = 'rotation'
        else:
            # add the control node to the overlay layer
            # selected_ctrl_center = ((self.curr_count + 1.5) * self.cell_len, (self.selected_control_y + 0.5) * self.cell_len)
            self.selected_control_y = y
            self.mode = "control"

    def control_circuit_click(self, y):
        if y == self.selected_control_y:
            return
        
        self.composer.add_two_qubit_gate(self.selected_gate, self.selected_control_y, y)
        self.selected_control_y = None
        self.mode = "neutral"
        self.curr_count += 1


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
    composer = Composer(7, "Poganini")
    qgui = SheetMusicGUI(composer)
    qgui.on_execute()