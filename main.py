from helper_functions import *


if __name__ == '__main__':
    write_to_file(file)
    config_path = os.path.join(os.path.dirname(__file__), 'config-feedforward.txt')
    run(config_path)