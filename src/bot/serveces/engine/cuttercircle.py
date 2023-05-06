# Copyright (C) 2023 Gubaydullin Nurislam - All Rights Reserved
# You can't use this code to generate the answer to your course work
#
# You can write me in telegram about course work ― @tonitaga
# If not, please use the telegram bot or visit   ― @CalculatorlevlevBot

import math as m
from tabulate import tabulate
from .basecourseworkpart import BaseCourseWorkPart


class CourseWorkPartCutterCircle(BaseCourseWorkPart):
    """
    This class solving circle cutter, calculating all parts of course work

    The initializing data is dictionary, dictionary must have that keys for correct work:

    data = {
        'D1': float,  -> Первый диаметр

        'D2': float,  -> Второй диаметр

        'D3': float,  -> Третий диаметр

        'D4': float,  -> Четвертый диаметр

        'l1': float,  -> Первая длина

        'l2': float,  -> Вторая длина

        'l3': float,  -> Третья длина

        'L':  float,  -> Общая длина

        'f':  float   -> Размер фаски

        'R': float    -> Радиус
    }
    """

    def __init__(self, data: dict) -> None:
        self.data = data
        self.__output_str = str()
        self.__methods = [
            method for method in dir(CourseWorkPartCutterCircle)
                if callable(getattr(CourseWorkPartCutterCircle, method)) and
                    method.startswith("_CourseWorkPartCutterCircle__part")
        ]
        self.L = self.data['L']
        self.l1 = self.data['l1']
        self.l2 = self.data['l2']
        self.l3 = self.data['l3']
        self.f = self.data['f']
        self.D1 = self.data['D1']
        self.D2 = self.data['D2']
        self.D3 = self.data['D3']
        self.D4 = self.data['D4']
        self.R = self.data['R']

    def calculate_part(self) -> None:
        for i in range(0, len(self.__methods)):
            method_index = self.__methods.index(f"_CourseWorkPartCutterCircle__part_{i}")
            getattr(self, self.__methods[method_index])()

    def save_data(self, path: str) -> None:
        text_file = open(path, "w+", encoding="utf-8")
        text_file.write(self.__output_str)
        text_file.close()

    def __part_0(self):
        self.__output_str += f"\tПРОЕКТИРОВАНИЕ ФАСОННОГО РЕЗЦА\n"
        self.__output_str += f"\tИсходные данные\n"
        self.__output_str += f"Рассчитать и сконструировать круглый фасонный резец для наружного обтачивания детали, изготовляемой из стали.\n"
        self.__output_str += f"- D1 = {self.D1} мм\n- D2 = {self.D2} мм\n- D3 = {self.D3} мм\n- D4 = {self.D4} мм\n" + \
                             f"- l1 = {self.l1} мм\n- l2 = {self.l2} мм\n- l3 = {self.l3} мм\n- L = {self.L} мм\n" + \
                             f"- R = {self.R} мм\n- f = {self.f} мм\n"

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
        self.__output_str += "2)Расчет величины смещения h\n"
        self.h = round(self.R * m.sin(m.radians(self.alpha)), 2)
        self.__output_str += f"\th = R * sin(𝛼) = {self.R} * sin({self.alpha}) = {self.h} мм\n"

    def __part_3(self):
        self.__output_str += "3)Длина обрабатываемой поверхности круглым резцом\n"
        self.delta_work = self.L - (self.l1 + self.l2 + self.l3)
        self.__output_str += f"\tΔп = L - (l1 + l2 + l3) = {self.L} - ({self.l1} + {self.l2} + {self.l3}) = {self.delta_work} мм\n"

    def __part_4(self):
        self.__output_str += "4)Определение количества точек на участке (6-7)\n"
        self.step = 5
        self.section_count = round(self.delta_work / self.step, 2)
        if m.ceil(self.section_count) >= 7:
            self.step = 10
            self.section_count = round(self.delta_work / self.step, 2)
        self.__output_str += "Криволинейный участок 6-7 может быть разбит на сколько угодно малые отрезки 6-a, a-b, b-c и т.д.\n" + \
                             "Каждый отрезок можно считать образующей элементарного усеченного конуса.\n"
        self.__output_str += f"\tкол-во отвезков = Δп / {self.step} = {self.delta_work} / {self.step} = {self.section_count}\n"
        section_count_pred = int(self.section_count) + 0.4
        self.section_count = m.ceil(self.section_count) if self.section_count >= section_count_pred else m.floor(
            self.section_count)
        self.__output_str += f"\tПринимаем кол-во отрезков = {m.ceil(self.section_count)}\n"
        self.points_count = round(self.section_count - 1)
        self.__output_str += f"\tТогда i = кол-во отрезков - 1 = {self.points_count} точек\n"
        self.alphabit = "abcdefgjklmnop"
        self.__output_str += f"\tОтрезки: 6 - а"
        for i in range(1, self.points_count + 1):
            if i != self.points_count:
                self.__output_str += f", {self.alphabit[i - 1]} - {self.alphabit[i]}"
            else:
                self.__output_str += f", {self.alphabit[i - 1]} - 7\n"

    def __part_5(self):
        image = str()
        if self.points_count == 6:
            image = "\n   --------------------------------------------------------------------------------------------------------------------\n" + \
                    "            ║            ║             ║                ║                                                     ║ ║\n" * 9 + \
                    "            ║            ║             ║                ║                                              =======●_⁄\n" + \
                    "            ║            ║             ║                ║                                      =======●       7\n" + \
                    "            ║            ║             ║                ║                               ======●       f\n" + \
                    "            ║            ║             ║                ║                        =====●⁄      e\n" + \
                    "            ║            ║             ║                ║                   ==●=⁄     d\n" + \
                    "            ║            ●=============●                ║              ====⁄  c\n" + \
                    "            ║            ║3           4 \               ║          ===●\n" + \
                    "            ║            ║               \              ║      ===⁄   b\n" + \
                    "            ║            ║                \             ║   ==●\n" + \
                    "            ║            ║                 ●============●==⁄  a\n" + \
                    "            ●============●                 5            6\n" + \
                    "            1            2\n\n\n"
        elif self.points_count == 5:
            image = "\n   --------------------------------------------------------------------------------------------------------------------\n" + \
                    "            ║            ║             ║                ║                                                     ║ ║\n" * 9 + \
                    "            ║            ║             ║                ║                                              =======●_⁄\n" + \
                    "            ║            ║             ║                ║                                      ======●⁄       7\n" + \
                    "            ║            ║             ║                ║                               ====●=⁄      e\n" + \
                    "            ║            ║             ║                ║                        ==●===⁄    d\n" + \
                    "            ║            ║             ║                ║                   ====⁄  c\n" + \
                    "            ║            ●=============●                ║              ===●⁄\n" + \
                    "            ║            ║3           4 \               ║          ===⁄   b\n" + \
                    "            ║            ║               \              ║      ==●⁄\n" + \
                    "            ║            ║                \             ║   ==⁄  a\n" + \
                    "            ║            ║                 ●============●==⁄\n" + \
                    "            ●============●                 5            6\n" + \
                    "            1            2\n\n\n"
        elif self.points_count == 4:
            image = "\n   --------------------------------------------------------------------------------------------------------------------\n" + \
                    "            ║            ║             ║                ║                                                     ║ ║\n" * 9 + \
                    "            ║            ║             ║                ║                                              =======●_⁄\n" + \
                    "            ║            ║             ║                ║                                      ====●==⁄       7\n" + \
                    "            ║            ║             ║                ║                               ●=====⁄    d\n" + \
                    "            ║            ║             ║                ║                        ======⁄ c\n" + \
                    "            ║            ║             ║                ║                   =●==⁄\n" + \
                    "            ║            ●=============●                ║              ====⁄ b\n" + \
                    "            ║            ║3           4 \               ║          ===⁄\n" + \
                    "            ║            ║               \              ║      ===●\n" + \
                    "            ║            ║                \             ║   ==⁄   a\n" + \
                    "            ║            ║                 ●============●==⁄\n" + \
                    "            ●============●                 5            6\n" + \
                    "            1            2\n\n\n"
        elif self.points_count == 3:
            image = "\n   --------------------------------------------------------------------------------------------------------------------\n" + \
                    "            ║            ║             ║                ║                                                     ║ ║\n" * 9 + \
                    "            ║            ║             ║                ║                                              =======●_⁄\n" + \
                    "            ║            ║             ║                ║                                      ●======⁄       7\n" + \
                    "            ║            ║             ║                ║                               ======⁄ c\n" + \
                    "            ║            ║             ║                ║                        =●====⁄\n" + \
                    "            ║            ║             ║                ║                   ====⁄ b\n" + \
                    "            ║            ●=============●                ║              ====⁄\n" + \
                    "            ║            ║3           4 \               ║          =●=⁄\n" + \
                    "            ║            ║               \              ║      ===⁄ a\n" + \
                    "            ║            ║                \             ║   ==⁄\n" + \
                    "            ║            ║                 ●============●==⁄\n" + \
                    "            ●============●                 5            6\n" + \
                    "            1            2\n\n\n"
        elif self.points_count == 2:
            image = "\n   --------------------------------------------------------------------------------------------------------------------\n" + \
                    "            ║            ║             ║                ║                                                     ║ ║\n" * 9 + \
                    "            ║            ║             ║                ║                                              =======●_⁄\n" + \
                    "            ║            ║             ║                ║                                      =======⁄       7\n" + \
                    "            ║            ║             ║                ║                               ====●=⁄\n" + \
                    "            ║            ║             ║                ║                        ======⁄    b\n" + \
                    "            ║            ║             ║                ║                   ====⁄\n" + \
                    "            ║            ●=============●                ║              ==●=⁄\n" + \
                    "            ║            ║3           4 \               ║          ===⁄  a\n" + \
                    "            ║            ║               \              ║      ===⁄\n" + \
                    "            ║            ║                \             ║   ==⁄\n" + \
                    "            ║            ║                 ●============●==⁄\n" + \
                    "            ●============●                 5            6\n" + \
                    "            1            2\n\n\n"
        elif self.points_count == 1:
            image = "\n   --------------------------------------------------------------------------------------------------------------------\n" + \
                    "            ║            ║             ║                ║                                                     ║ ║\n" * 9 + \
                    "            ║            ║             ║                ║                                              =======●_⁄\n" + \
                    "            ║            ║             ║                ║                                      =======⁄       7\n" + \
                    "            ║            ║             ║                ║                               ======⁄\n" + \
                    "            ║            ║             ║                ║                        ==●===⁄\n" + \
                    "            ║            ║             ║                ║                   ====⁄  a\n" + \
                    "            ║            ●=============●                ║              ====⁄\n" + \
                    "            ║            ║3           4 \               ║          ===⁄\n" + \
                    "            ║            ║               \              ║      ===⁄\n" + \
                    "            ║            ║                \             ║   ==⁄\n" + \
                    "            ║            ║                 ●============●==⁄\n" + \
                    "            ●============●                 5            6\n" + \
                    "            1            2\n\n\n"
        self.__output_str += image

    def __part_6(self):
        self.__output_str += "5)Определение радиусов узловых точек профиля детали\n"
        self.__output_str += "По формуле определяем радиусы точек:\n"
        self.__output_str += "\t      ________________\n"
        self.__output_str += f"\tri = √(D / 2)² - (ih)²\n"
        self.__output_str += "где i - число шагов, h - шаг\n"
        self.radiuses = list()
        for i in range(1, self.points_count + 1):
            self.radiuses.append(round(m.sqrt(self.R ** 2 - (i * self.step) ** 2), 2))
            self.__output_str += "\t      ______________\n"
            self.__output_str += f"\tr{self.alphabit[self.points_count - i]} = √{self.R}² - ({i} * {self.step})² = {self.radiuses[i - 1]} мм\n"
        self.k0 = self.R + self.D4 / 2
        self.__output_str += f"\n\tk0 = R + D4 / 2 = {self.R} + {self.D4} / 2 = {self.k0} мм\n"
        self.radiuses_stroke = list()
        for i in range(1, self.points_count + 1):
            self.radiuses_stroke.append(round(self.k0 - self.radiuses[i - 1], 2))
            self.__output_str += f"\tr{self.alphabit[self.points_count - i]}' = k0 - r{self.alphabit[self.points_count - i]} = {self.k0} - {self.radiuses[i - 1]} = {self.radiuses_stroke[i - 1]} мм\n"
        r7 = self.D4 / 2
        r6 = r5 = self.D3 / 2
        r4 = r3 = self.D2 / 2
        r2 = r1 = self.D1 / 2
        self.__output_str += f"\tr7 = D4 / 2 = {self.D4} / 2 = {r7} мм,\n" + \
                             f"\tr5 = r6 = D3 / 2 = {self.D3} / 2 = {r5} мм,\n" + \
                             f"\tr3 = r4 = D2 / 2 = {self.D2} / 2 = {r3} мм,\n" + \
                             f"\tr1 = r2 = D1 / 2 = {self.D1} / 2 = {r1} мм\n"

        self.table_1 = [['  ', 1, 2, 3, 4, 5, 6],
                        ['ri', r1, r2, r3, r4, r5, r6],
                        ['li', 0, 0, 0, self.l1, self.l1 + self.l2, self.l1 + self.l2 + self.l3]]
        self.radiuses_stroke.reverse()
        for i in range(self.points_count):
            self.table_1[0].append(self.alphabit[i])
        self.table_1[0].append(7)
        for item in self.radiuses_stroke:
            self.table_1[1].append(item)
        self.table_1[1].append(r7)
        for i in range(self.points_count):
            self.table_1[2].append(self.L - (self.points_count - i) * self.step)
        self.table_1[2].append(self.L)

        self.__output_str += '\n' + tabulate(self.table_1, headers='firstrow', tablefmt='fancy_grid') + '\n\n'

    def __part_7(self):
        self.__output_str += "\tАлгоритмы расчета фасонных резцов\n\n"
        self.__output_str += "Профиль фасонного резца, как правило, не совпадает с профилем\n" + \
                             "обрабатываемой детали, что требует корректирование профиля резца.\n" + \
                             "Для этого определяют размеры осевого сечения для круглых фасонных резцов.\n" + \
                             "Корректирование профиля фасонных резцов проводится двумя способами:\n" + \
                             "\tграфическим и аналитическим.\n"
        self.__output_str += "Аналитический расчет фасонного резца заключается:\n" + \
                             "- В определении расстояния С по передней поверхности резца от точки с\n" + \
                             "минимальным радиусом детали до всех остальных опорных точек.\n"
        self.__output_str += "- В определении радиусов резца соответствующих опорным точкам детали.\n" + \
                             "Обозначим цифрами 1, 2 ... узловые точки заданного профиля.\n" + \
                             "Радиусы r1, r2 ... до узловых точек детали найдены выше.\n" + \
                             "Для расчета профиля круглых фасонных резцов необходимо определить\n" + \
                             "расстояние Сi по передней грани от 1-ой точки до точки 7.\n"

    def __part_8(self):
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

    def __part_9(self):
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
