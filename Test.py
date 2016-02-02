# -*- coding: utf-8 -*-
"""
Created on Tue Jan 26 19:28:54 2016

@author: Tom
"""


import unittest

from Elevator import Elevator
from ElevatorLogic import ElevatorLogic

UP = 1
DOWN = 2
FLOOR_COUNT = 6


# https://github.com/mshang/python-elevator-challenge/blob/master/README.md


class TestElevatorLogic(unittest.TestCase):

    def test_basic_usage(self):
        e = Elevator(ElevatorLogic())
        self.assertEqual(e._current_floor, 1)
        e.call(5, DOWN)
        e.run_until_stopped()
        self.assertEqual(e._current_floor, 5)
        e.select_floor(1)
        e.call(3, DOWN)
        e.run_until_stopped()
        self.assertEqual(e._current_floor, 3)
        e.run_until_stopped()
        self.assertEqual(e._current_floor, 1)

    def test_directionality1(self):
        e = Elevator(ElevatorLogic())
        e.call(2, DOWN)
        e.select_floor(5)
        e.run_until_stopped()
        self.assertEqual(e._current_floor, 5)
        e.run_until_stopped()
        self.assertEqual(e._current_floor, 2)

    def test_directionality2(self):
        e = Elevator(ElevatorLogic())
        e.select_floor(3)
        e.select_floor(5)
        e.run_until_stopped()
        self.assertEqual(e._current_floor, 3)
        e.select_floor(2)       # ignored
        e.run_until_stopped()
        self.assertEqual(e._current_floor, 5)
        e.run_until_stopped()   # nothing happens, because e.select_floor(2) was ignored
        self.assertEqual(e._current_floor, 5)
        e.select_floor(2)
        e.run_until_stopped()
        self.assertEqual(e._current_floor, 2)

    def test_changing_direction1(self):
        '''
        The process of switching directions is a bit tricky. Normally, if an
        elevator going up stops at a floor and there are no more requests at
        higher floors, the elevator is free to switch directions right away.
        However, if the elevator was called to that floor by a user indicating
        that she wants to go up, the elevator is bound to consider itself
        going up.
        '''
        e = Elevator(ElevatorLogic())
        e.call(2, DOWN)
        e.call(4, UP)
        e.run_until_stopped()
        self.assertEqual(e._current_floor, 4)
        e.select_floor(5)
        e.run_until_stopped()
        self.assertEqual(e._current_floor, 5)
        e.run_until_stopped()
        self.assertEqual(e._current_floor, 2)

    def test_changing_direction2(self):
        '''
        If nobody wants to go further up though, the elevator can turn around.
        '''
        e = Elevator(ElevatorLogic())
        e.call(2, DOWN)
        e.call(4, UP)
        e.run_until_stopped()
        self.assertEqual(e._current_floor, 4)
        e.run_until_stopped()
        self.assertEqual(e._current_floor, 2)

    def test_changing_direction3(self):
        '''
        If the elevator is called in both directions at that floor, it must
        wait once for each direction. You may have seen this too. Some
        elevators will close their doors and reopen them to indicate that
        they have changed direction.
        '''
        e = Elevator(ElevatorLogic())
        e.select_floor(5)
        e.call(5, UP)
        e.call(5, DOWN)
        e.run_until_stopped()
        self.assertEqual(e._current_floor, 5)

        # Here, the elevator considers itself to be going up, as it favors
        # continuing in the direction it came from.
        e.select_floor(4)  # ignored
        e.run_until_stopped()
        self.assertEqual(e._current_floor, 5)

        # Since nothing caused the elevator to move further up, it now waits
        # for requests that cause it to move down.
        e.select_floor(6)  # ignored
        e.run_until_stopped()
        self.assertEqual(e._current_floor, 5)

        # Since nothing caused the elevator to move down, the elevator now
        # considers itself idle. It can move in either direction.
        e.select_floor(6)
        e.run_until_stopped()
        self.assertEqual(e._current_floor, 6)


if __name__ == '__main__':
    unittest.main()
