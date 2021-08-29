from sys import argv
from argparse import ArgumentParser


def get_arguments():
    parser = ArgumentParser(prog='npuzzle.py', description='''
    Эта программа позволяет собирать пятнашки размером 3 на 3''',
                            add_help=True, epilog='''
    (c) November 2020''')
    parser.add_argument('--algo', '-algo', default='a',
                        help='''Тип используемого алгоритма:
                            a -     A-Star;
                            g -     Greedy search: ignores the g(n);
                            u -     Uniform cost search: ignores the h(n)''')
    parser.add_argument('--type', '-type', default='snail',
                        help='''Тип сбора пятнашки:
                        snail -             сбор змейкой, 0 в центре;
                        reverse_snail - сбор змейкой, 0 в левом верхнем углу;
                        standard -  1 в левом верхнем углу, 0 в правом нижнем;
                        reverse_standard - 0 в левом верхнем углу, 1;
                        в правом нижнем''')
    parser.add_argument('--file', '-file',
                        help='Имя файла,из которого нужно считать карту')
    parser.add_argument('--heuristic', '-heuristic', default='manhattan',
                        help='''Тип Используемой эвристики:
                            manhattan        -   манхэттенское расстояние;
                            linear_conflict  -   линейный конфликт;
                            hamming          -   расстояние Хэмминга;
                            corner_tiles     -   эвристика угловых клеток''')
    parser.add_argument('--vis', '-vis',  action='store_const', const=True,
                        help='Визуализация сбора пятнашки')
    parser.add_argument('--graph', '-graph', action='store_const', const=True,
                        help='График изменения ключевых показателей')
    return parser


def validation(parser):
    name = parser.parse_args(argv[1:])
    type, file, heuristic = name.type, name.file, name.heuristic
    algo, vis, graph = name.algo, name.vis, name.graph
    return algo, type, file, heuristic, vis, graph
