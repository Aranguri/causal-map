import random

min_weight = -1.5#0.01
max_weight = 1.5

class Abegama:
    def __init__(self, agent):
        self.agent = agent
        self.params = [random.uniform(-1, 1) for _ in range(4)]

    def learn(self):
        print ('abegama', self.params)
        for neuron in self.agent.neurons:
            for i, connection in enumerate(neuron.input_neurons):
                other_neuron, weight = connection
                weight += self.get_change(neuron.output, other_neuron.old_output, weight)
                if not (min_weight < weight < max_weight):
                    weight = min_weight if weight < min_weight else max_weight
                neuron.input_neurons[i] = [other_neuron, weight]

    def get_change(self, x, y, weight):
        vars = [x, y, weight, 1]
        return sum([param * var for param, var in zip(vars, self.params)])
