import scipy

class Pendulum:

    def __init__(self, L = 1, M = 1, g = 9.81):
        self.L = L
        self.M = M
        self.g = g

    def __call__(self, t, y):
        self.t = t
        self.theta, self.v = y
        import math
        
        return [self.v,-(self.g/self.L)*math.sin(self.theta)]

    def solve(self, y0, T, dt, angles = "rad"):
        self.y0 = y0
        self.T = T
        self.dt = dt
        if angles == "deg":
            from math import pi
            self.y0 = [y0[0]*pi/180, y0[1]]

        import numpy as np
        sol = scipy.integrate.solve_ivp(self, self.T, self.y0, 
                t_eval=np.linspace(self.T[0], self.T[1], (self.T[1]-self.T[0])/self.dt))
        return sol.t, sol.y