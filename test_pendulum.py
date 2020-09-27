import pendulum
import math
import pytest

def test_derivative():
    ta = pendulum.Pendulum(L=2.7)
    theta, v = ta(0, [math.pi/6, 0.15])
    assert math.isclose(theta, 0.15)
    assert math.isclose(v, -1.81666666667)

def test_motionless():
    ta = pendulum.Pendulum()
    theta, v = ta(0, [0, 0])
    assert math.isclose(theta, 0)
    assert math.isclose(v, 0)