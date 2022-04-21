def get_shot_accuracity(screen_width, bullet_shots):
    fitness = 0
    for shot_distance in bullet_shots:
        width_diffrence = screen_width - shot_distance
        # get exponentially worse (= less reward), the further away the hit is
        fitness += 0.4 * (width_diffrence / screen_width) ** 2
    return fitness


def get_hit_accuracity_fitness(hits, shots):
    if shots < 1:
        shots = 1
    hit_rate = hits / shots
    # reward shooters with better hit rate, reward is exponential
    fitness = hit_rate ** 2
    return fitness


def get_hits_fitness(hits, accuracity):
    fitness = hits * accuracity
    fitness *= 2
    return fitness


def fitness_function(screen_width, bullet_shots, hits, shots):

    shot_accuracity_fitness = get_shot_accuracity(
        screen_width, bullet_shots)

    hit_accuracity = get_hit_accuracity_fitness(hits, shots)
    get_hits_fitness

    hits_fitness = get_hits_fitness(hits, hit_accuracity)

    fitness = 0
    fitness += shot_accuracity_fitness
    fitness += hits_fitness

    return fitness


def test_fitness_function():
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
    for shots in range(0, 20, 2):
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

    print('breakpoint')


# test_fitness_function()
