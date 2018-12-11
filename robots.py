import math

from my_modules import gip_len


class Robot():
    def __init__(self, start_point):
        self.pos_connection = [start_point, start_point]
        self.pos_length = 1
        self.mission = []

        # Расстояние в пикселях(дискрета), которое робот будет проходить за один цикл
        self.speed = 1

    def paintngStep(self):
        if len(self.pos_connection) == 1:
            return self.pos_connection[0][0], self.pos_connection[0][1]
        elif len(self.pos_connection) == 2:
            first_x = self.pos_connection[0][0]
            first_y = self.pos_connection[0][1]
            fin_x = self.pos_connection[1][0]
            fin_y = self.pos_connection[1][1]

            # TODO: что бы на каждой итерации не просчитывать значение gip_len сделать с ней переменную self
            # Проверяем будет ли следующий шаг увеличения длинны больше длинны ребра и если будет возвращаем последнюю точку
            if self.pos_length > gip_len(first_x, first_y, fin_x, fin_y):
                return True, True, fin_x, fin_y

            # Костыль при y = const
            # ошибка возникает из-за того, что в выведенном уравнении при расчете new_x делитель = 0
            if first_y == fin_y:
                if first_x > fin_x:
                    return first_x, first_y, first_x - self.pos_length, first_y
                else:
                    return first_x, first_y, first_x + self.pos_length, first_y

            # Функция рассчета следующей точки на прямой при известной первой и последней точки и длинны от первой точки
            numerator = self.pos_length ** 2 * (fin_y - first_y) ** 2
            denominator = (fin_x - first_x) ** 2 + (fin_y - first_y) ** 2
            new_y = math.sqrt(numerator / denominator) + first_y
            new_x = (((new_y - first_y) / (fin_y - first_y)) * (fin_x - first_x)) + first_x

            # Костыль переворачивающий значение найденной точки, поскольку по формуле новая точка всегда направлена
            # в сторону увеличения y
            if first_y > fin_y:
                # Проверка, достиг ли x конечной точки, что бы еще раз не переворачивать координаты
                if new_x != fin_x or new_y != fin_y:
                    new_x = first_x + first_x - new_x
                    new_y = first_y + first_y - new_y

            self.pos_length += self.speed
            return first_x, first_y, new_x, new_y

