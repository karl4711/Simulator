from robot import *
from multiprocessing.dummy import Pool as ThreadPool 

# online_motivation, ad_acceptance, mission_skill, consumption_ability
r1 = Robot('r1',50, 50, 50, 50)
r2 = Robot('r2',60, 60, 60, 60)
r3 = Robot('r3',70, 70, 70, 70)
r4 = Robot('r4',80, 80, 80, 80)

robots = [r1, r2, r3, r4]

def run(robot):
	robot.start()


if __name__ == "__main__":

	pool = ThreadPool(4) 
	results = pool.map(run, robots)

	pool.close() 
	pool.join() 