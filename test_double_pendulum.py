import double_pendulum
import math as m
import pytest
import numpy as np

def test_atrest():
    ta = double_pendulum.DoublePendulum(L1=2.7, L2=2)
    ta.solve((0, 0, 0, 0), [0,10], 0.02)
    assert all(np.isclose(0, ta.theta1))
    assert all(np.isclose(0, ta.theta2))
    assert all(np.isclose(ta.t, np.arange(0, 10 + 0.02, 0.02)))

def test_exceptions():
    ta = double_pendulum.DoublePendulum(L1=2.7, L2=2)
    with pytest.raises(AttributeError):
        ta.t
        ta.theta1
        ta.theta2

def test_radius():
    ta = double_pendulum.DoublePendulum(L1=2.7, L2=2)
    ta.solve((m.pi/6, 0.15, m.pi/6, 0.15), [0,10], 0.02)
    assert all(np.isclose(ta.x1**2+ta.y1**2, 2.7**2))