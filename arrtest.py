import matplotlib.pyplot as plt
import numpy as np
from numpy import pi , sin, cos
from sympy import *

angle = [1,2,3,4]
velocity = [0,0,8,9]
control = [1,1,2,3]

# angle_t = np.array(angle)
# velocity_t = np.array(velocity)
# control_t = np.array(control)
csv_data = np.vstack((angle, velocity, control))
csv_data_t = csv_data.transpose()
print(csv_data_t.shape)
print(csv_data_t)
# np.savetxt('test.csv', csv_data, delimiter=',')