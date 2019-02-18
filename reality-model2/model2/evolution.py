from agent import Agent
from heapq import heappush
import copy
import random
import itertools

agents_amount = 20
conn_variance = .1
total_conn_amount = 143
min_weight = -1.5#0.01
max_weight = 1.5

class Evolution:
    def __init__(self):
        self.agents = [Agent() for _ in range(agents_amount)]

    def main(self):
        for i in itertools.count():
            scoreboard = []

            for j in range(len(self.agents)):
                fitness = self.agents[j].live(i)
                scoreboard.append((fitness, j))

            scoreboard = sorted(scoreboard)
            print ('Generation {}'.format(i))
            print (scoreboard)

            for fitness, j in scoreboard[int(agents_amount / 2):]:
                self.agents[j].drawer = None
                new_agent = copy.deepcopy(self.agents[j])
                self.mutate(new_agent)
                self.agents.append(new_agent)

            #print ('Fitness avg {}'.format(total_fitness / agents_amount))
            #print ('Total fitness avg {}'.format(total_total_fitness / (i + 0.000001)))

            for _, j in scoreboard[:int(agents_amount / 2)]:
                del self.agents[j]

            for agent in self.agents:
                agent.init_agent()
                agent.mind.reset_mind()

    def mutate(self, agent):
        mind = agent.mind
        mind.initial_weight += random.uniform(0, .2)
        if not (min_weight < mind.initial_weight < max_weight):
            mind.initial_weight = min_weight if mind.initial_weight < min_weight else max_weight
        for i in range(len(agent.mind.abegama.params)):
            mind.abegama.params[i] += random.uniform(-.1, .1)

        conn_amount = sum([len(n.input_neurons) for n in mind.neurons])

        for i in range(len(mind.neurons)):
            saved_connections = []
            for j in range(len(mind.neurons[i].input_neurons)):
                if random.uniform(0, 1) > conn_variance:
                    saved_connections.append(mind.neurons[i].input_neurons[j])
            mind.neurons[i].input_neurons = saved_connections

        '''
        new_conn_variance = conn_variance * conn_amount / (total_conn_amount - conn_amount)
        new_conn_variance += random.uniform(-0.03, 0.03)

        for neuron in mind.neurons:
            for other_neuron in mind.get_neurons(['goal', 'sensor', 'processor']):
                if not neuron.connected_from(other_neuron):
                    if random.uniform(0, 1) < new_conn_variance:
                        neuron.input_neurons.append([other_neuron, agent.mind.initial_weight])
        '''

Evolution().main()


'''
from agent import Agent
a = Agent()
import copy
b = copy.deepcopy(a)
'''
