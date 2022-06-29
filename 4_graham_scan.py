"""
    Алгоритм Грехема построения выпуклой оболочки в двумерном пространстве:

В этом алгоритме задача о выпуклой оболочке решается с помощью стека, сформированного из точек-кандидатов.
Все точки входного множества заносятся в стек, а потом точки, не являющиеся вершинами выпуклой оболочки,
со временем удаляются из него. По завершении работы алгоритма в стеке остаются только вершины оболочки
в порядке их обхода против часовой стрелки.

Время работы алгоритма (ф-ии graham_scan): сложность будет O(n * log(n)), где n = |Q|, и Q - мн-во точек.
Циклу внутри потребуется время O(n), в то время как сортировка полярных углов займет O(n * (log(n)) времени,
откуда и следует общая асимптотика этой функции.
"""

import math
from pprint import pprint
from random import randint
from typing import Sequence, Optional, Any

import matplotlib.pyplot as plt


# генерирует случайные точки в кол-ве how_many
def create_points(_min: int = 0,
                  _max: int = 50,
                  *,
                  how_many: int = 1) -> Sequence[list[int]]:
    return [[randint(_min, _max), randint(_min, _max)]
            for _ in range(how_many)]


# Создает и заполняет холст;
# В ф-ю передается список всех точек и список тех, из которых будет состоять фигура
def scatter_plot(coords: Sequence[list[float]], convex_hull: Optional[Any] = None) -> None:
    xs, ys = zip(*coords)  # витягуємо координати x and y зі списку і записуємо в змінні

    plt.scatter(xs, ys, c='deeppink')  # отображаем точки на холсте
    if convex_hull is not None:  # если еще точки из МВО

        # строим границу (кривая H по опр.) МВО, доп. итерация для того, чтобы соединить перву точку с последней
        for i in range(1, len(convex_hull) + 1):
            if i == len(convex_hull):
                i = 0  # граница

            c0 = convex_hull[i - 1]
            c1 = convex_hull[i]

            plt.plot((c0[0], c1[0]), (c0[1], c1[1]), 'y')  # соединяем точки на холсте
    plt.show()


# Вычисляет полярный угол (в рад) от p0 до p1.
# Если p1 is None, то по ум заменяется на глобальную переменную anchor
def polar_angle(p0: Sequence[float], p1: Optional[Sequence[float]] = None) -> float:
    if p1 is None:
        p1 = anchor

    y_span = p0[1] - p1[1]
    x_span = p0[0] - p1[0]

    return math.atan2(y_span, x_span)


# Выисляет евклидово расстояние от p0 до p1,
# Если p1 is None, то по ум заменяется на глобальную переменную anchor
def distance(p0: Sequence[float], p1: Optional[Sequence[float]] = None):
    if p1 is None:
        p1 = anchor

    y_span = p0[1] - p1[1]
    x_span = p0[0] - p1[0]

    return y_span ** 2 + x_span ** 2


# Вычисляет det матрицы 3x3.
# [p1(x) p1(y) 1]
# [p2(x) p2(y) 1]
# [p3(x) p3(y) 1]
# Если det > 0, то против часовой стрелки
# Если det < 0, то по часовой стрелке
# Если det = 0, то коллинеарны
def det(p1, p2, p3):
    return (p2[0] - p1[0]) * (p3[1] - p1[1]) \
           - (p2[1] - p1[1]) * (p3[0] - p1[0])


# Сортировка по возрастания полярного угла от точки привязки.
# Для любых значений с раными полярными углами применяется второй тип сортировки,
# обеспечивающий увеличение расстояния от точки "якоря"
def quicksort(a: Sequence[list[float]]) -> Any:
    if len(a) <= 1:
        return a

    smaller, equal, larger = [], [], []
    pivoting_angle = polar_angle(a[randint(0, len(a) - 1)])  # выбираю случайную точку поворота

    for pt in a:
        pol_angle = polar_angle(pt)  # вычисляю полярный угол текущей точки

        if pol_angle < pivoting_angle:
            smaller.append(pt)
        elif pol_angle == pivoting_angle:
            equal.append(pt)
        else:
            larger.append(pt)

    return quicksort(smaller) + \
           sorted(equal, key=distance) + \
           quicksort(larger)


# Находим вершины-границы выпуклой оболочки.
# Входные точки - список координат (x, y).
# если show_progress == True, построение каркаса будет происходить на каждой итерации
def graham_scan(points: Sequence[list[float]],
                *,
                show_progress: bool = False) -> list[Any]:
    global anchor

    # Находим точку (x, y) с наименьшим значением y,
    # а также с ее индексом в списке точек. Если
    # существует несколько точек с одинаковым значением y,
    # Выбираем ту, у которой x - наименьший.
    min_idx = None
    for i, (x, y) in enumerate(points):
        if min_idx is None or y < points[min_idx][1]:
            min_idx = i
        if y == points[min_idx][1] and x < points[min_idx][0]:
            min_idx = i

    # устанавливаю глобальную переменную, которая будет необходима в ф-ях polar_angle() и distance()
    anchor = points[min_idx]

    # Сортируем точки по полярному углу, затем удаляем якорь из нового отсортированного списка
    sorted_pts = quicksort(points)
    del sorted_pts[sorted_pts.index(anchor)]

    # Якорь и точка с наименьшим полярным углом всегда будут на figure
    hull = [anchor, sorted_pts[0]]
    for s in sorted_pts[1:]:
        while det(hull[-2], hull[-1], s) <= 0:
            del hull[-1]

        hull.append(s)
        if show_progress:
            scatter_plot(points, hull)
    return hull


def main():
    pts = create_points(how_many=20)
    pprint(f'Points: {pts}')

    hull = graham_scan(pts, show_progress=True)
    pprint(f'Hull: {hull}')

    scatter_plot(pts, hull)

    plt.show()


if __name__ == '__main__':
    main()
