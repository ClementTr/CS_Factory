from factory import Factory
from robot import Robot
from launcher import launch_robot
import threading
import time

if __name__ == '__main__':
    start = time.time()

    # Create Factory
    cs_factory = Factory(100, 10)

    #Launch 2 first robots
    launch_robot(cs_factory, 2)

    # Wait for all threads to complete
    for rt in cs_factory.robots:
        rt.join()
        print("Stopping " + rt.name)
    print ("Exiting Main Thread")

    # Buy last robots
    cs_factory.final_buy()
    # Display stocks and achievment
    cs_factory.get_log()

    # Display algo time needed
    end = time.time()
    print("Time: ", end - start)
