class ExponentialDecay:
    def __init__(self, a):
        self.a = a

    def __call__(self, kt, ku):
        self.ku = ku
        self.kt = kt

        return -self.a*self.ku

    def solve(self, u0, T, dt):
        self.u0 = u0
        self.u = []
        self.dt = dt
        
        for i in range(len(self.u0)):
            self.t = [T[0]]
            self.ii = 0
            self.lu = [u0[i]]
            if len(u0) == 1:
                self.u.append(u0[i])
            else:
                self.u.append([u0[i]])

            while self.t[self.ii] <= T[-1]:
                du = self(self.t[self.ii], self.lu[self.ii])
                if len(u0) == 1:
                    du = self(self.t[self.ii], self.lu[self.ii])
                    dlu = self.lu[self.ii] + du*self.dt
                    self.u.append(dlu)
                    self.lu.append(dlu)         
                else:
                    dlu = self.u[i][self.ii]+ du*self.dt
                    self.u[i].append(dlu)
                    self.lu.append(dlu)    
                
                self.t.append(self.t[self.ii] + self.dt)
                self.ii += 1
            
        return self.t, self.u