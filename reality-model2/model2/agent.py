import random
from mind import Mind
from drawer import Drawer

min_dist = .05      #Minimum distance between agent and food for the food to be eaten.
goal_decay = 0.01   #How much score is lose in each iteration
iterations = 15#10000

class Agent:
    def __init__(self):
        self.mind = Mind(self)
        self.init_agent()

    def init_agent(self):
        self.drawer = Drawer(self)
        self.goal = 0
        self.goal_integral = 0
        self.foods_eaten = 0
        self.food_pos = [random.uniform(0, 1) for _ in range(2)]
        self.agent_pos = [random.uniform(0, 1) for _ in range(2)]
        self.agent_vel = [random.uniform(0, 1) for _ in range(2)]

    def live(self, generation):
        for i in range(iterations):
            self.mind.one_iteration(generation)

        return self.goal_integral

    def percept(self):
        distance_to_food = [(self.food_pos[i] - self.agent_pos[i]) for i in range(2)]
        self.goal = (self.agent_pos[0] - self.agent_pos[1]) / 2 #sum([pos for pos in self.agent_pos]) / 2
        #return [self.goal] + distance_to_food + self.agent_vel
        return [self.goal] + self.agent_vel

    def update_sensors(self):
        #self.goal -= goal_decay if self.goal == 0 else 0
        self.goal_integral += self.goal
        for i in range(2):
            self.agent_pos[i] += self.agent_vel[i] / 20
            if not (0 < self.agent_pos[i] < 1):
                self.agent_pos[i] = int(self.agent_pos[i])#.5 + random.uniform(-.1, .1)#

        '''
        if all([abs(a - f) < min_dist for a, f in zip(self.agent_pos, self.food_pos)]):
            self.goal += 1
            self.foods_eaten += 1
            self.food_pos = [random.uniform(0, 1) for _ in range(2)]
        '''
