from time import time


def get_movement_fitness(frames, movement_to_player, movement_away_player):
    # less rewarding the more go
    movement_to_per_s = movement_to_player / frames
    movement_to_reward = 6 * (movement_to_per_s ** 0.2)

    # first slow but gets more exponential
    movement_away_per_s = movement_away_player / frames
    movement_away_reward = 0.1 * (movement_away_per_s ** 2.5)

    # reward movers, but prefer those who don't go too much to other direction
    fitness = (movement_to_reward -
               movement_away_reward) + movement_away_per_s / 4

    return fitness


def get_shot_accuracity_fitness(screen_width, bullet_shots):
    fitness = 0
    for shot_distance in bullet_shots:
        width_diffrence = screen_width - shot_distance
        # get exponentially worse, the further away the hit is
        fitness += 0.8 * (width_diffrence / screen_width) ** 2
    return fitness


def get_shots_hits_fitness(hits, shots):
    hits_reward = 5 * (hits ** 1.5)
    miss_shots_reward = 0.6 * (shots ** 1.6)

    # reward shooters, but too many miss shots are bad
    fitness = hits_reward - miss_shots_reward

    return fitness


def get_survived_time_fitness(start_time):
    time_survived = time() - start_time
    fitness = time_survived * 0.5
    return fitness


def fitness_function(frames, movement_to_player, movement_away_player, screen_width, bullet_shots, hits, shots, start_time):
    movement_fitness = get_movement_fitness(
        frames, movement_to_player, movement_away_player)

    shot_accuracity_fitness = get_shot_accuracity_fitness(
        screen_width, bullet_shots)

    shots_hits_fitness = get_shots_hits_fitness(hits, shots)

    survived_time_fitness = get_survived_time_fitness(start_time)

    fitness = 0
    fitness += movement_fitness
    fitness += shot_accuracity_fitness
    fitness += shots_hits_fitness
    fitness += survived_time_fitness

    return fitness


def test_fitness_function():
    frames = 60

    # movement_to_player_tests = []
    # for movement_to_player in range(0, 600, 30):
    #     movement_to_player_tests.append(fitness_function(
    #         frames, movement_to_player, 0, lambda: 0, 0, 0))

    # movement_away_player_tests = []
    # for movement_away_player in range(0, 600, 30):
    #     movement_away_player_tests.append(fitness_function(
    #         frames, 0, movement_away_player, lambda: 0, 0, 0))

    # Check if good movement
    movement_good_tests = []
    for movement in range(0, 600, 30):
        movement_to_player = movement * 0.8
        movement_away_player = movement * 0.2
        movement_fitness = get_movement_fitness(
            frames, movement_to_player, movement_away_player)
        movement_good_tests.append(movement_fitness)

    # Check if bad movement
    movement_bad_tests = []
    for movement in range(0, 600, 30):
        movement_to_player = movement * 0.2
        movement_away_player = movement * 0.8
        movement_fitness = get_movement_fitness(
            frames, movement_to_player, movement_away_player)
        movement_bad_tests.append(movement_fitness)

    # Check for shot accuracity
    shot_accuracity_tests = []
    for shot_accuracity in range(0, 1280, 50):
        shot_accuracity_fitness = get_shot_accuracity_fitness(
            1280, [shot_accuracity, shot_accuracity])
        shot_accuracity_tests.append(shot_accuracity_fitness)

    # Check if good shots
    shots_hits_good_tests = []
    for shots in range(0, 20):
        hits = round(shots*0.8)
        shots_hits_fitness = get_shots_hits_fitness(hits, shots)
        shots_hits_good_tests.append(shots_hits_fitness)

    # Check if bad shots
    shots_hits_bad_tests = []
    for shots in range(0, 20):
        hits = round(shots * 0.2)
        shots_hits_fitness = get_shots_hits_fitness(hits, shots)
        shots_hits_bad_tests.append(shots_hits_fitness)

    # Check if very good shots
    shots_hits_very_good_tests = []
    for shots in range(0, 120):
        hits = round(shots*0.95)
        shots_hits_fitness = get_shots_hits_fitness(hits, shots)
        shots_hits_very_good_tests.append(shots_hits_fitness)

    # print(shots_hits_good_tests)
    print(shots_hits_bad_tests)
    # print(shots_hits_very_good_tests)


# test_fitness_function()
