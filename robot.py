import time
import random
from enum import Enum
import requests
from pdb import set_trace

engagement_addr = 'http://127.0.0.1:4711/engagement/%s/%s'

event_addr = 'http://127.0.0.1:4711/event/%s/%s'

class Responses(Enum):
    show_ad = 0
    send_award = 1
    increase_difficulty = 2
    decrease_difficulty = 3
    goods_recommend = 4

class Engagements(Enum):
    online = 0
    mission_completed = 1
    mission_failed = 2
    level_up = 3

class Events(Enum):
    ad_closed = 0
    ad_opened = 1
    offline = 2
    mission_start = 3
    transaction = 4



class Robot(object):
    def __init__(self, name, online_motivation, ad_acceptance, mission_skill, consumption_ability, life_duration = 0):

        self.name = name
        self.life_duration = life_duration # the duration of the robot lifetime, 0 for infinity

        # ----- fixed attributes ------
        self.offline_time = 60 / 5 # single offline time 
        self.mission_time = 20 / 5 # single mission time
        self.rest_time = 5 / 5 # time between 2 missions
        self.transaction_amount = 1 # single transaction amount

        # ----- state attributes ------
        self.online_motivation = online_motivation
        self.ad_acceptance = ad_acceptance
        self.mission_skill = mission_skill
        self.consumption_ability = consumption_ability

        # ----- attributes based on state ------


        self.online_time = online_motivation / 5 # TODO / 5 to compress running time

        self.ad_open_probability = self.ad_acceptance

        self.mission_complete_probability = self.mission_skill

        self.transaction_interval = (100 - self.consumption_ability) / 5


        # ----- attributes change on progress -----
        self.last_online_time = 0
        self.last_offline_time = 0
        self.is_online = False
        self.is_in_mission = False
        self.current_mission_time = 0
        self.current_rest_time = self.rest_time
        self.time_before_transaction = self.transaction_interval


    def __repr__(self):
        return """Robot %s -
        [online_time : %s
        ad_open_probability : %s
        mission_complete_probability : %s
        transaction_interval : %s
        last_online_time : %s
        last_offline_time : %s
        is_online : %s
        is_in_mission : %s
        current_mission_time : %s
        current_rest_time : %s
        time_before_transaction : %s]

        """ % (self.name, self.online_time,\
        self.ad_open_probability,\
        self.mission_complete_probability,\
        self.transaction_interval,\
        self.last_online_time,\
        self.last_offline_time,\
        self.is_online,\
        self.is_in_mission,\
        self.current_mission_time,\
        self.current_rest_time,\
        self.time_before_transaction,)

    def start(self):
        current_time = time.time()
        self.send_engagement(Engagements.online)
        self.last_online_time = current_time
        self.is_online = True

        print_interval = 60
        current_run_time = 0

        while True:
            self.update()
            time.sleep(0.2) #TODO try 1 -> 0.2 to compress running time
            current_run_time += 1

            if current_run_time % print_interval == 0:
                print('current_run_time: ', current_run_time, '\n', self)

                # robot lifetime over
                if self.life_duration != 0 and current_run_time > self.life_duration:
                    return

    def update(self):
        current_time = time.time()
        if self.is_online:
            self.time_before_transaction -= 1
            #transaction
            if self.time_before_transaction <= 0:
                self.send_event(Events.transaction, self.transaction_amount)
                self.time_before_transaction = self.transaction_interval

            if self.is_in_mission:
                self.current_mission_time += 1
                # mission over
                if self.current_mission_time >= self.mission_time:
                    self.is_in_mission = False
                    self.current_mission_time = 0
                    if random.randint(0,100) > self.mission_complete_probability:
                        return self.send_engagement(Engagements.mission_failed)
                    return self.send_engagement(Engagements.mission_completed)
            else:
                self.current_rest_time += 1
                # mission start
                if self.current_rest_time >= self.rest_time:
                    self.current_rest_time = 0
                    self.is_in_mission = True
                    return self.send_event(Events.mission_start)

            # get offline
            if current_time - self.last_online_time >= self.online_time:
                self.is_online = False
                self.last_offline_time = current_time
                return self.send_event(Events.offline)


        elif current_time - self.last_offline_time > self.offline_time:
            # get online
            self.is_online = True
            self.last_online_time = current_time
            return self.send_engagement(Engagements.online)


    def handle_response(self, response):
        if response == Responses.show_ad.name:
            if random.randint(0,100) > self.ad_open_probability:
                self.online_time = decrease(self.online_time)
                self.send_event(Events.ad_closed)
            else:
                self.send_event(Events.ad_opened)

        elif response == Responses.send_award.name:
            self.online_time = increase(self.online_time)
            self.transaction_interval = increase(self.transaction_interval)

        elif response == Responses.increase_difficulty.name:
            self.mission_complete_probability = decrease(self.mission_complete_probability)
        elif response == Responses.decrease_difficulty.name:
            self.mission_complete_probability = increase(self.mission_complete_probability)
        elif response == Responses.goods_recommend.name:
            if random.randint(0,100) > (self.transaction_interval * 5):
                self.send_event(Events.transaction, self.transaction_amount)
                self.transaction_interval = decrease(self.transaction_interval)
            else:
                self.online_time = decrease(self.online_time)
                self.transaction_interval = increase(self.transaction_interval)


    def send_event(self, event, params = None):
        print(self.name, 'send event: ', event.name)
        addr = event_addr % (self.name, event.name)

        if params:
            addr = addr + "?params=" + str(params)
        requests.get(addr)


    def send_engagement(self, engagement):
        response = requests.get(engagement_addr % (self.name, engagement.name)).text
        print(self.name, 'send engagement: ', engagement.name, 'get response:', response)
        return self.handle_response(response)


def increase(val):
    val += 1
    if val > 100:
        return 100
    return val

def decrease(val):
    val -= 1
    if val < 10:
        return 10
    return val




        






