# -*- coding: utf-8 -*-
"""
Created on Tue Jan 26 08:08:16 2016

@author: Tom
"""

from Requests import Requests

UP = 1
DOWN = 2


class ElevatorLogic(object):
    """
    An incorrect implementation. Can you make it pass all the tests?

    Fix the methods below to implement the correct logic for elevators.
    The tests are integrated into `README.md`. To run the tests:
    $ python -m doctest -v README.md

    To learn when each method is called, read its docstring.
    To interact with the world, you can get the current floor from the
    `current_floor` property of the `callbacks` object, and you can move the
    elevator by setting the `motor_direction` property. See below for how this
    is done.
    """

    def __init__(self):
        self.callbacks = None
        self._direction = None
        self._requests = Requests()

    def on_called(self, floor, direction):
        """
        This is called when somebody presses the up or down button to call the
        elevator.
        This could happen at any time, whether or not the elevator is moving.
        The elevator could be requested at any floor at any time, going in
        either direction.

        floor: the floor that the elevator is being called to
        direction: the direction the caller wants to go, up or down
        """
        self._requests.insert(floor, direction)
        if self._direction is None:
            if floor > self.callbacks.current_floor:
                self._direction = UP
            elif floor < self.callbacks.current_floor:
                self._direction = DOWN

    def on_floor_selected(self, floor):
        """
        This is called when somebody on the elevator chooses a floor.
        This could happen at any time, whether or not the elevator is moving.
        Any floor could be requested at any time.

        floor: the floor that was requested
        """
        if self._direction == UP and floor <= self.callbacks.current_floor:
            print('select ignored:', floor)
            return
        if self._direction == DOWN and floor >= self.callbacks.current_floor:
            print('select ignored:', floor)
            return
        self._requests.insert(floor)
        if self._direction is None:
            if floor > self.callbacks.current_floor:
                self._direction = UP
            elif floor < self.callbacks.current_floor:
                self._direction = DOWN

    def on_floor_changed(self):
        """
        This lets you know that the elevator has moved one floor up or down.
        You should decide whether or not you want to stop the elevator.
        """
        assert(self.callbacks.motor_direction in (UP, DOWN))

        floor = self.callbacks.current_floor

        maximum = self._requests.is_max(floor, self._direction)
        member = self._requests.is_member(floor, self._direction)
        if maximum or member:
            self.callbacks.motor_direction = None
        if maximum and not member:
            self.change_direction()

    def on_ready(self):
        """
        This is called when the elevator is ready to go.
        Maybe passengers have embarked and disembarked. The doors are closed,
        time to actually move, if necessary.
        """
        assert(self.callbacks.motor_direction is None)

        floor = self.callbacks.current_floor

        if self._direction:
            self._requests.delete(floor, self._direction)

            if self._requests.is_empty():
                self._direction = None
                assert(self.callbacks.motor_direction is None)
            elif self._requests.is_max(floor, self._direction):
                self.change_direction()
                assert(self.callbacks.motor_direction is None)
                if self._requests.is_member(floor, self._direction):
                    self._requests.delete(floor, self._direction)
                else:
                    self.callbacks.motor_direction = self._direction
            else:
                self.callbacks.motor_direction = self._direction

    def change_direction(self):
        assert(self._direction in (UP, DOWN))
        if self._direction is UP:
            self._direction = DOWN
        elif self._direction is DOWN:
            self._direction = UP
