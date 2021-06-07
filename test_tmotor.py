from rPyControl.hardware.can import CANSocket
from rPyControl.hardware.actuators.tmotor import TMotorQDD
from time import perf_counter
import matplotlib.pyplot as plt
from numpy import sin, cos

bus = CANSocket(interface='can0')

motor = TMotorQDD(bus, device_id=0x002)
motor.torque_limit = 6
time = []
angle = []
err = []
desired = []
t0 = perf_counter()

t_con = 1./2000.
t_log = 1e-2
tl = 0
tc = 0

alpha, dalpha = 0, 0

kp = 11.
kd = 2.5

try:
    
    motor.enable()

    while True:

        t = perf_counter() - t0

        if t - tc >= t_con:
            alpha_d, dalpha_d = 0.75*sin(t*2), 0.75*cos(t*2)
            alpha = motor.state['pos']
            dalpha = motor.state['vel']
            e, de = alpha_d - alpha, dalpha_d - dalpha
            u = kp*e + kd*de
            motor.set_torque(u)
            
            tc = t

        if t - tl >= t_log:
            # print(f"time {round(t, 4)}, pos: {round(alpha, 3)}, speed: {round(dalpha, 3)}")
            # print(motor.state['tor'])
            time.append(t)
            angle.append(alpha)
            desired.append(alpha_d)
            err.append(alpha-alpha_d)
            tl = t


except KeyboardInterrupt:
    motor.set_torque(0)
    motor.disable()
    
# except:
#     motor.set_torque(0)
#     motor.disable()



plt.figure(figsize=(7, 3))
plt.plot(time, desired, 'b--', label=r'$\alpha_d$')
plt.plot(time, angle, 'r', label=r'$\alpha$')
plt.plot(time, err, 'g', label='err')
plt.ylabel(r'Angle $\alpha$ (rad)')
plt.xlabel(r'Time $t$ (s)')
plt.grid(color='gray', linestyle='--', alpha=0.7)
plt.grid(True)
plt.xlim([time[0], time[-1]])
plt.legend()
plt.tight_layout()
plt.savefig('angles.png', dpi=300)
plt.show()
