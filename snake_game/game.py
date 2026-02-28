import pygame
import sys
from models import Snake
from evolution import EvolutionManager
from config import *
import random

pygame.init()
screen=pygame.display.set_mode((GRID_SIZE*CELL_SIZE, GRID_SIZE*CELL_SIZE))
clock=pygame.time.Clock()

def run_simulation():



    genetic_algorithm=EvolutionManager()
    old_champion = genetic_algorithm.load_champion()

    population = [Snake(GRID_SIZE // 2, GRID_SIZE // 2) for _ in range(100)]
    if old_champion:
        population[0].brain = old_champion
        print("The old champion was load into the game!")

    generation_count=0
    test_mode=False
    fast_mode=False

    while True:
        while any(s.is_alive for s in population):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_f:
                        fast_mode = not fast_mode
                        print(f"--- Fast Mode: {fast_mode} ---")

                    if event.key == pygame.K_t:
                        test_mode = not test_mode
                        print(f"--- Champion Only Mode: {test_mode} ---")

                    if event.key == pygame.K_s:
                        best = max(population, key=lambda s: s.score)
                        genetic_algorithm.save_champion(best.brain)
                        print("Saved current best brain!")

            for snake in population:
                if snake.is_alive:
                    vision = snake.get_vision()
                    move_idx = snake.brain.feed_forward(vision)
                    directions = [[0, -1], [0, 1], [-1, 0], [1, 0]]
                    snake.direction = directions[move_idx]
                    snake.move()

            if not fast_mode:
                screen.fill((20, 20, 20))

                for i, snake in enumerate(population):
                    if snake.is_alive:
                        if test_mode and i != 0:
                            continue

                        pygame.draw.rect(screen, (255, 0, 0), (
                            snake.food[0] * CELL_SIZE,
                            snake.food[1] * CELL_SIZE,
                            CELL_SIZE - 1, CELL_SIZE - 1
                        ))

                        color = (0, 191, 255) if i == 0 else (0, 255, 0)
                        for part in snake.bodyParts:
                            pygame.draw.rect(screen, color, (
                                part[0] * CELL_SIZE,
                                part[1] * CELL_SIZE,
                                CELL_SIZE - 1, CELL_SIZE - 1
                            ))

                pygame.display.flip()
                if test_mode:
                    clock.tick(20)

        generation_count += 1

        new_brains = genetic_algorithm.evolve(population)
        genetic_algorithm.update_live_plot()


        population = []
        for brain in new_brains:
            s = Snake(GRID_SIZE // 2, GRID_SIZE // 2)
            s.brain = brain
            population.append(s)

        print(f"Gen: {generation_count} | Record Fitness: {int(genetic_algorithm.best_fitness_ever)}")

if __name__ == '__main__':
    run_simulation()
