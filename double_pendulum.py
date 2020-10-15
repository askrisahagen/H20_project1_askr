import scipy
import math as m
from scipy.integrate import solve_ivp
import numpy as np

class DoublePendulum:

    def __init__(self, M1 = 1, L1 = 1, M2 = 1, L2 = 1, g = 9.81):
        self.L1 = L1
        self.M1 = M1
        self.L2 = L2
        self.M2 = M2
        self.g = g

    def __call__(self, t, y):
        angularvelocity1, angularvelocity2 = self.domega1_dt(y[0], y[2], y[1], y[3]), self.domega2_dt(y[0], y[2], y[1], y[3])
        motion1, motion2 = y[1], y[3] 
        return (motion1, angularvelocity1, motion2, angularvelocity2)

    def delta(self, theta1, theta2):
        return theta2-theta1


    def domega1_dt(self, theta1, theta2, omega1, omega2):
        return  (self.M2*self.L1*omega1**2*np.sin(self.delta(theta1,theta2))*np.cos(self.delta(theta1,theta2)) + 
                self.M2*self.g*np.sin(theta2)*np.cos(self.delta(theta1,theta2)) + 
                self.M2*self.L2*omega2**2*np.sin(self.delta(theta1,theta2)) - \
                (self.M1+self.M2)*self.g*np.sin(theta1))/((self.M1+self.M2)*self.L1 - 
                self.M2*self.L1*np.cos(self.delta(theta1, theta2))**2)


    def domega2_dt(self, theta1, theta2, omega1, omega2):
        return  (-self.M2*self.L1*omega2**2*np.sin(self.delta(theta1,theta2))*np.cos(self.delta(theta1,theta2)) + 
                (self.M1+self.M2)*self.g*np.sin(theta1)*np.cos(self.delta(theta1,theta2)) - 
                (self.M1+self.M2)*self.L1*omega1**2*np.sin(self.delta(theta1,theta2)) - \
                (self.M1+self.M2)*self.g*np.sin(theta2))/((self.M1+self.M2)*self.L2 - 
                self.M2*self.L2*np.cos(self.delta(theta1, theta2))**2)

    def solve(self, y0, T, dt, angles = "rad"):
        if angles == "deg":
            y0[0] = y0[0]*m.pi/180
        self.sol = solve_ivp(self, T, y0, t_eval=np.arange(T[0], T[1] + dt, dt))
