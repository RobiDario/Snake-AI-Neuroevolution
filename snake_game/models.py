from jinja2.compiler import generate

from snake_game.brain import NeuralNetwork
from config import START_HUNGER,GRID_SIZE
import random

class Snake:
    def __init__(self,start_x,start_y):
        self.bodyParts=[[start_x,start_y],[start_x-1,start_y],[start_x-2,start_y]]

        self.direction=[1,0]

        self.is_alive=True
        self.score=0

        self.lifetime=0
        self.hunger=START_HUNGER

        self.brain= NeuralNetwork()

        self.food = self.generate_food()
        self.fitness = 0
        pass

    def calculate_fitness(self):

        self.fitness = (self.score ** 2) * 1000 + self.lifetime * 0.5
        if self.score == 0 and self.lifetime > 50:
            self.fitness *= 0.5

    def generate_food(self):
        all_positions = []
        for x in range(GRID_SIZE):
            for y in range(GRID_SIZE):
                all_positions.append([x, y])

        body_set = [list(p) for p in self.bodyParts]
        free_positions = [pos for pos in all_positions if pos not in body_set]

        if not free_positions:
            return None

        return random.choice(free_positions)

    def move(self):
        if not self.is_alive: return

        new_head = [self.bodyParts[0][0] + self.direction[0], self.bodyParts[0][1] + self.direction[1]]

        if new_head == self.food:
            self.score += 1
            self.hunger = START_HUNGER
            self.bodyParts.insert(0, new_head)
            self.food = self.generate_food()
        else:
            self.bodyParts.insert(0, new_head)
            self.bodyParts.pop()
            self.hunger -= 1

        self.lifetime += 1
        self.check_if_dead()

    def check_if_dead(self):

        if self.check_colision() or self.is_starving():
            self.is_alive=False

    def check_colision(self):

        head=self.bodyParts[0]
        if head[0]<0 or head[0]>=GRID_SIZE or head[1]<0 or head[1]>=GRID_SIZE:
            return True

        if head in self.bodyParts[1:]:
           return True

        return False

    def is_starving(self):
        return self.hunger <= 0

    def get_vision(self):
        vision = []
        directions = [[0, -1], [1, -1], [1, 0], [1, 1], [0, 1], [-1, 1], [-1, 0], [-1, -1]]

        body_set = {tuple(p) for p in self.bodyParts[1:]}
        food_pos = tuple(self.food)
        head_pos = self.bodyParts[0]

        for dx, dy in directions:
            radar_x, radar_y = head_pos
            distance = 0
            dist_food = 0
            dist_body = 0

            while True:
                radar_x += dx
                radar_y += dy
                distance += 1

                if radar_x < 0 or radar_x >= GRID_SIZE or radar_y < 0 or radar_y >= GRID_SIZE:
                    break

                if (radar_x, radar_y) == food_pos and dist_food == 0:
                    dist_food = distance
                if (radar_x, radar_y) in body_set and dist_body == 0:
                    dist_body = distance

            vision.append(1.0 / distance)
            vision.append(1.0 / dist_food if dist_food != 0 else 0)
            vision.append(1.0 / dist_body if dist_body != 0 else 0)

        return vision




