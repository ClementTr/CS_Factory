import threading
import random
import time

class Factory:
    '''
    Class Factory contains a list of object Robots.
    For our project, the obj is to make this list equals to 100.
    It also contains all stock information.
    '''
    def __init__(self):
        '''
        Class Constructor
        '''
        self.robots = []
        self.foobar = 0
        self.foo = 0 #2s
        self.bar = 0 #.5-2s
        self.money = 0

    def create_robot(self):
        '''
        Add Robot to factory (see Robot constructor)
        '''
        Robot(self)

class Robot(threading.Thread):
    def __init__(self, factory):
        '''
        Class Constructor
        '''
        threading.Thread.__init__(self)
        self.factory = factory
        self.factory.robots.append(self)
        self.name = "robot_" + str(len(self.factory.robots)-1)

    def move(self):
        '''
        Move function make robot sleeping 2 seconds.
        '''
        time.sleep(2)

    def isin_stock(self):
        '''
        Check if there are enough foo+bar for robot in its factory to create
        FooBar.
        '''
        if (self.factory.foo > 0) & (self.factory.bar > 0):
            return True
        return False

    def mine_foo(self):
        '''
        Mining Foo is waiting 2 seconds and remove one foo of robot's factory.
        '''
        print(self.name + " mining Foo")
        time.sleep(2)
        self.factory.foo += 1

    def mine_bar(self):
        '''
        Mining Bar is waiting random time (between 0.5 and 2 seconds)
        and remove one bar of robot's factory.
        '''
        print(self.name + " mining Bar")
        making_time = random.uniform(.5, 2)
        time.sleep(making_time)
        self.factory.bar += 1

    def create_foobar(self):
        '''
        Function creating FooBar remove 1 foo and 1 bar from robot's factory.
        It's also adding one foobar.
        Add assert as we cannot have negative value in stock's factory.
        '''
        print(self.name + " created FooBar")
        self.factory.foo -= 1
        self.factory.bar -= 1
        self.factory.foobar += 1
        assert(self.factory.foo >= 0)
        assert(self.factory.bar >= 0)

    def fail_foobar(self):
        '''
        Function fail FooBar is removing 1 foo from robot's factory
        and asserting stock is positive.
        '''
        print(self.name + " failed FooBar")
        self.factory.foo -= 1
        assert(self.factory.foo >= 0)

    def sell_foobar(self):
        '''
        Function reomve 1 foobar from robot's factory and increment +1
        money attribute.
        Assert FooBar stock is positive after removing FooBar.
        '''
        print(self.name + " sold 1 FooBar")
        time.sleep(1)
        self.factory.money += 1
        self.factory.foobar -= 1
        assert(self.factory.foobar >= 0)

    def can_buy(self):
        '''
        Check if enough stock to buy a robot
        '''
        if (self.factory.money >= 3) & (self.factory.foo >= 6):
            return True
        return False

    def run(self):
        self.mine_foo()
        self.mine_bar()


if __name__ == '__main__':
    # Create Factory
    cs_factory = Factory()
    cs_factory.create_robot()


    cs_factory.robots[0].start()
    cs_factory.robots[0].join()
    print("Stopping " + cs_factory.robots[0].name)

    print("Bar: ", cs_factory.bar)
    print("Foo: ", cs_factory.foo)
