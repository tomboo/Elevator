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


class TestElevatorLogic(unittest.TestCase):

    def test_scenario00(self):
        e = Elevator(ElevatorLogic())
        self.assertEqual(e.current_floor, 1)
        self.assertEqual(e.motor_direction, None)

    def test_scenario01(self):
        e = Elevator(ElevatorLogic())
        e.call(5, DOWN)
        e.run_until_stopped()
        e.call(3, DOWN)
        e.run_until_stopped()
        e.run_until_stopped()
        self.assertEqual(e.current_floor, 1)
        self.assertEqual(e.motor_direction, None)

        # self.assertEqual('foo'.upper(), 'FOO')

    def test_isupper(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())

    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)

if __name__ == '__main__':
    unittest.main()
