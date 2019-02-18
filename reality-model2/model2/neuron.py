import time

class Neuron:
    def __init__(self, agent, type):
        self.agent = agent
        self.type = type

        self.input_neurons = []
        self.output = 0
        self.water = {'pos': 0, 'neg': 0}

    def remove_water(self):
        self.water = {'pos': 0, 'neg': 0}
        if self in self.agent.watery_neurons:
            self.agent.watery_neurons.remove(self)

    def receive_water(self, added_water):
        self.water['pos'] += added_water[0]
        self.water['neg'] += added_water[1]
        if self.type != 'actuator':
            if self not in self.agent.watery_neurons: # Make wns a set
                self.agent.watery_neurons.append(self)

    def transfer_water(self, next_neuron):
        next_neuron.receive_water(self.water)
        self.remove_water()

    def connected_from(self, neuron):
        for input_neuron, _ in self.input_neurons:
            if neuron == input_neuron: return True
        return False

    def potential(self, neuron, weight, type):
        return abs(weight)
        '''
        print ('connection', self.type, neuron.type, weight, type)
        if (weight > 0 and type == 'pos') or (weight <= 0 and type == 'neg'):
            return weight#(1 - neuron.output) * weight
        elif (weight <= 0 and type == 'pos') or (weight > 0 and type == 'neg'):
            return -1 * weight#(0 - neuron.output) * weight
        '''

    def distribute_water(self):
        #print (len(self.agent.watery_neurons))
        neuron_water = self.water
        self.remove_water()

        for water_type in ['pos', 'neg']:
            total_potential = sum([self.potential(n, w, water_type) for n, w in self.input_neurons])
            if neuron_water[water_type] != 0 and total_potential != 0:
                for neuron, weight in self.input_neurons:
                    potential = self.potential(neuron, weight, water_type)
                    relative_potential = potential / total_potential
                    water = neuron_water[water_type] * relative_potential

                    if (weight > 0 and water_type == 'pos') or (weight <= 0 and water_type == 'neg'):
                        neuron.receive_water([water, 0])
                    else:
                        neuron.receive_water([0, water])
