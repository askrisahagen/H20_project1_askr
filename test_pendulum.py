import pendulum
import math
import pytest
import numpy as np

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

def test_exceptions():
    ta = pendulum.Pendulum(L=2.7)
    with pytest.raises(AttributeError):
        ta.t
        ta.theta
        ta.omega

def test_atrest():
    ta = pendulum.Pendulum(L=2.7)
    ta.solve((0,0), [0,30], 0.2)
    assert all(np.isclose(0, ta.theta))
    assert all(np.isclose(0, ta.omega))
    assert all(np.isclose(ta.t, np.arange(0, 30 + 0.2, 0.2)))

def test_radius():
    ta = pendulum.Pendulum(L=2.7)
    ta.solve((math.pi/6,0.15), [0,30], 0.2)
    assert all(np.isclose(ta.x**2+ta.y**2, 2.7**2))