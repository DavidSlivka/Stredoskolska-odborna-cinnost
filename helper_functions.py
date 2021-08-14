from settings import *
from Bird import Bird
from Pipe import Pipe
from Base import Base
from collections import Counter


def write_to_file(file_name):
    with open(file_name, 'w', newline='') as f:
        writer = csv.writer(f, dialect='excel')
        writer.writerow(["Generation", "Score"])


def append_to_file(file_name, gen, score):
    with open(file_name, 'a', newline='') as f:
        writer = csv.writer(f, dialect='excel')
        writer.writerow([gen, score])


def plot(file_name):
    plt.style.use('ggplot')
    data = pd.read_csv(file_name)
    gens = data['Generation']
    score = data['Score']

    points_count = Counter()
    for g, s in zip(gens, score):
        points_count[(g, s)] += 1

    for coords, size in points_count.items():
        plt.scatter(*coords, s=size * 10, alpha=0.75, linewidths=1, edgecolors='black')

    c_bar = plt.colorbar()
    c_bar.set_label('Score')

    plt.title('NEAT in Flappy Bird')
    plt.xlabel('Generation')
    plt.ylabel('Score')

    plt.show()


def draw_screen(screen, birds, pipes, base, score, gen):
    screen.blit(BG_IMG, (0, 0))
    for pipe in pipes:
        pipe.draw()

    for bird in birds:
        bird.draw()

    score_text = FONT.render('Score: ' + str(score), 1, (255, 255, 255))
    screen.blit(score_text, (WIDTH - 10 - score_text.get_width(), 10))

    gen_text = FONT.render('Gen: ' + str(gen), 1, (255, 255, 255))
    screen.blit(gen_text, (WIDTH - 10 - gen_text.get_width(), 40))

    birds_alive_text = FONT.render('Alive: ' + str(len(birds)), 1, (255, 255, 255))
    screen.blit(birds_alive_text, (WIDTH - 10 - birds_alive_text.get_width(), 70))
    base.draw()

    pygame.display.update()


def collision(bird, pipe):
    bird_mask = bird.get_mask()
    top_pipe_mask = pipe.get_top_mask()
    bottom_pipe_mask = pipe.get_bottom_mask()

    top_shift = (pipe.x - bird.x, pipe.top - round(bird.y))
    bottom_shift = (pipe.x - bird.x, pipe.bottom - round(bird.y))

    bottom_collision = bird_mask.overlap(bottom_pipe_mask, bottom_shift)
    top_collision = bird_mask.overlap(top_pipe_mask, top_shift)

    if top_collision or bottom_collision:
        return True

    return False


def remove_from_generation(nets, ge, birds, bird_index):
    nets.pop(birds.index(bird_index))
    ge.pop(birds.index(bird_index))
    birds.pop(birds.index(bird_index))


def main(genomes, config):
    global generation, pipe
    generation += 1

    nets = []
    gen = []
    birds = []
    base = Base(GROUND)
    pipes = [Pipe(WIDTH+30)]

    score = 0

    for genome_id, genome in genomes:
        genome.fitness = 0
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        birds.append(Bird())
        gen.append(genome)

    running = True
    while running:
        pygame.time.delay(30)
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                for bird in birds:
                    append_to_file(file, generation, score)
                    nets.pop(birds.index(bird))
                    gen.pop(birds.index(bird))
                    birds.pop(birds.index(bird))

                running = False
                pygame.quit()
                plot(file)
                quit()
                break

        pipe_index = 0
        if len(birds) > 0:
            if len(pipes) > 1 and birds[0].x > pipes[0].TOP_PIPE.get_width():
                pipe_index = 1
        else:
            break

        remove_pipes = []

        for pipe in pipes:
            pipe.move()
            if pipe.x + pipe.TOP_PIPE.get_width() < 0:
                remove_pipes.append(pipe)

        for bird in birds:
            gen[birds.index(bird)].fitness += 0.2
            bird.move()
            output = nets[birds.index(bird)].activate((abs(bird.y - pipes[pipe_index].height),
                                                       abs(bird.y - pipes[pipe_index].bottom),
                                                       abs(pipes[pipe_index].x - bird.x)))
            # refer to tanh function
            if output[0] > 0:
                bird.jump()

            if collision(bird, pipe) or bird.y + bird.img.get_height() >= GROUND or bird.y < 0:
                gen[birds.index(bird)].fitness -= 1
                append_to_file(file, generation, score)
                remove_from_generation(nets, gen, birds, bird)

            if score == 100:
                append_to_file(file, generation, score)
                remove_from_generation(nets, gen, birds, bird)

            if not pipe.passed and bird.x > pipe.x+pipes[0].TOP_PIPE.get_width():
                pipe.passed = True

                score += 1
                for genome in gen:
                    genome.fitness += 5
                pipes.append(Pipe(WIDTH))

                if len(birds) == 0:
                    running = False
                    pygame.quit()
                    plot(file)
                    quit()

        for pipe in remove_pipes:
            pipes.remove(pipe)

        base.move()
        draw_screen(screen, birds, pipes, base, score, generation)


def run(config_path):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                neat.DefaultSpeciesSet, neat.DefaultStagnation,
                                config_path)

    pop = neat.Population(config)
    pop.add_reporter(neat.StdOutReporter(True))
    pop.add_reporter(neat.StatisticsReporter())
    print(pop)

    winner = pop.run(main, 100)
    print('\nBest genome:\n{!s}'.format(winner))
    plot(file)
