def launch_robot(factory, num_robot=1):
    for robot in range(num_robot):
        factory.create_robot()
        factory.robots[-1].start()
