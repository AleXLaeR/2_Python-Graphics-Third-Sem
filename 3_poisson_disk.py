# Источники и ссылки:
# Роберт Бридсон, SIGGRAPH, 2007 - https://www.researchgate.net/publication/234801901_Fluid_simulation_
# SIGGRAPH_2007_course_notes_Video_files_associated_with_this_course_are_available_from_the_citation_page
# https://github.com/rougier/from-python-to-numpy/blob/master/code/Bridson_sampling.py
# https://sighack.com/post/poisson-disk-sampling-bridsons-algorithm

# Задание: выполнить семплирование поверхности в пространстве и отобразить результат в виде графика,
# используя алгоритм семплирования Роберта Бридсона

# Сложность алгоритма: ссылаясь на исследования по
# https://www.osti.gov/servlets/purl/1109248, https://escholarship.org/content/qt8xv0237z/qt8xv0237z.pdf?t=ptt40r,
# алгоритм имеет сложность выполнения и затрат памяти O(n * log(n)), где n - количество дротиков в области

from typing import Sequence

import numpy as np
import matplotlib.pyplot as plt


def poisson_disk(width: float,
                 height: float,
                 *,
                 k: int = 10,
                 radius: int = 10) -> np.ndarray:

    # Вычислить координаты диап, в который попадает точка
    def squared_distance(p0: Sequence[float], p1: Sequence[float]) -> float:
        return (p0[0] - p1[0]) ** 2 + (p0[1] - p1[1]) ** 2

    def random_point_around(p: Sequence[float], k: int) -> np.ndarray:  # генерируем случайные точки около p
        R = np.random.uniform(radius, 2 * radius, k)
        T = np.random.uniform(0, 2 * np.pi, k)
        P = np.empty((k, 2))

        P[:, 0] = p[0] + R * np.sin(T)
        P[:, 1] = p[1] + R * np.cos(T)

        return P

    def in_limits(p: Sequence[float]) -> bool:  # проверяем, входит ли точка p в изначально заданные пределы холста
        return 0 <= p[0] < width and 0 <= p[1] < height

    # находим индексы точек в соседних диап, по координатам
    def neighborhood(shape: Sequence[float], index: Sequence[int], n: int = 2) -> np.ndarray:
        row, col = index
        row0, row1 = max(row - n, 0), min(row + n + 1, shape[0])
        col0, col1 = max(col - n, 0), min(col + n + 1, shape[1])

        I = np.dstack(np.mgrid[row0:row1, col0:col1])
        I = I.reshape(I.size // 2, 2).tolist()

        I.remove([row, col])
        return I

    def in_neighborhood(p: Sequence[float]):  # можно ли использовать точку p как пример?

        # Она должна быть на расстоянии не менее r от любой другой точки
        i, j = int(p[0] / cellsize), int(p[1] / cellsize)

        if M[i, j]:
            return True

        for (i, j) in N[(i, j)]:
            if M[i, j] and squared_distance(p, P[i, j]) < squared_radius:
                return True

        return False

    def add_point(p: Sequence[float]) -> None:  # добавляем точку в очередь для нанесения на холст
        points.append(p)
        i, j = int(p[0] // cellsize), int(p[1] // cellsize)
        P[i, j], M[i, j] = p, True

    cellsize = radius / np.sqrt(2)  # 2 - ndim
    rows = int(np.ceil(width / cellsize))
    cols = int(np.ceil(height / cellsize))

    # Рад**2, т к мы сравниваем квадрат расстояния
    squared_radius = radius ** 2

    # Позиции решеточек
    P = np.zeros((rows, cols, 2), dtype=np.float32)
    M = np.zeros((rows, cols), dtype=bool)

    #Генерация кеша для соседей - neighborhood
    N = {}
    for i in range(rows):
        for j in range(cols):
            N[(i, j)] = neighborhood(M.shape, (i, j), 2)

    points = []
    add_point((np.random.uniform(width), np.random.uniform(height)))
    while len(points):  # добавляем точки в очередь для нанесения на холст
        i = np.random.randint(len(points))
        p = points[i]
        del points[i]
        Q = random_point_around(p, k)
        for q in Q:
            if in_limits(q) and not in_neighborhood(q):
                add_point(q)
    return P[M]


def main():
    fig, ax = plt.subplots()
    ax.grid(which='both')

    grid_size = 80
    points = poisson_disk(grid_size, grid_size + 20, radius=8)

    x_cords, y_cords = [], []
    for x, y in points:
        x_cords.append(x)
        y_cords.append(y)

    ax.scatter(x_cords, y_cords,
               color='b', s=15, marker='x')

    ax.set_xlim(-5, grid_size + 5)
    ax.set_ylim(-5, grid_size + 25)
    ax.twinx()

    plt.show()


if __name__ == '__main__':
    main()
