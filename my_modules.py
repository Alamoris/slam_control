import math
import numpy


# инвертированный range
def reversedRange(x):
    while x > 0:
        yield x
        x -= 1


# Рассчет длинны гипотенузы
def gip_len(first_x, first_y, fin_x, fin_y):
    gip = math.sqrt((first_x - fin_x) ** 2 + (first_y - fin_y) ** 2)
    return gip


# Алгоритм Дийкстры
def dejkstraAlg(points, connections, start_point):
    # Рекурсивная функция выполняющая поиск путей во взвешеном графе
    def dejkstraAnalyzer(cur_point, vektor, matrix_graph, checked_points, points_weigths):
        """
        Алгоритм работает с однонаправленным взвешеным графом
        :param cur_point: Текущая точка работы алгоритма
        :param vektor: Вектор наикратчайших путей
        :param matrix_graph: Матрица весов графа
        :param checked_points: Массив пройденых точек
        :param points_weigths: Веса каждой точки, изначально задаются как 9999(длинна между точками не превышает
        данного значния)
        :return:
        """
        point_array = [i for i in range(len(matrix_graph[cur_point])) if matrix_graph[cur_point][i] != 0]
        next_point_array = []

        for i in point_array:
            if i not in checked_points:
                if points_weigths[i] > matrix_graph[cur_point, i]:
                    points_weigths[i] = matrix_graph[cur_point, i] + points_weigths[cur_point]
                    next_point_array.append(i)
                    vektor[i] = cur_point

        checked_points.append(cur_point)

        for i in range(len(next_point_array)):
            idx_min = i
            for j in range(i + 1, len(next_point_array)):
                if points_weigths[j] < points_weigths[idx_min]:
                    idx_min = j
            tmp = next_point_array[idx_min]
            next_point_array[idx_min] = next_point_array[i]
            next_point_array[i] = tmp

        if next_point_array:
            for i in next_point_array:
                dejkstraAnalyzer(i, vektor, matrix_graph, checked_points, points_weigths)
        else:
            return vektor

    points_weigths = [9999 for x in range(len(connections) + 1)]
    points_weigths[start_point] = 0

    if not points:
        vektor = [start_point for x in range(len(connections) + 1)]
        matrix_graph = numpy.zeros((len(connections) + 1, len(connections) + 1))
    else:
        vektor = [start_point for x in range(len(points))]
        matrix_graph = numpy.zeros((len(points), len(points)))

    for x in connections:
        if not points:
            length = 1
        else:
            length = gip_len(points[x[0]][0], points[x[0]][1], points[x[1]][0], points[x[1]][1])

        matrix_graph[x[0], x[1]] = length
        matrix_graph[x[1], x[0]] = length

    checked_points = []

    dejkstraAnalyzer(start_point, vektor, matrix_graph, checked_points, points_weigths)
    return vektor


# Поиск пути по вектору полученому из алгоритма Дийкстры
def takeWay(start_point, fin_point, vektor):
    de_way = [fin_point]
    next_point = fin_point
    while True:
        de_way.append(vektor[next_point])
        next_point = vektor[next_point]
        if next_point == start_point:
            break
    return de_way


# Нормализация случайных значений cons в последовательный набор чисел, для работы алгоритма Дийкстры
# Требуется из-за добавления соединений из общего массива TODO!!!
def normalizeDejkstraValues(cons):
    max_arg = 0
    our_points = []
    for i in cons:
        for x in i:
            if x not in our_points:
                our_points.append(x)

    normalize_dict = {}
    decode_dict = {}
    k = 0
    for x in our_points:
        normalize_dict[x] = k
        decode_dict[k] = x
        k += 1

    normalize_cons = []
    for i in cons:
        normalize_cons.append((normalize_dict[i[0]], normalize_dict[i[1]]))

    return normalize_cons, normalize_dict, decode_dict


def wayDecoder(inp_vektor, decode_dict):
    decoded_vektor = inp_vektor
    for i in range(len(inp_vektor)):
        decoded_vektor[i] = decode_dict[inp_vektor[i]]
    return decoded_vektor
