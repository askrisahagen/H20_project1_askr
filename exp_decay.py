class ExponentialDecay:
    def __init__(self, a):
        self.a = a

    def __call__(self, t, u):
        self.u = u
        self.t = t

        return -a*u

    def solve(u0, T, dt):

        return t, u
