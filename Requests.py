# -*- coding: utf-8 -*-
"""
Created on Fri Jan 29 12:43:01 2016

@author: Tom
"""

# from collections import deque

SELECT = 0  # 'select'
UP = 1      # 'up'
DOWN = 2    # 'down'


class Requests(object):
    def __init__(self):
        self._requests = dict()
        self._requests[SELECT] = set()
        self._requests[UP] = set()
        self._requests[DOWN] = set()

    def insert(self, floor, direction=None):
        column = SELECT if direction is None else direction
        self._requests[column].add(floor)

    def delete(self, floor, direction):
        assert(direction in (UP, DOWN))
        self._requests[SELECT].discard(floor)
        self._requests[direction].discard(floor)

    def is_empty(self):
        for column in (SELECT, UP, DOWN):
            if self._requests[column]:
                return False
        return True

    def is_member(self, floor, direction):
        for column in (SELECT, direction):
            if floor in self._requests[column]:
                return True
        return False

    def is_max(self, floor, direction):
        assert(direction in (UP, DOWN))
        for column in (SELECT, UP, DOWN):
            for f in self._requests[column]:
                if direction is UP:
                    if f > floor:
                        return False
                else:
                    if f < floor:
                        return False
        return True

    def display(self):
        print('table:')
        for column in (SELECT, UP, DOWN):
            print(column, ':', self._requests[column])
        print()


def main():
    requests = Requests()
    print('is_empty', ':', requests.is_empty())
    requests.insert(3)
    requests.display()
    print('is_member(3, UP)', ':', requests.is_member(3, UP))
    print('is_member(5, UP)', ':', requests.is_member(5, UP))
    requests.insert(5)
    requests.delete(3, UP)
    requests.display()
    requests.insert(2)
    requests.insert(2, DOWN)
    requests.insert(2, UP)
    requests.delete(2, DOWN)
    requests.display()
    print('is_empty', ':', requests.is_empty())
    print('is_max(5, UP)', ':', requests.is_max(5, UP))
    print('is_max(5, DOWN)', ':', requests.is_max(5, DOWN))


if __name__ == '__main__':
    main()
