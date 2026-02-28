import random
import numpy as np
from config import MUTATION_RATE, ELITISM_COUNT,TOURNAMENT_SIZE
from snake_game.brain import NeuralNetwork

import pickle
import os
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt






class EvolutionManager:

    def __init__(self):
        self.mutation_rate = MUTATION_RATE
        self.elitism_count = ELITISM_COUNT
        self.best_snake_ever = None
        self.best_fitness_ever = 0
        self.filename = "best_snake_brain.pkl"
        self.fitness_history = []

        plt.ion()
        self.fig, self.ax = plt.subplots(figsize=(5, 4))
        self.line, = self.ax.plot([], [], 'r-', label='Best Fitness')
        self.ax.set_title("Evoluție Fitness")
        self.ax.set_xlabel("Generație")
        self.ax.set_ylabel("Scor")
        self.ax.legend()
        plt.show(block=False)

    def save_champion(self, brain):
        with open(self.filename, 'wb') as f:
            pickle.dump(brain, f)
        print(f"--- New Record! Brain saved in {self.filename} ---")

    def load_champion(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'rb') as f:
                return pickle.load(f)
        return None

    def crossover_matrices(self, m1, m2):
        mask = np.random.rand(*m1.shape) > 0.5
        return np.where(mask, m1, m2)

    def crossover(self, parent1_brain, parent2_brain):
        child_brain = NeuralNetwork()

        child_brain.weights_input_hidden = self.crossover_matrices(parent1_brain.weights_input_hidden,
                                                                       parent2_brain.weights_input_hidden)
        child_brain.weights_hidden_output = self.crossover_matrices(parent1_brain.weights_hidden_output,
                                                                        parent2_brain.weights_hidden_output)
        child_brain.bias_hidden = self.crossover_matrices(parent1_brain.bias_hidden, parent2_brain.bias_hidden)
        child_brain.bias_output = self.crossover_matrices(parent1_brain.bias_output, parent2_brain.bias_output)
        return child_brain

    def mutate_matrix(self, matrix):
        m = matrix.copy()

        mask = np.random.rand(*m.shape) < self.mutation_rate

        noise = np.random.normal(0, 0.1, m.shape)
        m[mask] += noise[mask]

        return np.clip(m, -1, 1)

    def mutate(self, child_brain):

        child_brain.weights_input_hidden = self.mutate_matrix(child_brain.weights_input_hidden)
        child_brain.weights_hidden_output = self.mutate_matrix(child_brain.weights_hidden_output)
        child_brain.bias_hidden = self.mutate_matrix(child_brain.bias_hidden)
        child_brain.bias_output = self.mutate_matrix(child_brain.bias_output)

        return child_brain

    def breed(self, parent1_brain, parent2_brain):

        child_brain = self.crossover(parent1_brain, parent2_brain)
        child_brain = self.mutate(child_brain)

        return child_brain

    def selection(self, population):

        tournament_size = TOURNAMENT_SIZE

        candidates = random.sample(population, tournament_size)


        candidates.sort(key=lambda snake: snake.fitness, reverse=True)

        return candidates[0].brain

    def evolve(self, population):
        for s in population: s.calculate_fitness()
        population.sort(key=lambda s: s.fitness, reverse=True)

        best_fitness = population[0].fitness
        self.fitness_history.append(best_fitness)

        if best_fitness > self.best_fitness_ever:
            self.best_fitness_ever = best_fitness
            self.save_champion(population[0].brain)

        new_brains = [population[i].brain for i in range(self.elitism_count)]

        while len(new_brains) < len(population):
            p1 = self.selection(population)
            p2 = self.selection(population)
            child = self.mutate(self.crossover(p1, p2))
            new_brains.append(child)

        return new_brains

    def update_live_plot(self):
        if not self.fitness_history:
            return


        if not plt.fignum_exists(self.fig.number):
            return

        try:
            xdata = list(range(len(self.fitness_history)))
            ydata = self.fitness_history


            self.line.set_data(xdata, ydata)


            self.ax.relim()
            self.ax.autoscale_view()


            self.fig.canvas.draw()
            self.fig.canvas.flush_events()


            plt.pause(0.01)
        except Exception as e:
            print(f"Eroare Plot: {e}")