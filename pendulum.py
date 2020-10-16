import scipy
import math as m
from scipy.integrate import solve_ivp
import numpy as np

class Pendulum:

    def __init__(self, L = 1, M = 1, g = 9.81):
        self.L = L
        self.M = M
        self.g = g

    def __call__(self, t, y):
        angularvelocity = - self.g/self.L*m.sin(y[0])
        motion = y[1]
        return (motion, angularvelocity)

    def solve(self, y0, T, dt, angles = "rad"):
        if angles == "deg":
            y0[0] = y0[0]*m.pi/180
        self.sol = solve_ivp(self, T, y0, t_eval=np.arange(T[0], T[1] + dt, dt))

    @property
    def t(self):
        return self.sol.t
    
    @property
    def theta(self):
        return self.sol.y[0]

    @property
    def omega(self):
        return self.sol.y[1]

    @property
    def x(self):
        return self.L*np.sin(self.sol.y[0])

    @property
    def y(self):
        return -self.L*np.cos(self.sol.y[0])

    @property
    def potential(self):
        return self.M*self.g*(self.y+self.L)

    @property
    def vx(self):
        return np.gradient(self.x, self.t)

    @property
    def vy(self):
        return np.gradient(self.y, self.t)
    
    @property
    def kinetic(self):
        return .5*self.M*(self.vy**2 + self.vx**2)


if __name__ == "__main__":

    pend = Pendulum(L=2.7)
    pend.solve((m.pi/6,0.15), [0,30], 0.2) # løser bevegelsen til pendelen

    import matplotlib.pyplot as plt
    plt.plot(pend.x, pend.y) # plotter bevegelsen over tid
    plt.show()

    plt.plot(pend.t, pend.kinetic)
    plt.plot(pend.t, pend.potential)
    plt.plot(pend.t, pend.kinetic + pend.potential)
    plt.show() # plotter kinetic og potential i samme graf

class DampenedPendulum(Pendulum):
    
    def __init__(self, B, L = 1, M = 1, g = 9.81):
        super().__init__(L, M, g)
        self.B = B

    def __call__(self, t, y):
        angularvelocity = - self.g/self.L*m.sin(y[0]) - self.B/self.M*y[1]
        motion = y[1]
        return (motion, angularvelocity)

if __name__ == "__main__":
    pend = DampenedPendulum(0.2, L=2.7)
    pend.solve((m.pi/6,0.15), [0,30], 0.2) # løser bevegelsen til pendelen

    import matplotlib.pyplot as plt
    plt.plot(pend.x, pend.y) # plotter bevegelsen over tid
    plt.show()

    plt.plot(pend.t, pend.kinetic)
    plt.plot(pend.t, pend.potential)
    plt.plot(pend.t, pend.kinetic + pend.potential)
    plt.show() # plotter kinetic og potential i samme graf

    # Her er det veldig lett å se på plottet til engeri at den går nedover med tid