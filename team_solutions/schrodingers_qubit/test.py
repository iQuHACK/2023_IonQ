from pipelines.pic2num import avg_color
from pipelines.vid2num import batch_process, q_array
from quantum_driver import get_quantum_parameters
import numpy as np

dict = {"v_"}
avgs = []
file = "input_data/flower.jpg"
#avgs.append(avg_color(file))
file = "input_data/flower2.webp"
#avgs.append(avg_color(file))

#param1, param2 = batch_process("videos/")
#param1, param2 = q_array(param1, param2)

#np.savetxt('param1.csv', param1, delimiter=';')
#np.savetxt('param2.csv', param2, delimiter=';')
param1 = np.loadtxt('param1.csv', delimiter=';', dtype=float)
param2 = np.loadtxt('param2.csv', delimiter=';', dtype=float)



print(param1, param2)
n_vids = len(param1[0])
print(avgs)
out_params = get_quantum_parameters(n_vids,param1, param2)
print(out_params)
