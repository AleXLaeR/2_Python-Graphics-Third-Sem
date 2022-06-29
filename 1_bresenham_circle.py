"""
        Алгоритм Брезенхема для рисования окружностей:

В этом алгоритме строится дуга окружности для первой четверти (квадранта),
а координаты точек окружности для остальных квадрантов выходят симметрично.
На каждом шаге рассматриваются три пикселя в зависимости от параметра delta,
и из них выбирается наиболее подходящий путём сравнения расстояний от центра
до выбранного пикселя с радиусом окружности

Сложнсть алгоритма: O(n) в худшем случае, где n - радус окружности.
"""


from PIL import Image


class GridCordsError(ValueError):
    pass


def draw_circle(grid_size: int, radius: int) -> None:
    if grid_size < radius:  # если радиус больше размеров холста, не имеет смысла рисовать круг
        raise GridCordsError('grid size should be >= radius')

    sky_blue_rgb = (0, 191, 255)
    white_rgb = (255,) * 3

    im = Image.new('RGB', (grid_size * 2,) * 2, color=white_rgb)

    initial_x, initial_y = grid_size, grid_size

    # Начинаем с (x=0, y=radius) и двигаемся в первой четверти пока x не станет равным y, т е 45°
    # Ми повинні почати з перерахованих початкових умов:

    delta = 2 - 2 * radius
    x, y = 0, radius

    while y >= 0:
        # рисуем симметричные пиксели-засечки с каждой стороны
        im.putpixel((initial_x + x, initial_y + y), sky_blue_rgb)  # 1-ая четверть
        im.putpixel((initial_x + x, initial_y - y), sky_blue_rgb)  # 2-ая четверть
        im.putpixel((initial_x - x, initial_y + y), sky_blue_rgb)  # 3-ая четверть
        im.putpixel((initial_x - x, initial_y - y), sky_blue_rgb)  # 4-ая четверть

        if delta < 0:  # Если delta < 0, то диагональная точка нах внутри окружности
            x += 1
            delta += 2 * x + 1
        elif delta > 0:  # Если delta > 0, то диагональная точка нах вне окружности
            delta -= 2 * y + 1
            y -= 1
        else:  # если delta = 0, то диагональная точка лежит ровно на окружности
            delta += 2 * (x - y)
            x += 1
            y -= 1

    im.save('crc_im.png')


if __name__ == '__main__':
    draw_circle(300, radius=280)  # круг с центром в начале координат (x=300, y=300)
