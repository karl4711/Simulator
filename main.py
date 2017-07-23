from robot import *
from multiprocessing.dummy import Pool as ProcessPool 

# online_motivation, ad_acceptance, mission_skill, consumption_ability
r5 = Robot('r5',50, 50, 50, 50)
r6 = Robot('r6',60, 60, 60, 60)
r7 = Robot('r7',70, 70, 70, 70)
r8 = Robot('r8',80, 80, 80, 80)
r9 = Robot('r9',90, 90, 90, 90)

r4 = Robot('r4',40, 40, 40, 40)
r3 = Robot('r3',30, 30, 30, 30)
r2 = Robot('r2',20, 20, 20, 20)
r1 = Robot('r1',10, 10, 10, 10)


test_duration = 300
test_interval = 20
test_prefix = 'test_'

test_r = Robot(test_prefix, 50, 50, 50, 50, test_duration)

# robots = [r1, r2, r3, r4, r5, r6, r7, r8, r9, test_r]
robots = [r1]


def run(robot):
    if robot.name == test_prefix:
        current_interval = test_interval - 1
        test_number = 1

        while True:
            current_interval += 1
            if current_interval >= test_interval:
                current_interval = 0
                print('start a test..', test_number)

                robot.name = test_prefix + str(test_number)
                robot.start()
                test_number += 1

            time.sleep(1)
    else:
        robot.start()


if __name__ == "__main__":


    # run(r4)

    pool = ProcessPool(10) 
    pool.map(run, robots)

    pool.close() 
    pool.join() 