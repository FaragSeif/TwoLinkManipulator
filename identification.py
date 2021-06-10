from rPyControl.hardware.can import CANSocket
from rPyControl.hardware.actuators.tmotor import TMotorQDD
from time import perf_counter
import matplotlib.pyplot as plt
import numpy as np
from numpy import pi , sin, cos


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
tc = 0
counter = 1

# initial values
alpha, dalpha = 0, 0

try:
    
    motor.enable()

    while True:

        t = perf_counter() - t0

        if t - tc >= t_con:
            if counter <= 2500:
                alpha = motor.state['pos']
                dalpha = motor.state['vel']
                u = 0.40*sin(t*4)
                motor.set_torque(u)
            elif counter <= 5000:
                alpha = motor.state['pos']
                dalpha = motor.state['vel']
                if counter % 1000 < 500:
                    u = 0.3
                else:
                    u = -0.3
                motor.set_torque(u)
            elif counter <= 7500:
                alpha = motor.state['pos']
                dalpha = motor.state['vel']
                u = 0.4*sin(t*12)
                motor.set_torque(u)
            elif counter <= 10000:
                alpha = motor.state['pos']
                dalpha = motor.state['vel']
                if counter % 100 < 50:
                    u = 0.5
                else:
                    u = -0.5
                motor.set_torque(u)
            elif counter <= 12500:
                alpha = motor.state['pos']
                dalpha = motor.state['vel']
                u = 0.90*sin(t*4)
                motor.set_torque(u)
            elif counter <= 15000:
                alpha = motor.state['pos']
                dalpha = motor.state['vel']
                if counter % 500 < 250:
                    u = 1
                else:
                    u = -1
                motor.set_torque(u)
            elif counter <= 17500:
                alpha = motor.state['pos']
                dalpha = motor.state['vel']
                u = 0.90*sin(t*12)
                motor.set_torque(u)
            elif counter <= 20000:
                alpha = motor.state['pos']
                dalpha = motor.state['vel']
                if counter % 100 < 50:
                    u = 1
                else:
                    u = -1
                motor.set_torque(u)
            else:
                break
            
            control.append(u)
            time.append(t)
            angle.append(alpha)
            velocity.append(dalpha)

            tc = t
            counter = counter + 1


except KeyboardInterrupt:
    motor.set_torque(0)
    motor.disable()

csv_data = np.vstack((time ,angle, velocity, control))
csv_data_t = csv_data.transpose()
np.savetxt('highFreqCont1.csv', csv_data_t, delimiter=',')

plt.figure(figsize=(7, 3))
plt.plot(time, angle, 'r', label=r'$\alpha$')
plt.plot(time, velocity, 'b', label='vel')
plt.plot(time, control, 'g', label='ctrl')
plt.ylabel(r'Angle $\alpha$ (rad)')
plt.xlabel(r'Time $t$ (s)')
plt.grid(color='gray', linestyle='--', alpha=0.7)
plt.grid(True)
plt.xlim([time[0], time[-1]])
plt.legend()
plt.tight_layout()
plt.savefig('angles.png', dpi=300)
plt.show()
