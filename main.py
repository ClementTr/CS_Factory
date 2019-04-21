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

    def mine(self):
        '''
        Smart mine function that mine foo or bar depending of stock needs.
        '''
        if self.factory.foo - 7 <= self.factory.bar:
            self.mine_foo()
        elif self.factory.money > 3:
            self.mine_foo()
        else:
            self.mine_bar()

    def try_foobar(self):
        '''
        Function called when stock is enough in order to try to create a
        FooBar. Creation success (60%) is determined with random.
        '''
        time.sleep(2)
        success = random.random() <= 0.6
        if success:
            self.create_foobar()
            self.sell_foobar()
        else:
            self.fail_foobar()

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

    def buy_robot(self):
        print(self.factory.money, self.factory.foo)
        print(self.name + " bought a robot")
        self.factory.money -= 3
        self.factory.foo -= 6
        assert(self.factory.money >= 0)
        assert(self.factory.foo >= 0)
        launch_robot(self.factory)

    def buy_working_robots(self, nb_worker_robots):
        print("Starting " + self.name)
        exitFlag = 0
        while len(self.factory.robots) < nb_worker_robots:
            self.mine()
            # Get lock to synchronize threads
            robotsLock.acquire()
            self.try_foobar()
            if exitFlag == 0:
                if self.can_buy():
                    self.buy_robot()
                exitFlag += 1
            # Free lock to release next thread
            robotsLock.release()
            exitFlag = 0

    def run(self):
        '''
        Start Thread
        '''
        num_working_robots = 3
        for i in range(5):
            self.mine_foo()
        self.mine_bar()
        self.try_foobar()
        self.buy_working_robots(num_working_robots)


global launch_robot
global robotsLock
global nb_robots_target

def launch_robot(factory, num_robot=1):
    for robot in range(num_robot):
        factory.create_robot()
        factory.robots[-1].start()

if __name__ == '__main__':
    # Create Factory
    cs_factory = Factory()

    # Thread Lock
    robotsLock = threading.Lock()

    #Launch 2 first robots
    launch_robot(cs_factory, 2)

    # Wait for all threads to complete
    for rt in cs_factory.robots:
        rt.join()
        print("Stopping " + rt.name)
    print ("Exiting Main Thread")

    print("Bar: ", cs_factory.bar)
    print("Foo: ", cs_factory.foo)
