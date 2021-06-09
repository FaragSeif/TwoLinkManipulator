from rPyControl.hardware.can import CANSocket
from rPyControl.hardware.actuators.tmotor import TMotorQDD
from time import perf_counter
import matplotlib.pyplot as plt
import numpy as np
from numpy import pi , sin, cos
from sympy import *


# motor init
bus = CANSocket(interface='can0')
motor = TMotorQDD(bus, device_id=0x002)
motor.torque_limit = 5

# time variables
time = []
angle = []
velocity = []
control = []
t0 = perf_counter()

# smapling time and control time
t_con = 1./500.
t_log = 1./500.
tl = 0
tc = 0

# initial values
alpha, dalpha = 0, 0

kp = 6.
kd = 1.1

# b, i = symbols('b i')
# b_i = Eq(-b/i)

# A = np.array([[0, 1],
#               [0, b_i]])

# A_d_approx = np.eye(2) + T*A 
# B_d_approx = T*B

try:
    
    motor.enable()

    while True:

        t = perf_counter() - t0

        if t - tc >= t_con:
            alpha = motor.state['pos']
            dalpha = motor.state['vel']
            u = 0.45*sin(t*2)
            motor.set_torque(u)
            
            # print(f"time {round(t, 4)}, pos: {round(alpha, 3)}, speed: {round(dalpha, 3)}")
            # print(motor.state['tor'])

            control.append(u)
            time.append(t)
            angle.append(alpha)
            velocity.append(dalpha)

            tc = t


except KeyboardInterrupt:
    motor.set_torque(0)
    motor.disable()

csv_data = np.vstack((angle, velocity, control))
csv_data_t = csv_data.transpose()
np.savetxt('test.csv', csv_data_t, delimiter=',')

plt.figure(figsize=(7, 3))
plt.plot(time, angle, 'r', label=r'$\alpha$')
plt.plot(time, velocity, 'b', label='vel')
plt.ylabel(r'Angle $\alpha$ (rad)')
plt.xlabel(r'Time $t$ (s)')
plt.grid(color='gray', linestyle='--', alpha=0.7)
plt.grid(True)
plt.xlim([time[0], time[-1]])
plt.legend()
plt.tight_layout()
plt.savefig('angles.png', dpi=300)
plt.show()
