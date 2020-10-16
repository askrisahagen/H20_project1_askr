import scipy
import math as m
from scipy.integrate import solve_ivp
import numpy as np
import matplotlib.animation as animation
import matplotlib.pyplot as plt

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

    def solve(self, y0, T, dt, angles = "rad", method="Radau"):
        self.T = T
        self.dt = dt
        if angles == "deg":
            y0[0] = y0[0]*m.pi/180
        self.sol = solve_ivp(self, self.T, y0, t_eval=np.arange(self.T[0], self.T[1] + self.dt, self.dt))

    @property
    def t(self):
        return self.sol.t
    
    @property
    def theta1(self):
        return self.sol.y[0]

    @property
    def theta2(self):
        return self.sol.y[2]

    @property
    def x1(self):
        return self.L1*np.sin(self.theta1)

    @property
    def x2(self):
        return self.x1 + self.L2*np.sin(self.theta2)

    @property
    def y1(self):
        return -self.L1*np.cos(self.theta1)

    @property
    def y2(self):
        return self.y1 - self.L2*np.cos(self.theta2)

    @property
    def potential(self):
        P1 = self.M1*self.g*(self.y1 + self.L1)
        P2 = self.M2*self.g*(self.y2 + self.L1 + self.L2)
        return P1 + P2

    @property
    def vx1(self):
        return np.gradient(self.x1, self.t)

    @property
    def vx2(self):
        return np.gradient(self.x2, self.t)

    @property
    def vy1(self):
        return np.gradient(self.y1, self.t)

    @property
    def vy2(self):
        return np.gradient(self.y2, self.t)

    @property
    def kinetic(self):
        K1 = .5*self.M1*(self.vy1**2 + self.vx1**2)
        K2 = .5*self.M2*(self.vy2**2 + self.vx2**2)
        return K1 + K2

    @property
    def create_animation(self):
        # Create empty figure
        fig = plt.figure()
        
        # Configure figure
        plt.axis('equal')
        plt.axis((-(self.L1 + self.L2)*1.5, (self.L1 + self.L2)*1.5, -(self.L1 + self.L2)*1.5, (self.L1 + self.L2)*1.5))
        
        # Make an "empty" plot object to be updated throughout the animation
        self.pendulums, = plt.plot([], [], 'o-', lw=2)
        
        def _next_frame(i):
            self.pendulums.set_data((0, self.x1[i], self.x2[i]),
                                    (0, self.y1[i], self.y2[i]))
            return self.pendulums,

        # Call FuncAnimation
        self.animation = animation.FuncAnimation(fig,
                                                 _next_frame,
                                                 frames=[int(i) for i in list(np.around(np.linspace(0, len(self.x1) -1, 60*self.T[1])))], 
                                                 repeat=None,
                                                 interval=1000/60, 
                                                 blit=True)

    @property
    def show_animation(self):
        plt.show()

    def save_animation(self, filename):
        self.animation.save(filename, fps=60)


if __name__ == "__main__":
    pend = DoublePendulum()
    pend.solve((m.pi/6, 0.15, m.pi/6, 0.15), [0,10], 0.02) # løser bevegelsen til pendelen

    """
    Oppgave 4
    Animere dobbel pendel. 
    """
    pend.create_animation # lager animasjonen
    pend.save_animation("example_simulation.mp4") #lagrer den på pcen

    import matplotlib.pyplot as plt
    plt.plot(pend.x1, pend.y1) 
    plt.plot(pend.x2, pend.y2) 
    plt.show()

    plt.plot(pend.t, pend.kinetic)
    plt.plot(pend.t, pend.potential)
    plt.plot(pend.t, pend.kinetic + pend.potential)
    plt.show() # plotter kinetic og potential i samme graf

if __name__ == "__main__":

    """
    Oppgave 5
    Endre initial verdiene over samme t verdier
    """
    pend = DoublePendulum()
    pend.solve((m.pi/6, 0.15, m.pi/6, 0.15), [0,10], 0.02)
    plt.plot(pend.x1, pend.y1, "b")
    plt.plot(pend.x2, pend.y2, "b")

    pend = DoublePendulum()
    pend.solve((m.pi/5, 0.1, m.pi/4, 2), [0,10], 0.02)
    plt.plot(pend.x1, pend.y1, "g")
    plt.plot(pend.x2, pend.y2, "g")

    pend = DoublePendulum(L1 = 1.1, M1 = 9, M2 = 1.1, L2 = 0.9)
    pend.solve((m.pi/6, 0.15, m.pi/6, 0.15), [0,10], 0.02)
    plt.plot(pend.x1, pend.y1, "r")
    plt.plot(pend.x2, pend.y2, "r")

    plt.show()