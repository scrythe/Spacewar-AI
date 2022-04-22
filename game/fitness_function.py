def get_movement_fitness(movement_to_player, total_movement, screen_width):
    movement_to_player_per_screen = movement_to_player / screen_width
    if total_movement < 1:
        total_movement = 1

    good_movement_ratio = movement_to_player / total_movement
    # reward ship with better movement
    good_movement_reward_percentage = good_movement_ratio ** 2
    movement_fitness = movement_to_player_per_screen * good_movement_reward_percentage
    fitness = movement_fitness * 8

    return fitness


def get_shot_accuracity(screen_width, bullet_shots):
    fitness = 0
    for shot_distance in bullet_shots:
        width_diffrence = screen_width - shot_distance
        # get exponentially worse (= less reward), the further away the hit is
        fitness += 0.8 * (width_diffrence / screen_width) ** 2.5
    return fitness * 4


def get_hit_accuracity_fitness(hits, shots):
    if shots < 1:
        shots = 1
    hit_rate = hits / shots
    # reward shooters with better hit rate, reward is exponential
    accuracity = hit_rate ** 1.5
    return accuracity


def get_hits_fitness(hits, accuracity):
    fitness = hits * accuracity
    fitness *= 4
    return fitness


def move_wrong_way(movement_away_player, screen_width):
    movement_away_player_per_screen = movement_away_player / screen_width
    if total_movement < 1:
        total_movement = 1

    good_movement_ratio = movement_away_player / total_movement
    # negative reward for going in wrong way
    movement_fitness = movement_away_player_per_screen
    fitness = movement_fitness * 8

    return fitness


def get_survive_time_fitness(frames):
    fitness = frames / 200
    return fitness


def fitness_function(movement_to_player, total_movement, screen_width, bullet_shots, hits, shots, frames):

    movement_fitness = get_movement_fitness(
        movement_to_player, total_movement, screen_width)

    shot_accuracity_fitness = get_shot_accuracity(
        screen_width, bullet_shots)

    hit_accuracity = get_hit_accuracity_fitness(hits, shots)
    get_hits_fitness

    hits_fitness = get_hits_fitness(hits, hit_accuracity)

    frames_fitness = get_survive_time_fitness(frames)

    fitness = 0
    fitness += movement_fitness * 0.05
    fitness += shot_accuracity_fitness
    fitness += hits_fitness
    fitness += frames_fitness

    return fitness


def test_fitness_function():
    # Check if good movement
    movement_good_tests = []
    for movement in range(100, 1280, 50):
        screen_width = 1280
        movement_to_player = movement * 0.8
        movement_fitness = get_movement_fitness(
            movement_to_player, movement, screen_width)
        movement_good_tests.append(movement_fitness)

    # Check if bad movement
    movement_bad_tests = []
    for movement in range(1280, 12800, 1280):
        screen_width = 1280
        movement_to_player = movement * 0.2
        movement_fitness = get_movement_fitness(
            movement_to_player, movement, screen_width)
        movement_bad_tests.append(movement_fitness)

    # Check for shot accuracity, on how close hit was
    shot_accuracity_tests = []
    for shot_accuracity in range(0, 1280, 50):
        shot_accuracity_fitness = get_shot_accuracity(
            1280, [shot_accuracity, shot_accuracity])
        shot_accuracity_tests.append(shot_accuracity_fitness)

    # Check hit accuracity, on how shots actually hit enemy
    hit_accuracity_test = []
    shots_default = 10
    for percentage in range(0, 110, 10):
        percentage /= 100
        hits = shots_default * percentage
        hit_accuracity = get_hit_accuracity_fitness(hits, shots_default)
        hit_accuracity_test.append(hit_accuracity)

    # Check for good hit accuracity
    good_hits_tests = []
    for shots in range(0, 200, 2):
        hits = shots * 0.8
        hit_accuracity = get_hit_accuracity_fitness(hits, shots)
        hits_fitness = get_hits_fitness(hits, hit_accuracity)
        good_hits_tests.append(hits_fitness)

    # Check for bad hit accuracity
    bad_hits_tests = []
    for shots in range(0, 20, 2):
        hits = shots * 0.2
        hit_accuracity = get_hit_accuracity_fitness(hits, shots)
        hits_fitness = get_hits_fitness(hits, hit_accuracity)
        bad_hits_tests.append(hits_fitness)

    # Check how long survived
    frames_survived_tests = []
    for frames in range(20, 800, 50):
        survived_time_fitness = get_survive_time_fitness(frames)
        frames_survived_tests.append(survived_time_fitness)

    print('breakpoint')


# test_fitness_function()
