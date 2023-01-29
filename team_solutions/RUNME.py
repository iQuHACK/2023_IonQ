#{
# AUTHORS: Brandon Barton, Hakan Ayaz, Joshua Moler,
# George Grattan 
# 
# }


#Color imports
from math import floor 
from PIL import Image
from time import sleep 

#==
import matplotlib.pyplot as plt
import cirq 
import cirq_ionq
import random
from itertools import combinations
from math import factorial
from numpy import pi 
import os 



#Function Defintions

#Stroke combination 
def image_combination(image1,image2):
    background = Image.open(image1)
    overlay = Image.open(image2)

    background = background.convert("RGBA")
    overlay = overlay.convert("RGBA")

    new_img = Image.blend(background, overlay, 0.3)

    new_img.save("./painting.png","PNG")
    return "./painting.png"

#Mood Object 
class MoodImage:
    def __init__(self,state_num,perlinOrManual):
        self.state = state_num
        self.mood_mapping = {0:"anger1",1:"anger2",2:"anger3",3:"anger4",4:"anticipation1",5:"anticipation2",6:"anticipation3",7:"anticipation4", 
    8:"disgust1",9:"disgust2",10:"disgust3",11:"disgust4",12:"fear1",13:"fear2",14:"fear3",15:"fear4",16:"joy1",17:"joy2",18:"joy3",19:"joy4",20:"sadness1",21:"sadness2",22:"sadness3",23:"sadness4",24:"surprise1",25:"surprise2",
    26:"surprise3",27:"surprise4",28:"trust1",29:"trust2",30:"trust3",31:"trust4"} 
        self.perlinOrManual = perlinOrManual
        self.painting = self.moodProcess(state_num) 
        self.state = state_num
        img = Image.open(self.painting)
        img.save("./painting.png","PNG")

    def getPasscode(self):
        self.passcode = input('Type in your password for sudo command')

    def moodProcess(self,state_num):
        #self.processState(state_num)
        if self.perlinOrManual == 1: #1 == perlin artist, 0 == manual artist
            return self.perlinSimulation()
        else:
            return self.manualStrokes()
        

    def processState(self,state_num):
        self.stroke_num = floor(self.state/4) + 1 #Mood <- In Perlin Evolution, limited to 3 colors 

    #This is the perlin simluator <- procedurally generated perlin creator 
    def perlinSimulation(self):
        #self.stroke_num += 1
        with open('perlinColor.txt', 'w') as f:
            f.write(str(self.state) + '\n')  
        with open('perlinStroke.txt', 'w') as f:
            f.write(str(self.stroke_num) + '\n') 
        os.system("bash perlinRun.sh")
        os.system("rm perlinColor.txt")
        os/syste,("rm perlinStroke.txt")
        return "./images/perlin_strokes/currentStroke.png"


    #This is the manual strokes come hackathon participants
    def manualStrokes(self):
        file_name = "./images/org_strokes/" + str(self.mood_mapping[self.state]) + ".png"
        return file_name

    def addStroke(self,state_num):
        self.state = state_num
        if self.perlinOrManual == 1:
            self.painting = image_combination(self.painting,self.perlinSimulation())
        else:
            print(self.painting)
            print(self.manualStrokes())
            self.painting = image_combination(self.painting,self.manualStrokes())
    def outputPainting(self):
        img = Image.open(self.painting)
        img = img.convert('RGB')
        img.save("painting.png")

    #Amplitude Amplification Functions 
def diffuse(circuit, qubits, n):
    for _ in range(n):
        circuit.append([cirq.H(qubit) for qubit in qubits])
        circuit.append([cirq.X(qubit) for qubit in qubits])
        circuit.append(cirq.Z(qubits[-1]).controlled_by(*qubits[0:-1]))
        circuit.append([cirq.X(qubit) for qubit in qubits])
        circuit.append([cirq.H(qubit) for qubit in qubits])

def choose_random_operation(theta):
    ops = [cirq.rx(theta), cirq.ry(theta), cirq.rz(theta)]
    return random.choice(ops)

def two_qubit_error(qubit1, qubit2, p2 = None, error_angle = None):
    if p2 == None: 
        p2 = 0.001
    if error_angle == None:
        error_angle = pi/4
    error_qubit = random.choice([qubit1,qubit2])
    error_op = choose_random_operation(error_angle)
    yield error_op.on(error_qubit).with_probability(p2)

def build_monster_grover(nQubits, exponents, nDiffuse, measure, p2 = None, error_angle = None):
    
    
    if len(exponents) != 2*factorial(nQubits)/(2*factorial(nQubits-2)):
        raise IndexError("exponents must have 2*nQubitsCHOOSE2 values.")
    qubits = [cirq.LineQubit(ii) for ii in range(5)]
    circuit = cirq.Circuit()
    
    circuit.append([cirq.H(qubit) for qubit in qubits])
    for nn, (ii, jj) in enumerate(combinations(qubits, r=2)):
        circuit.append(cirq.CZPowGate(exponent = exponents[nn])(ii, jj))
        circuit.append(two_qubit_error(ii, jj, p2, error_angle))
    circuit.append([cirq.X(qubit) for qubit in qubits])
    for nn, (ii, jj) in enumerate(combinations(qubits, r=2)):
        circuit.append(cirq.CZPowGate(exponent =
                                         exponents[int(len(exponents)/2) + nn])(ii, jj))
        circuit.append(two_qubit_error(ii, jj, p2, error_angle))

    circuit.append([cirq.X(qubit) for qubit in qubits])

    diffuse(circuit, qubits, nDiffuse)
    
    if measure:
        circuit.append(cirq.measure(*qubits, key = 'r1'))
    return circuit

def getQuantumPainting(nShots, nQubits, exponents, p2 = 0.01, error_angle = pi):
    nDiffuse = 1
    if len(exponents) != 2*factorial(nQubits)/(2*factorial(nQubits-2)):
        raise IndexError("exponents must have 2*nQubitsCHOOSE2 values.")
    circuit = build_monster_grover(nQubits = nQubits, exponents=exponents,
    nDiffuse=nDiffuse, measure=True, p2=p2, error_angle=error_angle)
    s = cirq.Simulator()
    samples = s.run(circuit, repetitions = nShots)
    counts = list(cirq.get_state_histogram(samples))
    
    outputs = []
    for ii, jj in enumerate(counts):
        outputs += [ii]*int(jj)

    random.shuffle(outputs)
    QuantumArtist = MoodImage(outputs[0],0)
    for ii in outputs[1:]:
        QuantumArtist.addStroke(ii)
    QuantumArtist.outputPainting()
    #return outputs

def main():
    while(True):
        Mood = input("What type of mood would you like (Anger, Sadness, Joy, Fear): ")
        if Mood.lower() in ["anger","joy","sadness","fear"]:
            break
        else:
            print("Enter Valid Mood Type!")
            sleep(1)
    while(True):
        Strokes = input("How many artistic strokes do you want?: ")
        try:
            if int(Strokes) <= 0: raise(Exception)
            break
        except:
            print("Enter Stroke Integer!")
            sleep(1)
            continue
        
    Mood_dict = {"anger":[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],"joy":[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],"sadness":[0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],"fear":[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0]}

    getQuantumPainting(int(Strokes), 5, Mood_dict[Mood.lower()], p2 = 0.01, error_angle = pi)

    print("Your art is in painting.png!")


main()

