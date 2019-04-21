from launcher import launch_robot
import threading
import random
import time

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

    def isin_stock(self, val_min=0):
        '''
        Check if there are enough foo+bar for robot in its factory to create
        FooBar.
        '''
        if (self.factory.foo > val_min) & (self.factory.bar > 0):
            return True
        return False

    def mine_foo(self):
        '''
        Mining Foo is waiting 2 seconds and remove one foo of robot's factory.
        '''
        #print(self.name + " mining Foo")
        time.sleep(2)
        self.factory.foo += 1

    def mine_bar(self):
        '''
        Mining Bar is waiting random time (between 0.5 and 2 seconds)
        and remove one bar of robot's factory.
        '''
        #print(self.name + " mining Bar")
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
        #print(self.name + " created FooBar")
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
        #print(self.name + " failed FooBar")
        self.factory.foo -= 1
        assert(self.factory.foo >= 0)

    def sell_foobar(self):
        '''
        Function reomve 1 foobar from robot's factory and increment +1
        money attribute.
        Assert FooBar stock is positive after removing FooBar.
        '''
        #print(self.name + " sold 1 FooBar")
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
        '''
        Having enough foo and money a robot can buy another one.
        It remove money and foo from factory so we assert those
        attributes are still positive.
        Then it launches a new robot as a thread who will be able
        to mine, gather/sell foobar and buy a new robot itself.
        '''
        #print(self.factory.money, self.factory.foo)
        #print(self.name + " bought a robot")
        self.factory.money -= 3
        self.factory.foo -= 6
        assert(self.factory.money >= 0)
        assert(self.factory.foo >= 0)
        launch_robot(self.factory)

    def buy_working_robots(self):
        '''
        Function buy robots until factory have nb_worker_robots.
        First all robots mine.
        Then we use a synchronized Lock to avoid multi bought (make sure
        stocks are not negative)
        '''
        print("Starting " + self.name)
        self.move()
        exitFlag = 0
        while len(self.factory.robots) < self.factory.nb_working_robots:
            self.mine()
            # Get lock to synchronize threads
            self.factory.robotsLock.acquire()
            if self.isin_stock():
                self.try_foobar()
            if exitFlag == 0:
                if self.can_buy():
                    self.buy_robot()
                exitFlag += 1
            # Free lock to release next thread
            self.factory.robotsLock.release()
            exitFlag = 0

    def run(self):
        '''
        Start Thread

        Step1: Create Working Robots
        Step2: Bar Mining
        Step3: Foo Mining
        Step4: Create/Sell FooBar (If not enough money, GOTO Step3)
        Step5: Foo Mining for buying robots
        '''
        self.factory.activate_step("Step1", "Create Working Robots..")
        self.buy_working_robots()
        real_working_robots = len(self.factory.robots)
        needed_resources = self.factory.nb_robots_target - real_working_robots

        self.factory.activate_step("Step2", "Bar Mining..")
        while self.factory.bar < needed_resources:
            self.mine_bar()

        self.factory.activate_step("Step3", "Foo Mining..")
        #660 = 90(make foobar) + 30(pred foobar failed) + 540(buy robots)
        while self.factory.foo < 660:
            self.mine_foo()

        self.factory.activate_step("Step4", "Create/Sell FooBar..")
        while self.factory.money < needed_resources:
            if self.isin_stock(real_working_robots):
                self.try_foobar()
            else:
                #print("More Foo Mining")
                self.mine_foo()

        self.factory.activate_step("Step5", "Foo Mining for buying robots..")
        while self.factory.foo < 540:
            #print("Not Enough to buy")
            self.mine_foo()
