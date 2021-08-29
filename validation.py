import copy


def solver(my_puzzle, perfect_puzzle):
    # Определение решаемости пятнашки
    different = 0
    for key in my_puzzle:
        different += len(set(my_puzzle[key]) - set(perfect_puzzle[key]))
    if different % 2 == 1:
        print("Данная комбинация не имеет решения!")
        exit()
    print("Данная комбинация имеет решение, и мы сейчас его найдём!")


def order_dictionary(puzzle):
    # Создание словаря, где ключ - это определённая пятнашка
    # Значение - все пятнашки, стоящие после
    order = {x: puzzle[puzzle.index(x) + 1:] for x in puzzle}
    return order


def puzzle_list(npuzzle, size):
    # Создание списка из пятнашек, где каждая вторая строка перевёрнута
    my_puzzle = []
    puzzle = copy.deepcopy(npuzzle)
    for i in range(size):
        if i % 2 == 1:
            puzzle[i].reverse()
    for i in range(len(puzzle)):
        for j in range(len(puzzle[i])):
            my_puzzle.append(puzzle[i][j])
    if size**2 in my_puzzle:
        my_puzzle.pop(my_puzzle.index(size**2))
    elif 0 in my_puzzle:
        my_puzzle.pop(my_puzzle.index(0))
    puzzle_dict = order_dictionary(my_puzzle)
    return puzzle_dict


def get_puzzle_snail(size):
    # Создание пятнашки-решения по типу змейка
    # 0 в центре, 1 в левом верхнем углу
    puzzle = [[0] * size for i in range(size)]
    st, m = 1, 0
    for v in range(size // 2):
        # Заполнение верхней строки
        for i in range(size - m):
            puzzle[v][i + v] = st
            st += 1
        # Заполнение правого столбца
        for i in range(v + 1, size - v):
            puzzle[i][-v - 1] = st
            st += 1
        # Заполнение нижней строки
        for i in range(v + 1, size - v):
            puzzle[-v - 1][-i - 1] = st
            st += 1
        # Заполнение левого столбца
        for i in range(v + 1, size - (v + 1)):
            puzzle[-i - 1][v] = st
            st += 1
        m += 2
    puzzle_1 = puzzle_list(puzzle, size)
    for i in puzzle:
        if size**2 in i:
            i[i.index(size**2)] = 0
    return puzzle_1, puzzle


def get_puzzle_standard(size):
    # Создание пятнашки-решения по типу стандарт
    # 1 в левом верхнем углу, 0 в правом нижнем
    puzzle = []
    for i in range(1, size + 1):
        puzzle.append([x + (i - 1) * size for x in range(1, size + 1)])
    puzzle_1 = puzzle_list(puzzle, size)
    puzzle[-1][-1] = 0
    return puzzle_1, puzzle


def get_puzzle_reverse_standard(size):
    # Создание пятнашки-решения по типу стандарт наоборот
    # 0 в левом верхнем углу, 1 в правом нижнем
    puzzle = []
    for i in range(size, 0, -1):
        puzzle.append([x + (i - 1) * size for x in range(size, 0, -1)])
    puzzle_1 = puzzle_list(puzzle, size)
    puzzle[0][0] = 0
    return puzzle_1, puzzle


def get_puzzle_reverse_snail(size):
    # Создание пятнашки-решения по типу змейка наоборот
    # 1 в центре, 0 в левом верхнем углу
    puzzle = [[1] * size for i in range(size)]
    st, m = size * size, 0
    for v in range(size // 2):
        # Заполнение верхней строки
        for i in range(size - m):
            puzzle[v][i + v] = st
            st -= 1
        # Заполнение правого столбца
        for i in range(v + 1, size - v):
            puzzle[i][-v - 1] = st
            st -= 1
        # Заполнение нижней строки
        for i in range(v + 1, size - v):
            puzzle[-v - 1][-i - 1] = st
            st -= 1
        # Заполнение левого столбца
        for i in range(v + 1, size - (v + 1)):
            puzzle[-i - 1][v] = st
            st -= 1
        m += 2
    puzzle_1 = puzzle_list(puzzle, size)
    puzzle[0][0] = 0
    return puzzle_1, puzzle


def validate(puzzle):
    # Проверка поданной карты на валидность
    count = len(puzzle)
    if not pow(count, 0.5).is_integer():
        print(f"Карта невалидна: неверное количество значений")
        exit()
    for j in puzzle:
        if puzzle.count(j) > 1:
            print("Карта невалидна: повторение значений\n")
            exit()
        if j >= count or j < 0:
            print(f"""Карта невалидна:
                    значения не в диапазоне от 0 до {count - 1}""")
            exit()


def read_file(file):
    # Считывание пятнашки из поданного файла
    try:
        with open(file, 'r') as file:
            comment = file.readline()
            while comment[0] == '#':
                comment = file.readline()
            puzzle, size = [], ''
            try:
                size = int(comment)
            except ValueError:
                print(f'Некорректное значение размерности {size}')
                exit()
            if size < 1:
                print(f'Некорректное значение размерности {size}')
                exit()
            for i in range(size):
                line = file.readline().split()
                if '#' in line:
                    line = line[:line.index('#')]
                for x in line:
                    if '#' not in x:
                        puzzle.append(x)
            if len(puzzle) ** 0.5 != size:
                print('Размерность карты не соответствует указанной')
                exit()
            another = file.readlines()
            if another:
                for i in another:
                    if i[0] != '#':
                        print("Карта невалидна")
                        exit()
            return puzzle
    except FileNotFoundError:
        print('''Источник данных отсутствует''')
        exit()


def get_puzzle_map(puzzle, size):
    # определение координат каждой пятнашки по оси х и у
    x, y = [0] * size, [0] * size
    for i, j in enumerate(puzzle):
        for k, l in enumerate(j):
            x[l], y[l] = k, i
    return x, y


def input_puzzle():
    # Чтение паззла из командной строки
    comment = input()
    while comment[0] == '#':
        comment = input()
    puzzle, size = [], ''
    try:
        size = int(comment)
    except ValueError:
        print(f'Некорректное значение размерности {size}')
        exit()
    if size < 1:
        print(f'Некорректное значение размерности {size}')
        exit()
    for i in range(size):
        line = input().split()
        if '#' in line:
            line = line[:line.index('#')]
        for x in line:
            if '#' not in x:
                puzzle.append(x)
    if len(puzzle)**0.5 != size:
        print('Размерность карты не соответствует указанной')
        exit()
    return puzzle


def puzzle_validate(types, file):
    if not file:
        puzzle = input_puzzle()
    else:
        puzzle = read_file(file)
    try:
        puzzle = [int(x) for x in puzzle]
    except ValueError:
        print('Неверная карта')
        exit()
    validate(puzzle)
    count = len(puzzle)
    size = int(pow(count, 0.5))
    my_puzzle = [puzzle[i * size: (i + 1) * size] for i in range(size)]
    if types == 'snail':
        perfect_puzzle_solv, perfect_puzzle = get_puzzle_snail(size)
    elif types == 'reverse_snail':
        perfect_puzzle_solv, perfect_puzzle = get_puzzle_reverse_snail(size)
    elif types == 'standard':
        perfect_puzzle_solv, perfect_puzzle = get_puzzle_standard(size)
    else:
        perfect_puzzle_solv, perfect_puzzle = get_puzzle_reverse_standard(size)
    my_puzzle_solv = puzzle_list(my_puzzle, size)
    solver(my_puzzle_solv, perfect_puzzle_solv)
    my_x, my_y = get_puzzle_map(my_puzzle, count)
    perfect_x, perfect_y = get_puzzle_map(perfect_puzzle, count)
    return my_x, my_y, perfect_x, perfect_y, size
