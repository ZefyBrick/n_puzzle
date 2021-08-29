from validation import puzzle_validate
from heapq import heappush as insert, heappop as extract_minimum
from time import time
import parse
from subprocess import call
from graph import graph
import ctypes
if hasattr(ctypes, 'windll'):
    kernel32 = ctypes.windll.kernel32
    kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)


def move_zero(coord, x, y, digit_to_move=0):
    # Создание новой карты, путём передижения 0
    map = (zip(x, y))
    for i, j in enumerate(map):
        if j == coord:
            digit_to_move = i
            break
    x[digit_to_move], y[digit_to_move] = x[0], y[0]
    x[0], y[0] = coord[0], coord[1]
    return (tuple(x), tuple(y)), digit_to_move


def get_true_coordinates(size):
    max_index = size - 1

    def true_coordinates(x, y):
        # Проссматриваются все варианты, куда можно передвинуть 0
        coordinates = []
        if x[0] != 0:
            coordinates.append((x[0] - 1, y[0]))
        if x[0] != max_index:
            coordinates.append((x[0] + 1, y[0]))
        if y[0] != 0:
            coordinates.append((x[0], y[0] - 1))
        if y[0] != max_index:
            coordinates.append((x[0], y[0] + 1))
        return coordinates
    return true_coordinates


def get_hamming():
    # Эвристика Хэмминга
    # Подсчёт количества пятнашек, которые стоят не на своём месте
    def hamming(x, y, perfect_x, perfect_y):
        dist = 0
        for i, j, k, l in zip(x, perfect_x, y, perfect_y):
            if i != j or k != l:
                dist += 1
        return dist
    return hamming


def get_linear_conflict(x):
    size = int(len(x) ** 0.5)

    def linear_conflict(x, y, perfect_x, perfect_y):
        # Эвристика линейного конфликта
        # Пятнашки стоят в своём столбце/строке, но в неверном порядке
        dist = 0
        for i, j, k, l in zip(x, perfect_x, y, perfect_y):
            dist += abs(i - j) + abs(k - l)
        for i in range(size):
            line = [j for j, k in enumerate(x) if k == i and perfect_x[j] == i]
            if len(line) > 1:
                for p in range(len(line) - 1):
                    for key in line[p + 1:]:
                        if (perfect_y[line[p]] < perfect_y[key] and
                            y[line[p]] > y[key])\
                            or (perfect_y[line[p]] > perfect_y[key] and
                                y[line[p]] < y[key]):
                            dist += 2
        for i in range(size):
            line = [j for j, k in enumerate(y) if k == i and perfect_y[j] == i]
            if len(line) > 1:
                for p in range(len(line) - 1):
                    for key in line[p + 1:]:
                        if (perfect_x[line[p]] < perfect_x[key] and
                            x[line[p]] > x[key])\
                            or (perfect_x[line[p]] > perfect_x[key] and
                                x[line[p]] < x[key]):
                            dist += 2
        return dist
    return linear_conflict


def get_manhattan():

    def manhattan(x, y, perfect_x, perfect_y):
        # Манхэттенское расстояние
        dist = 0
        for i, j, k, l in zip(x, perfect_x, y, perfect_y):
            dist += abs(i - j) + abs(k - l)
        return dist
    return manhattan


def get_corner_tiles(x):
    size = int(len(x) ** 0.5) - 1

    def corner_tiles(x, y, perfect_x, perfect_y):
        # Эвристика угловых клеток
        # В углу стоит неверная пятнашка, а соседняя верная
        dist = 0
        for i, j, k, l in zip(x, perfect_x, y, perfect_y):
            dist += abs(i - j) + abs(k - l)
        dop_dist = 0
        corners, index = [], 0
        for i, j in zip(perfect_x, perfect_y):
            if i in (0, size) and j in (0, size):
                corners.append([index, i, j])
        for corner in corners:
            if x[corner[0]] != corner[1] or y[corner[0]] != corner[2]:
                if corner[1] == 0 and corner[2] == 0:
                    index = 0
                    for i, j in zip(perfect_x, perfect_y):
                        if (i == 1 and j == 0) or (i == 0 and j == 1):
                            if x[index] == i and y[index] == j:
                                dop_dist += 2
                        index += 1
                elif corner[1] == size and corner[2] == size:
                    index = 0
                    for i, j in zip(perfect_x, perfect_y):
                        if (i == size and j == size - 1) or (i == size - 1 and
                                                             j == size):
                            if x[index] == i and y[index] == j:
                                dop_dist += 2
                        index += 1
                elif corner[1] == 0 and corner[2] == size:
                    index = 0
                    for i, j in zip(perfect_x, perfect_y):
                        if (i == 0 and j == size - 1) or (i == 1 and
                                                          j == size):
                            if x[index] == i and y[index] == j:
                                dop_dist += 2
                        index += 1
                else:
                    index = 0
                    for i, j in zip(perfect_x, perfect_y):
                        if (i == size - 1 and j == 0) or (i == size and
                                                          j == 1):
                            if x[index] == i and y[index] == j:
                                dop_dist += 2
                        index += 1
        if size == 2:
            dop_dist /= 2
        return dist + dop_dist
    return corner_tiles


def print_path(paths, digits):
    # Распечатать решение в консоли
    size = len(paths[0][0])
    k = int(size ** 0.5)
    puzzle = [0 for i in range(size)]
    for key, i in enumerate(paths):
        for j in range(size):
            puzzle[int(i[0][j] + i[1][j] * k)] = j
        for l, m in enumerate(puzzle):
            if m == 0:
                print('\033[31m{:<2d}\033[0m'.format(m), end=' ')
            elif m == digits[key]:
                print('\033[32m{:<2d}\033[0m'.format(m), end=' ')
            else:
                print('{:<2d}'.format(m), end=' ')
            if (l + 1) % k == 0:
                print()
        print()
    print(f"solution length: \033[34;1m{len(paths) - 1}\033[0m")


def vis_path(paths):
    # Запись решения в файл и запуск визуализации
    size = len(paths[0][0])
    k = int(size ** 0.5)
    puzzle = [0 for i in range(size)]
    with open('puzzle_path.txt', 'w') as file:
        for i in paths:
            for j in range(size):
                puzzle[int(i[0][j] + i[1][j] * k)] = j
            for l in range(k):
                file.writelines("%s\n" % (" ".join(map(str,
                                             puzzle[l * k: l * k + k]))))
            file.writelines('\n')
    if hasattr(ctypes, 'windll'):
        call(['java', '-jar', 'npuzzle-visualiser_win.jar'])
    else:
        call(['java', '-jar', 'npuzzle-visualiser.jar'])


def path(closed_set, map, vis, graphik):
    # Поиск пути в закрытом списке
    path = []
    digits = []
    g = []
    h = []
    f = []
    while closed_set[map][0] is not None:
        path.append(map)
        digits.append(closed_set[map][1])
        if graphik:
            h.append(closed_set[map][-3])
            g.append(closed_set[map][-2])
            f.append(closed_set[map][-1])
        map = closed_set[map][0]
    path.append(map)
    if graphik:
        h.append(closed_set[map][-3])
        g.append(closed_set[map][-2])
        f.append(closed_set[map][-1])
        h.reverse()
        g.reverse()
        f.reverse()
        graph(h, g, f)
    path.reverse()
    digits.append(closed_set[map][1])
    digits.reverse()
    if not vis:
        print_path(path, digits)
    else:
        vis_path(path)


def main():
    parser = parse.get_arguments()
    algo, type, file, heuristics, vis, graph = parse.validation(parser)
    h = 0
    x, y, perfect_x, perfect_y, size = puzzle_validate(type, file)
    if heuristics == 'manhattan':
        heuristic = get_manhattan()
    elif heuristics == 'hamming':
        heuristic = get_hamming()
    elif heuristics == 'linear_conflict':
        heuristic = get_linear_conflict(x)
    else:
        heuristic = get_corner_tiles(x)
    id, open_set, closed_set = 1, [], {}
    start_time = time()
    coordinates = get_true_coordinates(size)
    if algo != 'g':
        g = 1
    else:
        g = 0
    now_state = (tuple(x), tuple(y))
    perfect_state = (tuple(perfect_x), tuple(perfect_y))
    perfect_x, perfect_y = perfect_x[1:], perfect_y[1:]
    if algo != 'u':
        h = heuristic(now_state[0][1:], now_state[1][1:], perfect_x, perfect_y)
    insert(open_set, (h, id, (h, 0, now_state, None, None)))
    h, g_state, now_state, previous, digit = extract_minimum(open_set)[2]
    while now_state != perfect_state:
        if id > 10000000:
            print('Слишком мого операций, похоже, мы здесь надолго')
            exit()
        closed_set[now_state] = previous, digit, h, g_state, h + g_state
        coord = coordinates(now_state[0], now_state[1])
        for i in coord:
            state, now_digit = move_zero(i, list(now_state[0]),
                                         list(now_state[1]))
            if state not in closed_set:
                if algo != 'u':
                    h = heuristic(state[0][1:], state[1][1:],
                                  perfect_x, perfect_y)
                g_new_state = g_state + g
                id += 1
                insert(open_set, (h + g_new_state, id,
                       (h, g_new_state, state, now_state, now_digit)))
        h, g_state, now_state, previous, digit = extract_minimum(open_set)[2]
    closed_set[now_state] = previous, digit, h, g_state, h + g_state
    path(closed_set, now_state, vis, graph)
    if algo == 'a':
        print(f'algorithm: \033[34;1mA-Star\033[0m')
    elif algo == 'g':
        print(f'algorithm: \033[34;1mGreedy search\033[0m')
    else:
        print(f'algorithm: \033[34;1mUniform cost search\033[0m')
    print(f'heuristic: \033[34;1m{heuristics}\033[0m')
    print(f'puzzle type: \033[34;1m{type}\033[0m')
    print(f'complexity in time: \033[34;1m{len(closed_set)}\033[0m')
    print(f'space complexity: \033[34;1m{id}\033[0m')
    print(f"time: \033[34;1m{time() - start_time} seconds\033[0m")


if __name__ == '__main__':
    main()
