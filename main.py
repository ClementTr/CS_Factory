import threading
import random
import time

class Factory:
    '''
    Class Factory contains a list of object Robots
    For our project, the obj is to make this list equals to 100
    It also contains all stock information
    '''
    def __init__(self):
        self.robots = []
        self.foobar = 0
        self.foo = 0 #2s
        self.bar = 0 #.5-2s
        self.money = 0

    def create_robot(self):
        Robot(self)


if __name__ == '__main__':
    # Create Factory
    cs_factory = Factory()
