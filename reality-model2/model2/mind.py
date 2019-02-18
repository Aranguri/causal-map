import math
import time
import random
from abegama import Abegama
from neuron import Neuron

water_passes = 8
processors_amount = 8
connection_density = 1

class Mind:
    def __init__(self, agent):
        self.agent = agent
        self.abegama = Abegama(self)
        self.initial_weight = 0.1
        self.watery_neurons = [] #Neurons with water
        #self.neuron_types = ['goal'] + ['sensor'] * 2 + ['actuator'] * 2 + ['processor'] * processors_amount
        self.neuron_types = ['goal'] + ['actuator'] * 2
        self.neurons = [Neuron(self, type) for type in self.neuron_types]

        for neuron in self.get_neurons(['goal', 'sensor', 'processor']):
            for other_neuron in self.neurons:
                if random.uniform(0, 1) < connection_density:
                    weight = random.uniform(-self.initial_weight, self.initial_weight)
                    neuron.input_neurons.append([other_neuron, weight])

    def one_iteration(self, generation):
        percept = self.agent.percept()
        self.predict(percept)
        self.init_water()

        for i in range(water_passes):
            if generation % 30 == 29:
                self.agent.drawer.draw()
                time.sleep(.03)
            watery_neurons = [wn for wn in self.watery_neurons] # We make a copy of wns on purpose
            for neuron in watery_neurons:
                #print (1)
                neuron.distribute_water()

        for i, act in enumerate(self.get_neurons('actuator')):
            self.agent.agent_vel[i] = 1 if act.water['pos'] > act.water['neg'] else -1

        self.agent.update_sensors()
        if generation % 30 == 29:
            self.agent.drawer.draw()
            time.sleep(.03)
        self.abegama.learn()

    def get_neurons(self, type):
        return filter(lambda n: n.type in type, self.neurons)

    def predict(self, percept):
        for i, neuron in enumerate(self.get_neurons(['goal', 'sensor', 'actuator'])):
            neuron.old_output = neuron.output
            neuron.output = percept[i]

        for neuron in self.neurons:
            weighted_sum = sum([n.output * w for n, w in neuron.input_neurons])
            neuron.next_output = self.sigmoid(weighted_sum)

        for neuron in self.neurons:
            neuron.old_output = neuron.output
            neuron.output = neuron.next_output

    def init_water(self):
        for neuron in self.neurons:
            neuron.remove_water()
        self.watery_neurons = []
        goal_neuron = list(self.get_neurons('goal'))[0]
        goal_neuron.receive_water([0, 1])

    def reset_mind(self):
        for neuron in self.neurons:
            neuron.old_output, neuron.output, neuron.next_output = [0] * 3
            weight = random.uniform(-self.initial_weight, self.initial_weight)
            neuron.input_neurons = [[n, weight] for n, w in neuron.input_neurons]

    @staticmethod
    def sigmoid(x):
        return 1 / (1 + math.exp(-x))
