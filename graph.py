import matplotlib.pyplot as plt


def graph(h, g, f):
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.plot(h, linewidth=2, color='lawngreen', label='heuristic',
            marker='o', markersize=5,)
    ax.plot(g, linewidth=2, color='orange', label='step',
            marker='X', markersize=7)
    ax.plot(f, linewidth=2, color='indigo', label='algorithm result',
            marker='s', markersize=5)
    ax.set_title('''Изменение значений ключевых показателей
    в процессе решения пятнашки''')
    ax.legend(loc='upper left')
    ax.set_xlabel('Номер хода', labelpad=18)
    ax.set_ylabel('Значение показателя', labelpad=18)
    fig.tight_layout()
    plt.savefig('graph.png')
    plt.show()

