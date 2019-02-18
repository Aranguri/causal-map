import pygame
import itertools
import time
import random

WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
PURPLE = (255, 0, 255)
BLACK = (0, 0, 0)

class Drawer:
    def __init__(self, agent):
        self.agent = agent
        self.width = 1200
        self.height = 700
        self.screen = pygame.display.set_mode((self.width, self.height))

    def handle_click(self):
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP:
                self.agent.food_pos = pygame.mouse.get_pos()

    def draw_structure(self):
        self.screen.fill(BLACK)
        pygame.draw.line(self.screen, WHITE, (self.width / 2, 0), (self.width / 2, self.height), 3)
        pygame.draw.line(self.screen, WHITE, (self.width / 4, 0), (self.width / 4, self.height), 1)
        pygame.draw.line(self.screen, WHITE, (0, self.height / 2), (self.width / 2, self.height / 2), 1)

    def draw_flatland(self):
        agent_pos = self.agent.agent_pos
        food_pos = self.agent.food_pos

        agent_pos = (int(agent_pos[0] * self.width / 2), int(agent_pos[1] * self.height))
        food_pos = (int(food_pos[0] * self.width / 2), int(food_pos[1] * self.height))

        pygame.draw.circle(self.screen, WHITE, agent_pos, 5)
        pygame.draw.circle(self.screen, GREEN, food_pos, 3)

    def draw_mind(self):
        neurons = self.agent.mind.neurons
        width_size = 10
        height_size = 10

        #Calculate neuron pos
        if not hasattr(neurons[0], 'map_pos'):
            for i, neuron in enumerate(neurons):
                width = (1 + i % width_size / (width_size)) * self.width / 1.8
                height = 50 + int(i / 3) / (height_size - 1) * self.height * 0.8
                neuron.map_pos = [int(width), int(height)]

        #Draw mind connections
        for neuron in neurons:
            for input_neuron, weight in neuron.input_neurons:
                color = GREEN if weight > 0 else RED
                size = 1 if 0 < abs(weight) < 1/10 else int(10 * abs(weight))
                input = [pos + 30 for pos in input_neuron.map_pos]
                pygame.draw.line(self.screen, color, input, neuron.map_pos, size)

        #Draw neurons and water
        for neuron in neurons:
            (width, height) = neuron.map_pos

            pos_water = int(neuron.water['pos'] * 50)
            neg_water = int(abs(neuron.water['neg']) * 50)
            pygame.draw.rect(self.screen, WHITE, neuron.map_pos + [30, 30])
            pygame.draw.circle(self.screen, PURPLE, (width - 10, height + 20), pos_water)
            pygame.draw.circle(self.screen, BLUE, (width + 10, height + 20), neg_water)

    def draw(self):
        self.handle_click()
        self.draw_structure()
        self.draw_flatland()
        self.draw_mind()
        pygame.display.flip()
