# Copyright (C) 2023 Gubaydullin Nurislam - All Rights Reserved
# You can't use this code to generate the answer to your course work
#
# You can write me in telegram about course work ― @tonitaga
# If not, prease use the telegram bot or visit   ― @CalculatorlevlevBot

import math as m
from tabulate import tabulate
from .basecourseworkpart import BaseCourseWorkPart


class CourseWorkPartCutterPrismatic(BaseCourseWorkPart):
    """
    This class solving prismatic cutter, calculating all parts of course work

    The initializing data is dictionary, dictionary must have that keys for correct work:

    data = {
        'D': float,  -> Основной диаметр

        'D1': float,  -> Первый диаметр

        'l1': float,  -> Первая длина

        'l2': float,  -> Вторая длина

        'l3': float,  -> Третья длина

        'L':  float,  -> Общая длина

        'f':  float   -> Размер фаски
    }
    """

    def __init__(self, data: dict) -> None:
        self.data = data
        self.__output_str = ""
        self.__methods = [
            method for method in dir(CourseWorkPartCutterPrismatic)
                if callable(getattr(CourseWorkPartCutterPrismatic, method)) and
                   method.startswith('_CourseWorkPartCutterPrismatic__part')
        ]
        self.D = self.data['D']
        self.D1 = self.data['D1']
        self.l1 = self.data['l1']
        self.l2 = self.data['l2']
        self.l3 = self.data['l3']
        self.L = self.data['L']
        self.f = self.data['f']

    def calculate_part(self) -> None:
        for i in range(0, len(self.__methods)):
            method_index = self.__methods.index(f"_CourseWorkPartCutterPrismatic__part_{i}")
            getattr(self, self.__methods[method_index])()

    def save_data(self, path: str) -> None:
        text_file = open(path, "w+", encoding="utf-8")
        text_file.write(self.__output_str)
        text_file.close()

    def __part_0(self):
        self.__output_str += f"\tПРОЕКТИРОВАНИЕ ФАСОННОГО РЕЗЦА\n"
        self.__output_str += f"\tИсходные данные\n"
        self.__output_str += f"Рассчитать и сконструировать призматический фасонный резец для наружного обтачивания детали, изготовляемой из стали.\n"
        self.__output_str += f"- D = {self.D} мм\n- D1 = {self.D1} мм\n- L = {self.L} мм\n- l1 = {self.l1} мм\n" + \
                             f"- l2 = {self.l2} мм\n- l3 = {self.l3} мм\n- f = {self.f} мм\n"

    def __part_1(self):
        self.steel = "Сталь 40"
        self.__output_str += "1)Рекомендуемые значения углов\n"
        self.__output_str += "Для улучшения процесса стружкообразования, повышения качетва обработанной поверхности и увеличения стойкости резцов\n" + \
                             "необходимо задавать оптимальные значения углов γ и α\n"
        self.__output_str += f"Для {self.steel} по таблице 1.14 выбираем  γ и α:\n"
        self.alpha = self.gamma = 10
        self.sigma_b = 700
        self.__output_str += f"\tПри σв = 700 мн/м², принимаем γ = 10, α = 10\n"

    def __part_2(self):
        self.__output_str += "2)Длина обрабатываемой поверхности призматическим резцом\n"
        self.delta_work = self.l3 - self.l1
        self.__output_str += f"\tΔп = l3 - l1 = {self.l3} - {self.l1} = {self.delta_work} мм\n"

    def __part_3(self):
        self.__output_str += "3)Определение количества точек на участке (2-3)\n"
        self.step = 5
        self.section_count = round(self.delta_work / self.step, 2)
        if m.ceil(self.section_count) >= 8:
            self.step = 10
            self.section_count = round(self.delta_work / self.step, 2)
        self.__output_str += "Криволинейный участок 2-3 может быть разбит на сколько угодно малые отрезки 2-a, a-b, b-c и т.д.\n" + \
                             "Каждый отрезок можно считать образующей элементарного усеченного конуса.\n"
        self.__output_str += f"\tкол-во отвезков = Δп / {self.step} = {self.delta_work} / {self.step} = {self.section_count}\n" + \
                             f"\tПринимаем кол-во отрезков = {m.ceil(self.section_count)}\n"
        self.section_count = m.ceil(self.section_count)
        self.points_count = round(self.section_count - 1)
        self.__output_str += f"\tТогда i = кол-во отрезков - 1 = {self.points_count} точек\n"
        self.alphabit = "abcdefgjklmnop"
        self.__output_str += f"\tОтрезки: 2 - а"
        for i in range(1, self.points_count + 1):
            if i != self.points_count:
                self.__output_str += f", {self.alphabit[i - 1]} - {self.alphabit[i]}"
            else:
                self.__output_str += f", {self.alphabit[i - 1]} - 3\n"

    def __part_4(self):
        image = str()
        if self.points_count == 7:
            image = '\n   --------------------------------------------------------------------------------------------------------------------\n' + \
                    '            ║            ║             ║                                                              ║       ║  ║\n' * 12 + \
                    '            ║            ║             ║                                                              ║       ║  /\n' + \
                    '            ║            ║             ║                                                              ║       ║ /\n' + \
                    '            ║            ●=============●                                                              ●=======●/\n' + \
                    '            ║            ║1           2 \_                                                          _/ 3      4\n' + \
                    '            ║            ║                \_●                                                    ●_/\n' + \
                    '            ║            ║                 a \__                                              __/ g\n' + \
                    '            ║            ║                      \___●                                   ●____/\n' + \
                    '            ║            ║                         b \_______●                  ●______/ f\n' + \
                    '            ║            ║                                  c \________●_______/ e\n' + \
                    '            ║============║                                             d\n\n\n'
        if self.points_count == 6:
            image = '\n   --------------------------------------------------------------------------------------------------------------------\n' + \
                    '            ║            ║             ║                                                              ║       ║  ║\n' * 12 + \
                    '            ║            ║             ║                                                              ║       ║  /\n' + \
                    '            ║            ║             ║                                                              ║       ║ /\n' + \
                    '            ║            ●=============●                                                              ●=======●/\n' + \
                    '            ║            ║1           2 \_                                                          _/ 3      4\n' + \
                    '            ║            ║                \__                                                    _●/\n' + \
                    '            ║            ║                   \_●                                              __/ f\n' + \
                    '            ║            ║                    a \____                                  ____●_/\n' + \
                    '            ║            ║                           \___●____                  _●____/    e\n' + \
                    '            ║            ║                               b    \________●_______/ d\n' + \
                    '            ║============║                                              c\n\n\n'
        elif self.points_count == 5:
            image = '\n   --------------------------------------------------------------------------------------------------------------------\n' + \
                    '            ║            ║             ║                                                              ║       ║  ║\n' * 12 + \
                    '            ║            ║             ║                                                              ║       ║  /\n' + \
                    '            ║            ║             ║                                                              ║       ║ /\n' + \
                    '            ║            ●=============●                                                              ●=======●/\n' + \
                    '            ║            ║1           2 \_                                                          _/ 3      4\n' + \
                    '            ║            ║                \__                                                    __/\n' + \
                    '            ║            ║                   \_●                                              ●_/\n' + \
                    '            ║            ║                    a \____                                   _____/ e\n' + \
                    '            ║            ║                           \___●____                  ____●__/ \n' + \
                    '            ║            ║                               b    \________●_______/    d\n' + \
                    '            ║============║                                             c\n\n\n'
        elif self.points_count == 4:
            image = '\n   --------------------------------------------------------------------------------------------------------------------\n' + \
                    '            ║            ║             ║                                                              ║       ║  ║\n' * 12 + \
                    '            ║            ║             ║                                                              ║       ║  /\n' + \
                    '            ║            ║             ║                                                              ║       ║ /\n' + \
                    '            ║            ●=============●                                                              ●=======●/\n' + \
                    '            ║            ║1           2 \_                                                          _/ 3      4\n' + \
                    '            ║            ║                \__                                                    __/\n' + \
                    '            ║            ║                   \__                                              _●/\n' + \
                    '            ║            ║                      \____                                   _____/ d\n' + \
                    '            ║            ║                           \●_______                  _____●_/\n' + \
                    '            ║            ║                            a       \________●_______/     c\n' + \
                    '            ║============║                                             b\n\n\n'
        elif self.points_count == 3:
            image = '\n   --------------------------------------------------------------------------------------------------------------------\n' + \
                    '            ║            ║             ║                                                              ║       ║  ║\n' * 12 + \
                    '            ║            ║             ║                                                              ║       ║  /\n' + \
                    '            ║            ║             ║                                                              ║       ║ /\n' + \
                    '            ║            ●=============●                                                              ●=======●/\n' + \
                    '            ║            ║1           2 \_                                                          _/ 3      4\n' + \
                    '            ║            ║                \__                                                    __/\n' + \
                    '            ║            ║                   \__                                              __/\n' + \
                    '            ║            ║                      \___●                                   ●____/\n' + \
                    '            ║            ║                         a \________                  _______/ c\n' + \
                    '            ║            ║                                    \________●_______/\n' + \
                    '            ║============║                                             b\n\n\n'
        elif self.points_count == 2:
            image = '\n   --------------------------------------------------------------------------------------------------------------------\n' + \
                    '            ║            ║             ║                                                              ║       ║  ║\n' * 12 + \
                    '            ║            ║             ║                                                              ║       ║  /\n' + \
                    '            ║            ║             ║                                                              ║       ║ /\n' + \
                    '            ║            ●=============●                                                              ●=======●/\n' + \
                    '            ║            ║1           2 \_                                                          _/ 3      4\n' + \
                    '            ║            ║                \__                                                    __/\n' + \
                    '            ║            ║                   \__                                              __/\n' + \
                    '            ║            ║                      \____                                   ●____/\n' + \
                    '            ║            ║                           \________                  _______/ b\n' + \
                    '            ║            ║                                    \________●_______/\n' + \
                    '            ║============║                                             a\n\n\n'
        elif self.points_count == 1:
            image = '\n   --------------------------------------------------------------------------------------------------------------------\n' + \
                    '            ║            ║             ║                                                              ║       ║  ║\n' * 12 + \
                    '            ║            ║             ║                                                              ║       ║  /\n' + \
                    '            ║            ║             ║                                                              ║       ║ /\n' + \
                    '            ║            ●=============●                                                              ●=======●/\n' + \
                    '            ║            ║1           2 \_                                                          _/ 3      4\n' + \
                    '            ║            ║                \__                                                    __/\n' + \
                    '            ║            ║                   \__                                              __/\n' + \
                    '            ║            ║                      \____                                   _____/\n' + \
                    '            ║            ║                           \________                  _______/ \n' + \
                    '            ║            ║                                    \________●_______/\n' + \
                    '            ║============║                                             a\n\n\n'
        self.__output_str += image

    def __part_5(self):
        self.__output_str += "4)Определение радиусов узловых точек профиля детали\n"
        self.__output_str += "По формуле определяем радиусы точек:\n"
        self.__output_str += "\t      ________________\n"
        self.__output_str += f"\tri = √(D / 2)² - (ih)²\n"
        self.__output_str += "где i - число шагов, h - шаг\n"

        step_array = list()
        step_start = m.floor(self.points_count / 2)
        if self.points_count % 2 != 0:
            for i in range(self.points_count):
                step_array.append(abs(step_start - i))
        else:
            step_start -= 1
            for i in range(self.points_count):
                step_array.append(abs(step_start - i))
        self.radiuses = list()
        for i in range(1, self.points_count + 1):
            self.radiuses.append(round(m.sqrt((self.D / 2) ** 2 - (step_array[i - 1] * self.step) ** 2), 2))
            self.__output_str += f"\t      ____________________\n"
            self.__output_str += f"\tr{self.alphabit[i - 1]} = √({self.D} / 2)² - ({step_array[i - 1]} * {self.step})² = {self.radiuses[i - 1]} мм\n"
        r1 = r2 = round(m.sqrt((self.D / 2) ** 2 - (self.l2 - self.l1) ** 2), 2)
        r3 = r4 = round(m.sqrt((self.D / 2) ** 2 - (self.l3 - self.l2) ** 2), 2)
        self.__output_str += f"\t           _____________________    _____________________\n"
        self.__output_str += f"\tr1 = r2 = √(D / 2)² - (l2 - l1)² = √({self.D} / 2)² - ({self.l2} - {self.l1})² = {r1} мм\n"
        self.__output_str += f"\t           _____________________    _____________________\n"
        self.__output_str += f"\tr3 = r4 = √(D / 2)² - (l3 - l2)² = √({self.D} / 2)² - ({self.l3} - {self.l2})² = {r3} мм\n"

        self.table_1 = [['  ', 1, 2],
                        ['ri', r1, r2],
                        ['li', 0, self.l1]]
        for i in range(self.points_count):
            self.table_1[0].append(self.alphabit[i])
        self.table_1[0].append(3)
        self.table_1[0].append(4)

        for item in self.radiuses:
            self.table_1[1].append(item)
        self.table_1[1].append(r3)
        self.table_1[1].append(r4)

        middle_l = self.l2
        for i in range(self.points_count):
            if i < self.points_count / 2:
                self.table_1[2].append(middle_l - step_array[i] * self.step)
            else:
                self.table_1[2].append(middle_l + step_array[i] * self.step)
        self.table_1[2].append(self.l3)
        self.table_1[2].append(self.L)
        self.__output_str += '\n' + tabulate(self.table_1, headers='firstrow', tablefmt='fancy_grid') + "\n\n"

    def __part_6(self):
        self.__output_str += "\tАлгоритмы расчета фасонных резцов\n\n"
        self.__output_str += "Профиль фасонного резца, как правило, не совпадает с профилем\n" + \
                             "обрабатываемой детали, что требует корректирование профиля резца.\n" + \
                             "Для этого определяют размеры осевого сечения для призматических фасонных резцов.\n" + \
                             "Корректирование профиля фасонных резцов проводится двумя способами:\n" + \
                             "\tграфическим и аналитическим.\n"
        self.__output_str += "Аналитический расчет фасонного резца заключается:\n" + \
                             "- В определении расстояния С по передней поверхности резца от точки с\n" + \
                             "минимальным радиусом детали до всех остальных опорных точек.\n"
        self.__output_str += "- В определении радиусов резца соответствующих опорным точкам детали.\n" + \
                             "Обозначим цифрами 1, 2 ... узловые точки заданного профиля.\n" + \
                             "Радиусы r1, r2 ... до узловых точек детали найдены выше.\n" + \
                             "Для расчета профиля призматических фасонных резцов необходимо определить\n" + \
                             "расстояние Сi.\n"

    def __part_7(self):
        self.__output_str += "\t      ___________________\n"
        self.__output_str += "\tCi = √ri² - rmin²*sin²(γ) + rmin*cos(180-γ)\n"
        rmin = min(self.table_1[1][1:])
        self.__output_str += f"где rmin = {rmin} мм\n"
        self.table_2 = [self.table_1[0],
                        ['Ci'],
                        ['Pi']]
        index = 1
        for ri in self.table_1[1][1:]:
            tmp = round(m.sqrt(ri ** 2 - rmin ** 2 * m.sin(m.radians(self.gamma)) ** 2) + rmin * m.cos(
                m.radians(180 - self.gamma)), 2)
            self.__output_str += "\t      ___________________                      ________________________\n"
            self.__output_str += f"\tC{self.table_1[0][index]} = √r{self.table_1[0][index]}² - rmin²*sin²(γ) + rmin*cos(180-γ) = " + \
                                 f"√{ri}² - {rmin}² * sin²({self.gamma}) + {rmin} * cos(180 - {self.gamma}) = {tmp} мм\n"
            self.table_2[1].append(tmp)
            index += 1

    def __part_8(self):
        self.__output_str += "\nИскомые силы в осевом сечении призматического фасонного резца для\n" + \
                             "наружной обработки могут быть вычислены по формулам\n"
        self.__output_str += "\tPi = Ci * cos(γ + α)\n\n"
        index = 1
        for ci in self.table_2[1][1:]:
            tmp = round(ci * m.cos(m.radians(self.alpha + self.gamma)), 2)
            self.__output_str += f"\tP{self.table_1[0][index]} = C{self.table_1[0][index]} * cos({self.gamma} + {self.alpha}) = {tmp} мм\n"
            self.table_2[2].append(tmp)
            index += 1
        self.__output_str += '\n' + tabulate(self.table_2, headers='firstrow', tablefmt='fancy_grid') + '\n\n'
