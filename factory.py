from robot import Robot
import threading

class Factory:
    '''
    Class Factory contains a list of object Robots.
    For our project, the obj is to make this list equals to 100.
    It also contains all stock information.
    '''
    def __init__(self, nb_robots_target, nb_working_robots):
        '''
        Class Constructor
        '''
        self.robots = []
        self.foobar = 0
        self.foo = 0 #2s
        self.bar = 0 #.5-2s
        self.money = 0
        self.nb_robots_target = nb_robots_target
        self.nb_working_robots = nb_working_robots
        self.robotsLock = threading.Lock() # Thread Lock
        self.steps = {"Step1": 0, "Step2": 0, "Step3": 0,
                      "Step4": 0, "Step5": 0}

    def create_robot(self):
        '''
        Add Robot to factory (see Robot constructor).
        '''
        Robot(self)

    def final_buy(self):
        '''
        Function allow buy robots until there is no more money or the
        number of robots targeted is reached.
        '''
        while self.money > 0:
            self.create_robot()
            self.money -= 1
            self.foo -= 6
            if len(self.robots) >= self.nb_robots_target:
                break;

    def get_log(self):
        '''
        Print attributes states.
        '''
        print("Bar: ", self.bar)
        print("Foo: ", self.foo)
        print("Foobar: ", self.foobar)
        print("Money: ", self.money)
        print("Robots: ", len(self.robots))

    def activate_step(self, step, log):
        '''
        Factory process log system
        '''
        if not self.steps[step]:
            self.steps[step] += 1
            print(step + ": " + log)
