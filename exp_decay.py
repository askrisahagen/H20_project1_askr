import scipy
from scipy.integrate import solve_ivp
import numpy as np

class ExponentialDecay:
    def __init__(self, a):
        self.a = a

    def __call__(self, t, u):
        return -self.a*u

    def solve(self, u0, T, dt):
        sol = solve_ivp(self, T, u0, t_eval=np.arange(T[0], T[1] + dt, dt))
        return sol.t, sol.y[0]

if __name__ == "__main__":
    a = 0.4
    u0 = [3.2]
    T = [0, 10]
    dt = 0.2
    decay_model = ExponentialDecay(a)
    t, u = decay_model.solve(u0, T, dt)

    import matplotlib.pyplot as plt
    
    plt.plot(t, u)
    plt.show()