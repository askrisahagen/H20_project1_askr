import exp_decay
import math

def test_derivative():
    ta = exp_decay.ExponentialDecay(0.4)
    assert math.isclose(ta(0, 3.2), -1.28)