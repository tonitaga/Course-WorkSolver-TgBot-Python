# Copyright (C) 2023 Gubaydullin Nurislam - All Rights Reserved
# You can't use this code to generate the answer to your course work
#
# You can write me in telegram about course work ― @tonitaga
# If not, prease use the telegram bot or visit   ― @CalculatorlevlevBot

import math as m
from . import tables as t
from .basecourseworkpart import BaseCourseWorkPart


class CourseWorkPartBroach(BaseCourseWorkPart):
    """
    This class solving broach, calculating all parts of course work

    The initializing data is dictionary, dictionary must have that keys for correct work:

    data = {
        'n':      int,    -> Количество зубьев

        'd':      float,  -> Внутренний диаметр

        'D':      float,  -> Наружний диаметр

        'b':      float,  -> Ширина

        'f':      float,  -> Фаска по внутреннему диаметру

        'Tf':     float,  -> Допуск на фаску

        'L':      float,  -> Длина протягивания

        'r':      float,  -> Радиус скругления

        'stanok': str     -> Тип станка
    }
    """

    def __init__(self, data: dict) -> None:
        self.Fk = None
        self.hk = None
        self.data = data
        self.__create_main_variant_params()
        self.__calculate_methods = [
            method for method in dir(CourseWorkPartBroach)
                if callable(getattr(CourseWorkPartBroach, method)) and
                   method.startswith('_CourseWorkPartBroach__part')
        ]
        self.__output_str = str()
        self.__current_part = 0

    def calculate_part(self) -> None:
        """
        The main function of the class, that calculating your broach with constracted data
        """
        for current in range(len(self.__calculate_methods)):
            method_index = self.__calculate_methods.index(f'_CourseWorkPartBroach__part_{current}')
            getattr(self, self.__calculate_methods[method_index])()
            self.__current_part += 1

    def save_data(self, path: str) -> None:
        """
        Function save solved variant data into file by path or creates file by path and writes the data
        """
        text_file = open(path, "w", encoding='utf-8')
        text_file.write(self.__output_str)
        text_file.close()

    def __part_0(self) -> None:
        """
        The main function that creating and initializing start variables to another functions
        """
        self.current_variant = t.table_deviation['variants'].index(f'{self.nz}x{self.d}x{self.D}x{self.b}x{self.f}x{self.Tf}x{self.r}')
        self.d_es = t.table_deviation['d_es'][self.current_variant]
        self.d_ei = 0
        self.D_ES = t.table_deviation['D_ES'][self.current_variant]
        self.D_EI = 0
        self.b_es = t.table_deviation['b_es'][self.current_variant]
        self.b_ei = t.table_deviation['b_ei'][self.current_variant]
        self.f_es = self.Tf
        self.f_ei = 0
        stanok_index = t.table_six['stanok'].index(self.stanok)
        self.Pc = t.table_six['P'][stanok_index] * 1000
        self.move_polzyn = t.table_six['move_polzyn'][stanok_index]
        greater = 'цельной, поскольку ее диаметр < 18' if self.d < 18 else 'сварной, поскольку ее диаметр ≥ 18 мм'
        self.__output_data_add(f'\t\tИсходные данные\n' +
                               f' ― Обозначение обрабатываемого отверстия: d – {self.nz}x{self.d}H7x{self.D}H12x{self.b}D9\n' +
                               f' ― Внутренний диаметр шлицевого отверстия d = {self.d} мм\n\tes = +{self.d_es} мм, ei = {self.d_ei} мм\n' +
                               f' ― Наружный диаметр шлицевого отверстия D = {self.D} мм\n\tES = +{self.D_ES} мм, EI = {self.D_EI} мм\n' +
                               f' ― Ширина шлица bш = {self.b} мм\n\tes = +{self.b_es} мм, ei = +{self.b_ei} мм\n' +
                               f' ― Число шлицев nz = {self.nz}\n' +
                               f' ― Размер фаски по внутреннему диаметру f = {self.f} мм\n\tes = +{self.f_es} мм, ei = {self.f_ei} мм\n' +
                               f' ― Длина протягивания L = {self.L} мм.\n' + f' ― Материал заготовки {self.steel}\n' + f' ― Станок модели {self.stanok}\n' +
                               f' ― Тяговая сила станка Рс = {self.Pc} Н\n' + f' ― Наибольший рабочий ход ползуна {self.move_polzyn} мм\n\n' +
                               f' ― Протяжку делаем {greater}.\n' +
                               f' ― Материал рабочей части ― быстрорежущая cталь Р6М5, материал хвостовика ― '
                               f'легированная cталь 40Х\n' + 
                               f' ― Длина протягивания L ≥ 30 мм, центрирование шлицевого соединения, в котором будет '
                               f'работать обрабатываемая деталь, осуществляется\n' + 
                               f'   по внутреннему диаметру, поэтому назначаем следующий порядок расположения зубьев '
                               f'протяжки по длине: фасочные, шлицевые, круглые (ФШК)\n\n') 
        
    def __part_1(self) -> None:
        """
        Независимо от схемы протяжки формулы остаются одинаковыми
        """
        delta_1 = round(0.005 * self.d + 0.1 * m.sqrt(self.L), 3)
        delta_2 = round(0.005 * self.d + 0.2 * m.sqrt(self.L), 3)
        self.delta = (delta_1 + delta_2) / 2
        if 1.0 > delta_1 and delta_2 > 1.0:
            self.delta = round(self.delta)
        else:
            self.delta = round(self.delta, 2)
        self.__output_data_add(f'\t\tОпределение диаметра отверстия в заготовке\n' +
                               f'{self.__current_part})Припуск под протягивание внутреннего диаметра равен:\n' +
                               f'\tΔ = 0.005 * d + (0.1 - 0.2) * √L = ({delta_1} - {delta_2}) мм\n' +
                               f'\tПринимаем Δ = {self.delta} мм\n')
        
    def __part_2(self) -> None:
        """
        Независимо от схемы протяжки формулы остаются одинаковыми
        """
        self.D01 = self.Dп = self.D1 = round(self.d - self.delta, 2)
        self.__output_data_add(f'{self.__current_part})Диаметры отверстий в заготовке D01, переднего направления в '
                               f'заготовке Dп и первого режущего зуба D1 равны:\n' + 
                               f'\tD01 = Dп = D1 = d - {self.delta} = {self.D01} мм\n')
        
    def __part_3(self) -> None:
        """
        Независимо от схемы протяжки формулы остаются одинаковыми
        """
        self.L1 = 280 + self.L
        self.__output_data_add(f'\n\t\tПроектирование гладких частей протяжки\n' +
                               f'{self.__current_part})Расстояние до первого зуба протяжки:\n\tL1 = 280 + L = {self.L1} мм\n') 
        
    def __part_4(self) -> None:
        """
        Независимо от схемы протяжки формулы остаются одинаковыми
        """
        d1_1 = self.D01 - 0.5
        d1_2 = self.D01 - 1.0
        self.d1 = m.floor((d1_1 + d1_2) / 2)
        if self.d1 > 100:
            self.d1 = 100
        elif self.d1 < 12:
            self.d1 = 12
        while self.d1 not in t.table_first['d1']:
            self.d1 -= 1
        index_d1 = t.table_first['d1'].index(self.d1)
        self.Fx = t.table_first['F'][index_d1]
        self.__output_data_add(f'{self.__current_part})Диаметр хвостовика, площадь хвостовика:\n' +
                               f'\td1 = D01 - (0.5 - 1.0)\n' +
                               f'\td1 = {self.D01} - (0.5 - 1.0) = ({d1_1} - {d1_2}) мм\n' +
                               f'Полученное значение d1 корректируют по стандартным значениям (табл.1) в меньшую '
                               f'сторону\n' +
                               f'Принимаем диаметр хвостовика d1 = {self.d1} мм\n' +
                               f'Тогда по табл.1 площадь хвостовика, определяющая его прочность Fх = {self.Fx} мм²\n')
        
    def __part_5(self) -> None:
        """
        Формула зависит от того принята ли групповая схема или одиночная схема
        """
        self.__output_data_add(f'\n\t\tОпределение параметров стружечной канавки\n' +
                               f'{self.__current_part})Шаг режущих зубьев tp:\n')
        if self.is_group:
            self.tp_space_find(1.45, 1.9)
        else:
            self.tp_space_find(1.25, 1.5)
            self.saved_tp = self.tp
            self.saved_hk = self.hk
            self.saved_Fk = self.Fk

    def __part_6(self) -> None:
        """
        Формула зависит от того принята ли групповая схема или одиночная схема
        """
        self.Zmax = round(self.L / self.tp + 1, 3)
        self.__output_data_add(f'{self.__current_part})Наибольшее число одновременно работающих зубьев:\n' +
                               f'\tZmax = (L / tp) + 1 = {self.L} / {self.tp} + 1 = {self.Zmax}\n' +
                               f'\tПринимаем Zmax = {round(self.Zmax)} зубьев\n')
        self.Zmax = round(self.Zmax)

    def __part_7(self) -> None:
        """
        Формула зависит от того принята ли групповая схема или одиночная схема
        """
        self.K = 4
        if self.is_group:
            self.K = 3
        text = 'так как одиночная схема' if self.K == 4 else 'так как групповая схема'
        self.__output_data_add(f'{self.__current_part})Коэффициент заполнения стружечной канавки:\n' +
                               f'\tК = {self.K}, {text}. (табл.3)\n')
        
    def __part_8(self) -> None:
        """
        Формула зависит от того принята ли групповая схема или одиночная схема
        """
        self.__output_data_add(f'{self.__current_part})Подача, допустимая по размещению стружки в канавке, равна:\n')
        if self.is_group:
            self.Sgk = round(self.Fk / (self.K * self.L), 3)
            self.__output_data_add(f'\tSгk= Fk / (K * L) = {self.Fk} / ({self.K} * {self.L}) = {self.Sgk} мм/группа\n')
            
        else:
            self.Szk = round(self.Fk / (self.K * self.L), 3)
            self.__output_data_add(f'\tSzk= Fk / (K * L) = {self.Fk} / ({self.K} * {self.L}) = {self.Szk} мм/зуб\n')
        
    def __part_9(self) -> None:
        """
        Независимо от схемы протяжки формулы остаются одинаковыми
        """
        self.sigma_x = t.table_five['sigma_x'][0]
        self.Px = round(self.Fx * self.sigma_x, 1)
        self.__output_data_add(f'{self.__current_part})Наибольшее усилие, допустимое хвостовиком, равно:\n' +
                               f'\tPx = Fx * σx = {self.Fx} * {self.sigma_x} = {self.Px} H\n')
    
    def __part_10(self) -> None:
        """
        Независимо от схемы протяжки формулы остаются одинаковыми
        """
        self.F1 = self.Fx
        self.sigma_1 = t.table_five['sigma_1'][3]
        self.P1 = round(round(m.pi, 2) * (self.D01 - 2 * self.hk) ** 2 * self.sigma_1 / 4, 2)
        self.__output_data_add(f'{self.__current_part})Наибольшее усилие, допустимое протяжкой на прочность по первому зубу, равно:\n' +
                               f'\tP1 = F1 * σ1 = π(D01 - 2hk)² * σ1 / 4 = {3.14} * ({self.D01} - 2 * {self.hk})² * {self.sigma_1} / 4 = {self.P1} H\n')

    def __part_11(self) -> None:
        """
        Независимо от схемы протяжки формулы остаются одинаковыми
        """
        tmp_Pc = self.Pc
        self.Pc = 0.9 * self.Pc
        self.Pp = min(self.P1, min(self.Px, self.Pc))
        self.__output_data_add(f'{self.__current_part})В качестве расчетной силы резания принимаем минимальное значение из следующего ряда сил:\n' +
                               f'\tP1 = {self.P1} H, Px = {self.Px} H, 0.9Pc = 0.9 * {tmp_Pc} = {self.Pc} H\n' +
                               f'\tПринимаем за Pp минимальное значение, следовательно, Pp = {self.Pp} H\n')
        self.Pc = tmp_Pc

    def __part_12(self) -> None:
        """
        Независимо от схемы протяжки формулы остаются одинаковыми
        """
        self.Bрф = round((self.b + 2 * self.f + 2 * self.Tf) * self.nz, 2)
        self.__output_data_add(f'\n\n\t\tРасчет фасочной части протяжки\n' +
                               f'{self.__current_part})Наибольшая ширина слоя, срезаемого фасочными зубьями протяжки структуры ФШК, равна:\n' +
                               f'\tBрф = (bш + 2f + 2Tf)nz = ({self.b} + 2 * {self.f} + 2 * {self.Tf}) * {self.nz} = {self.Bрф} мм\n')

    def __part_13(self) -> None:
        """
        Формула зависит от того принята ли групповая схема или одиночная схема
        """
        self.x = 0.8   # Константное значение для степени подачи
        self.Cp = 2170 # Значение должно зависеть от типа стали self.steel 
        self.n = 2     # Количество зубьев в группе в фасочной части протяжки - является константой
        self.Sg = self.Sgp = self.Szp = self.Sz = 0
        if self.is_group:
            self.Sgp = round(pow((self.Pp * self.n / (self.Bрф * self.Cp * self.Zmax)), 1 / self.x), 3)
            self.Sg = round(min(self.Sgk, self.Sgp), 3)
            self.__output_data_add(f'{self.__current_part})Подача, допустимая по силе резания, равна:\n' +
                                   f'\tПринимаем для фасочной части количество зубьев в группе n = {self.n}\n' +
                                   f'\tSгp = (Pp * n / (Bрф * Ср * Zmax))^(1/x) = ({self.Pp} * {self.n} / ({self.Bрф} * {self.Cp} * {self.Zmax}))^(1/{self.x}) = {self.Sgp} мм/группа\n' +
                                   f'\tПодача, допустимая по размещению стружки в канавке, расчитанная для групповой схемы, Sг = {self.Sgk} мм/группа\n' +
                                   f'\tРасчетное значение Sг = {self.Sg}\n' + 
                                   f'\tОкругляем до сотых, принимаем Sг = {round(self.Sg, 2)} мм/группа\n')
            self.Sg = round(self.Sg, 2)
        else:
            self.Szp = round(pow((self.Pp / (self.Bрф * self.Cp * self.Zmax)), 1 / self.x), 3)
            self.__output_data_add(f'{self.__current_part})По формуле (1.10) подача, допустимая по силе резания, равна:\n' +
                                   f'\tSzp = (Pp / (Bрф * Ср * Zmax))^(1/x) = ({self.Pp} / ({self.Bрф} * {self.Cp} * {self.Zmax}))^(1/{self.x}) = {self.Szp} мм/зуб\n')
            if self.Szp < self.Szk:
                self.__output_data_add(f'\tПоскольку Szp = {self.Szp} < Szk = {self.Szk} рассмотрим групповую схему для фасочной части\n' +
                                       f'\tСделаем перерасчет с 5 по 13 пункт\n\n' +
                                       f'\t _________________________________________________________________ \n' +
                                       f'\t|                                                                 |\n' +
                                       f'\t|               Перерасчет данных для фасочной части              |\n' + 
                                       f'\t|_________________________________________________________________|\n')
                self.is_group = True
                for current in range(5, 13 + 1):
                    self.__current_part += 1
                    method_index = self.__calculate_methods.index(f'_CourseWorkPartBroach__part_{current}')
                    getattr(self, self.__calculate_methods[method_index])()
            else:
                self.Sz = round(min(self.Szk, self.Szp), 3)
                self.__output_data_add(f'\tПоскольку Szp = {self.Szp} ≥ Szk = {self.Szk} (расчет Szk приведен в п.8), для фасочных зубьев принимаем одиночкую схему резания.\n' +
                                       f'\tПодача, допустимая по размещению стружки в канавке, расчитанная для одиночной схемы, Sz = {self.Szk} мм/зуб\n' +
                                       f'\tРасчетное значение Sz = {self.Sz}\n' +
                                       f'\tОкругляем до сотых, принимаем Sz = {round(self.Sz, 2)} мм/зуб\n')
                self.Sz = round(self.Sz, 2)

    def __part_14(self) -> None:
        """
        Независимо от схемы протяжки формулы остаются одинаковыми
        """
        self.dmin = self.d - self.d_ei
        self.delta_ф = round(self.dmin + 2 * (self.f + self.Tf) - self.D01, 2)
        self.__output_data_add(f'{self.__current_part})По формуле (1.21) припуск, снимаемый фасочными зубьями, равен:\n' +
                               f'\t∆ф = dmin + 2(f + Tf) - D01 = {self.dmin} + 2({self.f} + {self.Tf}) - {self.D01} = {self.delta_ф} мм\n')
        
    def __part_15(self) -> None:
        """
        Формула зависит от того принята ли групповая схема или одиночная схема
        """
        self.Zф = 0  # Количество зубьев в фасочной части
        if self.is_group:
            self.Zф = round((self.delta_ф / (2 * self.Sg)) * self.n + 1, 2)
            self.__output_data_add(f'{self.__current_part})По формуле (1.22) количество фасочных зубьев равно:\n' +
                                   f'\tZф = (∆ф / 2Sг) * n + 1 = ({self.delta_ф} / 2 * {self.Sg}) * {self.n} + 1 = {self.Zф}\n')
        else:
            self.Zф = round(self.delta_ф / (2 * self.Sz) + 1, 1)
            self.__output_data_add(f'{self.__current_part})По формуле (1.22) количество фасочных зубьев равно:\n' +
                                   f'\tZф = (∆ф / 2Sz) + 1 = ({self.delta_ф} / 2 * {self.Sz}) + 1 = {self.Zф}\n')
        self.Zф = m.ceil(self.Zф)
        self.__output_data_add(f'\tПринимаем Zф = {self.Zф} зубьев\n')

    def __part_16(self) -> None:
        """
        Независимо от схемы протяжки формулы остаются одинаковыми
        """
        self.Dфп = round(self.dmin + 2 * (self.f + self.Tf), 1)
        self.__output_data_add(f'{self.__current_part})Диаметр последнего фасочного зуба равен:\n' +
                               f'\tDфп = dmin + 2(f + Tf) = {self.dmin} + 2({self.f} + {self.Tf}) = {self.Dфп} мм\n')
        
    def __part_17(self) -> None:
        """
        Формула зависит от того принята ли групповая схема или одиночная схема
        """
        self.Dф_array = [self.D01]
        self.__output_data_add(f'{self.__current_part})Диаметры фасочных зубьев:\n')
        if self.is_group:
            self.groups_count = round(self.Zф / self.n, 2)
            current = 2
            self.__output_data_add(f'\tКоличество групп зубьев = Zф / n = {self.Zф} / {self.n} = {self.groups_count} групп\n' +
                                   f'\tТак как первый зуб диаметра D1 делается одинарным, округляем количество групп в меньшую сторону:\n' +
                                   f'\tКоличество групп зубьев = {m.floor(self.groups_count)} групп\n' +
                                   f'\tDфч1 = {self.Dф_array[0]}\n')
            self.groups_count = m.floor(self.groups_count)
            for group in range(1, self.groups_count + 1):
                self.__output_data_add(f'\t%2d группа: ' % (group))
                new_d = (self.Dф_array[current - 2] if group == 1 else self.Dф_array[current - 3]) + 2 * self.Sg
                if group == self.groups_count and self.Zф % 2 == 0:
                    self.Dф_array.append(round(new_d - 0.02, 2))
                    self.__output_data_add(f'Dфч{current} = {self.Dф_array[current - 1]}\t')
                    self.Zф += 1
                else:                    
                    for i in range(self.n):
                        if i != self.n - 1:
                            self.Dф_array.append(round(new_d, 2))
                        else:
                            self.Dф_array.append(round(new_d - 0.02, 2))
                        self.__output_data_add(f'Dфч{current} = {self.Dф_array[current - 1]}\t')
                        current += 1
                self.__output_data_add('\n')
            self.Zф -= 1    
        else:
            self.__output_data_add(f'\tDфч1 = {self.Dф_array[0]}\t')
            for i in range(2, self.Zф + 1):
                self.Dф_array.append(round(self.Dф_array[i - 2] + 2 * self.Sz, 2))
                self.__output_data_add(f'Dфч{i} = {self.Dф_array[i - 1]}\t')
                if i % 4 == 0:
                    self.__output_data_add('\n\t')
        self.__output_data_add(f'\n\tКалибрующих зубьев на фасочной части протяжки нет.\n')

    def __part_18(self) -> None:
        """
        Независимо от схемы протяжки формулы остаются одинаковыми
        """
        self.lраб_ф = round(self.tp * (self.Zф - 1))
        self.__output_data_add(f'{self.__current_part})Длина фасочной части протяжки:\n' +
                               f'\tlраб.ф = tp(Zф - 1) = {self.tp}({self.Zф} - 1) = {self.lраб_ф} мм\n')
        
    def __part_19(self) -> None:
        """
        Независимо от схемы протяжки формулы остаются одинаковыми
        """
        arcsin_degrees = m.degrees(m.asin(self.data['b'] / self.data['d']))
        self.beta_1 = round(45 - arcsin_degrees, 2)
        beta_1_radians = m.radians(self.beta_1)
        self.N = round(0.5 * m.sqrt(pow(self.data['d'] + 2 * self.f, 2) - pow(self.data['b'], 2)), 2)
        self.M = round(self.N * m.sin(beta_1_radians) + 0.5 * self.data['b'] * m.cos(beta_1_radians), 2)
        self.beta = round(360 / self.data['n'] + 2 * self.beta_1, 2)
        self.delta_h = 0.8  # Постоянное значение независимо от варианта
        self.P = round((round(m.pi, 2) * self.d) / self.nz - self.b - 2 * self.delta_h - 2 * self.f - 2 * self.Tf, 1)
        self.__output_data_add(f'{self.__current_part})Расчет размеров фасочных зубьев по формулам (1.31) – (1.35):\n' +
                               f'\tB1 = 45ͦ  - arcsin(bш / d) = 45ͦ  - arcsin({self.b} / {self.d}) = {self.beta_1}ͦ \n'+\
                               f'\tN = 0.5 * sqrt((d + 2f)^2 - bш^2) = 0.5 * sqrt(({self.d} + 2 * {self.f})^2 - {self.b}^2) = {self.N} мм\n'+
                               f'\tM = N * sinB1 + 0.5bш * cosB1 = {self.M} мм\n'+\
                               f'\tB = 360 / nz + 2B1 = 360 / {self.nz} + 2 * {self.beta_1} = {self.beta}ͦ \n'+\
                               f'\tP = pi * d / nz - bш - 2∆h - 2f - 2Tf = 3.14 * {self.d} / {self.nz} - {self.b} - 2 * {self.delta_h} - 2 * {self.f} - 2 * {self.Tf} = {self.P} мм\n')
        if self.P < 8:
            self.__output_data_add(f'Поскольку P < 8 мм, то поэтому стружкоразделительных канавок на фасочных зубьях нет.\n')
        else:
            self.__output_data_add(f'Поскольку P > 8 мм, на фасочной части есть стружкоразделнительные канавки.\n')
        self.is_group = False  # Если при расчете фасочной части было определено что схема групповая, нужно сделать одиночную схему снова, для расчета других частей

    def __part_20(self) -> None:
        """
        Независимо от схемы протяжки формулы остаются одинаковыми
        """
        self.Bрш = self.b * self.nz
        self.__output_data_add(f'\n\t\tРасчет шлицевой части протяжки\n' +
                               f'{self.__current_part})Наибольшая ширина слоя, срезаемого шлицевыми зубьями протяжки структуры ФШК, равна:\n' +
                               f'\tВрш = bш * nz = {self.b} * {self.nz} = {self.Bрш} мм\n')
        
    def __part_21(self) -> None:
        """
        Формула зависит от того принята ли групповая схема или одиночная схема
        """
        self.n = 2
        self.Zmax = self.__calulate_zmax_saved()
        self.Sg = self.Sgp = self.Szp = self.Sz = 0
        if self.is_group:
            self.Sgp = round(pow((self.Pp * self.n / (self.Bрш * self.Cp * self.Zmax)), 1 / self.x), 3)
            self.Sg = round(min(self.Sgk, self.Sgp), 3)
            self.__output_data_add(f'{self.__current_part})Подача, допустимая по силе резания, равна:\n' +
                                   f'\tПринимаем для шлицевой части количество зубьев в группе n = {self.n}\n' +
                                   f'\tSгp = (Pp * n / (Bрш * Ср * Zmax))^(1/x) = ({self.Pp} * {self.n} / ({self.Bрш} * {self.Cp} * {self.Zmax}))^(1/{self.x}) = {self.Sgp} мм/группа\n' +
                                   f'\tПодача, допустимая по размещению стружки в канавке, расчитанная для групповой схемы, Sг = {self.Sgk} мм/группа\n' +
                                   f'\tРасчетное значение Sг = {self.Sg}\n' + 
                                   f'\tОкругляем до сотых, принимаем Sг = {round(self.Sg, 2)} мм/группа\n')
            self.Sg = round(self.Sg, 2)
        else:
            self.Szp = round(pow((self.Pp / (self.Bрш * self.Cp * self.Zmax)), 1 / self.x), 3)
            self.__output_data_add(f'{self.__current_part})По формуле (1.10) подача, допустимая по силе резания, равна:\n' +
                                   f'\tSzp = (Pp / (Bрш * Ср * Zmax))^(1/x) = ({self.Pp} / ({self.Bрш} * {self.Cp} * {self.Zmax}))^(1/{self.x}) = {self.Szp} мм/зуб\n')
            if self.Szp < self.Szk:
                self.__output_data_add(f'\tПоскольку Szp = {self.Szp} < Szk = {self.Szk} рассмотрим групповую схему для шлицевой части\n' +
                                       f'\tСделаем перерасчет с 5 по 12 и с {self.__current_part - 1} по {self.__current_part} пункт\n\n' +
                                       f'\t _________________________________________________________________ \n' +
                                       f'\t|                                                                 |\n' +
                                       f'\t|               Перерасчет данных для шлицевой части              |\n' + 
                                       f'\t|_________________________________________________________________|\n')
                self.is_group = True
                for current in [5, 6, 7, 8, 9, 10, 11, 20, 21]:
                    self.__current_part += 1
                    method_index = self.__calculate_methods.index(f'_CourseWorkPartBroach__part_{current}')
                    getattr(self, self.__calculate_methods[method_index])()
            else:
                self.Sz = round(min(self.Szk, self.Szp), 3)
                self.__output_data_add(f'\tПоскольку Szp = {self.Szp} ≥ Szk = {self.Szk} (расчет Szk приведен в п.8), для шлицевых зубьев принимаем одиночкую схему резания.\n' +
                                       f'\tПодача, допустимая по размещению стружки в канавке, расчитанная для одиночной схемы, Sz = {self.Szk} мм/зуб\n' +
                                       f'\tРасчетное значение Sz = {self.Sz}\n' +
                                       f'\tОкругляем до сотых, принимаем Sz = {round(self.Sz, 2)} мм/зуб\n')
                self.Sz = round(self.Sz, 2)

    def __part_22(self) -> None:
        """
        Независимо от схемы протяжки формулы остаются одинаковыми
        """
        self.Dш1 = self.d + 2 * self.f
        self.__output_data_add(f'{self.__current_part})Диаметр первого шлицевого зуба равен:\n'+
                               f'\tDш1 = d + 2f = {self.d} + 2 * {self.f} = {self.Dш1} мм\n')
        
    def __part_23(self) -> None:
        """
        Независимо от схемы протяжки формулы остаются одинаковыми
        """
        self.Dmax = self.D + self.D_ES
        self.TD = self.D_ES - self.D_EI
        self.Dшпч = self.Dшк = round(self.Dmax - 0.3 * self.TD, 2)
        self.__output_data_add(f'{self.__current_part})Диаметр последнего чистового режущего шлицевого зуба равен диаметру калибрующих шлицевых зубьев и по выражению, аналогичному (1.27), равен:\n' +
                               f'\tDшпч = Dшк = Dmax - 0.3 * TD = {self.Dmax} - 0.3 * {self.TD} = {self.Dшпч} мм\n')
    
    def __part_24(self) -> None:
        """
        Формула зависит от того принята ли групповая схема или одиночная схема
        """
        if self.is_group:
            self.delta_шч = round(self.Dшпч - self.Dш1 - 2 * self.Sg, 3)
            self.__output_data_add(f'{self.__current_part})Припуск, снимаемый черновыми шлицевыми зубьями, равен:\n' +
                               f'\tΔшч = Dшпч - Dш1 - 2Sz = {self.Dшпч} - {self.Dш1} - 2 * {self.Sg} = {self.delta_шч} мм\n')
        else:
            self.delta_шч = round(self.Dшпч - self.Dш1 - 2 * self.Sz, 3)
            self.__output_data_add(f'{self.__current_part})Припуск, снимаемый черновыми шлицевыми зубьями, равен:\n' +
                               f'\tΔшч = Dшпч - Dш1 - 2Sz = {self.Dшпч} - {self.Dш1} - 2 * {self.Sz} = {self.delta_шч} мм\n')
            
    def __part_25(self) -> None:
        """
        Формула зависит от того принята ли групповая схема или одиночная схема
        """
        self.Zшч = 0  # Количество зубьев в шлицевой части
        if self.is_group:
            self.Zшч = round((self.delta_шч / (2 * self.Sg)) * self.n + 1, 2)
            self.__output_data_add(f'{self.__current_part})Число шлицевых черновых зубьев равно::\n' +
                                   f'\tZшч = (∆шч / 2Sг) * n + 1 = ({self.delta_шч} / 2 * {self.Sg}) * {self.n} + 1 = {self.Zшч}\n')
        else:
            self.Zшч = round(self.delta_шч / (2 * self.Sz) + 1, 2)
            self.__output_data_add(f'{self.__current_part})Число шлицевых черновых зубьев равно::\n' +
                                   f'\tZф = (∆шч / 2Sz) + 1 = ({self.delta_шч} / 2 * {self.Sz}) + 1 = {self.Zшч}\n')
        self.Zшч = m.floor(self.Zшч)
        self.__output_data_add(f'\tПри определении числа черновых режущих шлицевых зубьев\n' +
                               f'\tрезультат расчета округляется до целого числа в меньшую сторону.\n' +
                               f'\tПринимаем Zшч = {self.Zшч} зубьев\n')

    def __part_26(self) -> None:
        """
        Формула зависит от того принята ли групповая схема или одиночная схема
        """
        self.Dш_array = [self.Dш1]
        self.__output_data_add(f'{self.__current_part})Диаметры шлицевых зубьев:\n')
        if self.is_group:
            self.groups_count = round(self.Zшч / self.n, 2)
            current = 2
            self.__output_data_add(f'\tКоличество групп зубьев = Zшч / n = {self.Zшч} / {self.n} = {self.groups_count} групп\n' +
                                   f'\tТак как первый зуб диаметра D1 делается одинарным, округляем количество групп в меньшую сторону:\n' +
                                   f'\tКоличество групп зубьев = {m.floor(self.groups_count)} групп\n' +
                                   f'\tDшч1 = {self.Dш_array[0]}\n')
            self.groups_count = m.floor(self.groups_count)
            for group in range(1, self.groups_count + 1):
                self.__output_data_add(f'\t%2d группа: ' % (group))
                new_d = (self.Dш_array[current - 2] if group == 1 else self.Dш_array[current - 3]) + 2 * self.Sg
                if group == self.groups_count and self.Zшч % 2 == 0:
                    self.Dш_array.append(round(new_d - 0.02, 2))
                    self.__output_data_add(f'Dшч{current} = {self.Dш_array[current - 1]}\t')
                else:                    
                    for i in range(self.n):
                        if i != self.n - 1:
                            self.Dш_array.append(round(new_d, 2))
                        else:
                            self.Dш_array.append(round(new_d - 0.02, 2))
                        self.__output_data_add(f'Dшч{current} = {self.Dш_array[current - 1]}\t')
                        current += 1
                self.__output_data_add('\n')
        else:
            self.__output_data_add(f'\tDшч1 = {self.Dш_array[0]}\t')
            for i in range(2, self.Zшч + 1):
                self.Dш_array.append(round(self.Dш_array[i - 2] + 2 * self.Sz, 2))
                self.__output_data_add(f'Dф{i} = {self.Dш_array[i - 1]}\t')
                if i % 4 == 0:
                    self.__output_data_add('\n\t')
        self.__output_data_add('\n')

    def __part_27(self) -> None:
        """
        Независимо от схемы протяжки формулы остаются одинаковыми
        """
        self.delta_ш_перех = round(self.Dшпч - self.Dш_array[self.Zшч - 1], 2)
        self.__output_data_add(f'{self.__current_part})Уточняем диаметральный припуск на переходные зубья:\n' +
                               f'\tΔш.перех = Dшпч - Dш{self.Zшч} = {self.Dшпч} - {self.Dш_array[self.Zшч - 1]} = {self.delta_ш_перех} мм\n')
        
    def __part_28(self) -> None:
        """
        Формула зависит от того принята ли групповая схема или одиночная схема
        """
        if self.is_group:
            n_groups = 2
            self.n_perexod = self.n * n_groups  # Хз как правильно расчитывать для групповой схемы
            self.__output_data_add(f"{self.__current_part})Определяем подъемы на переходные группы и их диаметры:\n\tПринимаем {n_groups} переходных группы.\n")
            self.total_lift = round(self.delta_ш_перех / n_groups, 3)
            self.Sg = 0.6 * self.total_lift
            self.__output_data_add(f"\tСуммарный подъем на эти группы составляет {self.delta_ш_перех} / {n_groups} = {self.total_lift} мм.\n" +
                                   f"\tРаспределим его между группами. Первая получистовая группа Sg = 0.6 * {self.total_lift} = {self.Sg} мм/группа.\n" +
                                   f"\tПринимаем для него Sg = {round(self.Sg, 3)} мм/группа\n")
            self.Sg = round(self.Sg, 3)
            tmp_Sg = round(self.total_lift - self.Sg, 3)
            self.__output_data_add(f"\tТогда вторая чистовая группа снимет Sg = {self.total_lift} - {self.Sg} = {tmp_Sg} мм/группа\n")
            new_diametr_1 = round(self.Dш_array[self.Zшч - 1] + 2 * self.Sg, 3)
            new_diametr_2 = round(new_diametr_1 + 2 * tmp_Sg, 3)
            for _ in range(self.n):
                self.Dш_array.append(new_diametr_1)
            for _ in range(self.n):
                self.Dш_array.append(new_diametr_2)

            self.__output_data_add(f"\t{self.groups_count + 1} группа: Dш{self.Zшч + 1} = Dш{self.Zшч + 2} = {self.Dш_array[self.Zшч - 1]} + 2 * {self.Sg} = {new_diametr_1} мм\n")
            self.__output_data_add(f"\t{self.groups_count + 2} группа: Dш{self.Zшч + 3} = Dш{self.Zшч + 4} = {self.Dш_array[self.Zшч]} + 2 * {tmp_Sg} = {new_diametr_2} мм\n")
            self.Zшч_total = self.Zшч + self.n_perexod
            self.groups_count += n_groups
        else:
            self.n_perexod = 2
            self.__output_data_add(f"{self.__current_part})Определяем подъемы на переходные зубья и их диаметры:\n\tПринимаем {self.n_perexod} переходных зуба.\n")
            self.total_lift = round(self.delta_ш_перех / self.n_perexod, 3)
            self.Sz = 0.5 * self.total_lift
            self.__output_data_add(f"\tСуммарный подъем на эти зубья составляет {self.delta_ш_перех} / {self.n_perexod} = {self.total_lift} мм.\n" +
                                   f"\tРаспределим его между зубьями. Первый получистовой зуб Sz = 0.5 * {self.total_lift} = {self.Sz} мм/зуб.\n" +
                                   f"\tПринимаем для него Sz = {round(self.Sz, 3)} мм/зуб\n")
            self.Sz = round(self.Sz, 3)
            tmp_Sz = round(self.total_lift - self.Sz, 3)
            self.__output_data_add(f"\tТогда второй чистовой зуб снимет Sz = {self.total_lift} - {self.Sz} = {tmp_Sz} мм/зуб\n")
            self.Dш_array.append(round(self.Dш_array[self.Zшч - 1] + 2 * self.Sz, 3))
            self.Dш_array.append(round(self.Dш_array[self.Zшч] + 2 * tmp_Sz, 3))
            self.__output_data_add(f"\tDш{self.Zшч + 1} = {self.Dш_array[self.Zшч - 1]} + 2 * {self.Sz} = {self.Dш_array[self.Zшч]} мм\n")
            self.__output_data_add(f"\tDш{self.Zшч + 2} = {self.Dш_array[self.Zшч]} + 2 * {tmp_Sz} = {self.Dш_array[self.Zшч + 1]} мм\n")
            self.Zшч_total = self.Zшч + self.n_perexod

    def __part_29(self) -> None:
        """
        Формула зависит от того принята ли групповая схема или одиночная схема
        """
        if self.is_group:
            self.Zшк = 2
            self.tk = 0.75 * self.tp
            self.__output_data_add(f'{self.__current_part}) Калибрующие зубья:\n')
            self.__output_data_add(f"\tПо таблице 7 число калибрующих зубьев Zшк = {self.Zшк}\n" + 
                                   f"\tШаг между зубьями tк= 0,75tр = 0,75 * {self.tp} = {self.tk} мм\n" +
                                   f"\tПо таблице 2 выбираем hk = {self.hk} мм. Диаметры калибрующих зубьев равны:\n")
            self.Dш_array.append(self.Dшпч);
            self.Dш_array.append(self.Dшпч);
            self.__output_data_add(f"\tDш{self.Zшч_total + 1} = Dш{self.Zшч_total + 2} = {self.Dшпч} мм\n")
        else:
            self.Zшк = 2
            self.tk = 0.75 * self.saved_tp
            self.__output_data_add(f"{self.__current_part})По таблице 7 число калибрующих зубьев Zшк = {self.Zшк}\n" +
                                   f"\tШаг между зубьями tк= 0,75tр = 0,75 * {self.tp} = {self.tk} мм.\n" +
                                   f"\tПо таблице 2 выбираем hk = {self.hk} мм. Диаметры калибрующих зубьев равны:\n")
            self.Dш_array.append(self.Dшпч);
            self.Dш_array.append(self.Dшпч);
            self.__output_data_add(f"\tDш{self.Zшч_total + 1} = Dш{self.Zшч_total + 2} = {self.Dшпч} мм\n")

    def __part_30(self) -> None:
        """
        Независимо от схемы протяжки формулы остаются одинаковыми
        """
        self.lраб_ш = self.tp * (self.Zшч_total - 1) + self.tk * self.Zшк
        self.__output_str += f"{self.__current_part})Длина шлицевой части складывается из длин режущей и калибрующей частей:\n"+\
              f"\tlраб.ш = tp(Zp - 1) + tk*Zk = {self.tp}({self.Zшч_total} - 1) + {self.tk} * {self.Zшк} = {self.lраб_ш} мм\n"
        self.__output_str += "Подобно фасочным на шлицевых зубьях стружкоразделительные канавки отсутствуют.\n"
        self.is_group = False  # Если при расчете фасочной части было определено что схема групповая, нужно сделать одиночную схему снова, для расчета других частей

    def __part_31(self) -> None:
        """
        Независимо от схемы протяжки формулы остаются одинаковыми
        """
        self.Bрк = round(round(m.pi, 2) * self.d - (self.b + 2 * self.f + 2 * self.Tf) * self.nz, 2)
        self.__output_data_add(f'\n\t\tРасчет круглой части протяжки\n' +
                               f'{self.__current_part})Наибольшая ширина слоя, срезаемого круглыми зубьями протяжки структуры ФШК, равна:\n' +
                               f'\tBрк = pi * d - (bш + 2f + 2Tf) * nz = 3.14 * {self.d} - ({self.b} + 2 * {self.f} + 2 * {self.Tf}) * {self.nz} = {self.Bрк} мм\n')
        
    def __part_32(self) -> None:
        """
        Формула зависит от того принята ли групповая схема или одиночная схема
        """
        self.n = 2
        self.Zmax = self.__calulate_zmax_saved()
        self.Sg = self.Sgp = self.Szp = self.Sz = 0
        if self.is_group:
            self.Sgp = round(pow((self.Pp * self.n / (self.Bрк * self.Cp * self.Zmax)), 1 / self.x), 3)
            self.Sg = round(min(self.Sgk, self.Sgp), 3)
            self.__output_data_add(f'{self.__current_part})Подача, допустимая по силе резания, равна:\n' +
                                   f'\tПринимаем для круглой части количество зубьев в группе n = {self.n}\n' +
                                   f'\tSгp = (Pp * n / (Bрк * Ср * Zmax))^(1/x) = ({self.Pp} * {self.n} / ({self.Bрк} * {self.Cp} * {self.Zmax}))^(1/{self.x}) = {self.Sgp} мм/группа\n' +
                                   f'\tПодача, допустимая по размещению стружки в канавке, расчитанная для групповой схемы, Sг = {self.Sgk} мм/группа\n' +
                                   f'\tРасчетное значение Sг = {self.Sg}\n' + 
                                   f'\tОкругляем до сотых, принимаем Sг = {round(self.Sg, 2)} мм/группа\n')
            self.Sg = round(self.Sg, 2)
        else:
            self.Szp = round(pow((self.Pp / (self.Bрк * self.Cp * self.Zmax)), 1 / self.x), 3)
            self.__output_data_add(f'{self.__current_part})По формуле (1.10) подача, допустимая по силе резания, равна:\n' +
                                   f'\tSzp = (Pp / (Bрк * Ср * Zmax))^(1/x) = ({self.Pp} / ({self.Bрк} * {self.Cp} * {self.Zmax}))^(1/{self.x}) = {self.Szp} мм/зуб\n')
            if self.Szp < self.Szk:
                self.__output_data_add(f'\tПоскольку Szp = {self.Szp} < Szk = {self.Szk} рассмотрим групповую схему для круглой части\n' +
                                       f'\tСделаем перерасчет с 5 по 12 и с {self.__current_part - 1} по {self.__current_part} пункт\n\n' +
                                       f'\t _________________________________________________________________ \n' +
                                       f'\t|                                                                 |\n' +
                                       f'\t|               Перерасчет данных для круглой части               |\n' + 
                                       f'\t|_________________________________________________________________|\n')
                self.is_group = True
                for current in [5, 6, 7, 8, 9, 10, 11, 31, 32]:
                    self.__current_part += 1
                    method_index = self.__calculate_methods.index(f'_CourseWorkPartBroach__part_{current}')
                    getattr(self, self.__calculate_methods[method_index])()
            else:
                self.Sz = round(min(self.Szk, self.Szp), 3)
                self.__output_data_add(f'\tПоскольку Szp = {self.Szp} ≥ Szk = {self.Szk} (расчет Szk приведен в п.8), для круглых зубьев принимаем одиночкую схему резания.\n' +
                                       f'\tПодача, допустимая по размещению стружки в канавке, расчитанная для одиночной схемы, Sz = {self.Szk} мм/зуб\n' +
                                       f'\tРасчетное значение Sz = {self.Sz}\n' +
                                       f'\tОкругляем до сотых, принимаем Sz = {round(self.Sz, 2)} мм/зуб\n')
                self.Sz = round(self.Sz, 2)

    def __part_33(self) -> None:
        """
        Независимо от схемы протяжки формулы остаются одинаковыми
        """
        self.dmax = self.d + self.d_es
        self.Td = self.d_es - self.d_ei
        self.Dкпч = Dкк = round(self.dmax - 0.3 * self.Td, 2)
        self.__output_data_add(f"{self.__current_part})Диаметр последнего чистового режущего круглого зуба равен диаметру калибрующих круглых зубьев:\n" +
                               f"\tDкпч = Dкк = dmax - 0.3Td = {self.dmax} - 0.3 * {self.Td} = {self.Dкпч} мм\n")

    def __part_34(self) -> None:
        """
        Формула зависит от того принята ли групповая схема или одиночная схема
        """
        if self.is_group:
            self.delta_кч = round(self.Dкпч - self.D01 - 2 * self.Sg, 3)
            self.__output_data_add(f"{self.__current_part})Припуск, снимаемый черновыми режущими зубьями, равен:\n" +
                                   f"\t∆кч = Dкпч - D01 - 2Sg = {self.Dкпч} - {self.D01} - 2 * {self.Sg} = {self.delta_кч} мм\n")
        else:
            self.delta_кч = round(self.Dкпч - self.D01 - 2 * self.Sz, 3)
            self.__output_data_add(f"{self.__current_part})Припуск, снимаемый черновыми режущими зубьями, равен:\n" +
                                   f"\t∆кч = Dкпч - D01 - 2Sz = {self.Dкпч} - {self.D01} - 2 * {self.Sz} = {self.delta_кч} мм\n")

    def __part_35(self) -> None:
        """
        Формула зависит от того принята ли групповая схема или одиночная схема
        """
        self.Zкч = 0  # Количество зубьев в круглой части
        if self.is_group:
            self.Zкч = round((self.delta_кч / (2 * self.Sg)) * self.n + 1, 2)
            self.__output_data_add(f'{self.__current_part})Число шлицевых черновых зубьев равно::\n' +
                                   f'\tZкч = (∆кч / 2Sг) * n + 1 = ({self.delta_кч} / 2 * {self.Sg}) * {self.n} + 1 = {self.Zкч}\n')
        else:
            self.Zкч = round(self.delta_кч / (2 * self.Sz) + 1, 2)
            self.__output_data_add(f'{self.__current_part})Число шлицевых черновых зубьев равно::\n' +
                                   f'\tZкч = (∆кч / 2Sz) + 1 = ({self.delta_кч} / 2 * {self.Sz}) + 1 = {self.Zкч}\n')
        self.Zкч = m.floor(self.Zкч)
        self.__output_data_add(f'\tПри определении числа черновых режущих круглых зубьев\n' +
                               f'\tрезультат расчета округляется до целого числа в меньшую сторону.\n' +
                               f'\tПринимаем Zкч = {self.Zкч} зубьев\n')
        
    def __part_36(self) -> None:
        """
        Формула зависит от того принята ли групповая схема или одиночная схема
        """
        self.Dк_array = [self.D01]
        self.__output_data_add(f'{self.__current_part})Диаметры круглых зубьев:\n')
        if self.is_group:
            self.groups_count = round(self.Zкч / self.n, 2)
            current = 2
            self.__output_data_add(f'\tКоличество групп зубьев = Zкч / n = {self.Zкч} / {self.n} = {self.groups_count} групп\n' +
                                   f'\tТак как первый зуб диаметра D1 делается одинарным, округляем количество групп в меньшую сторону:\n' +
                                   f'\tКоличество групп зубьев = {m.floor(self.groups_count)} групп\n' +
                                   f'\tDкч1 = {self.Dк_array[0]}\n')
            self.groups_count = m.floor(self.groups_count)
            for group in range(1, self.groups_count + 1):
                self.__output_data_add(f'\t%2d группа: ' % (group))
                new_d = (self.Dк_array[current - 2] if group == 1 else self.Dк_array[current - 3]) + 2 * self.Sg
                if group == self.groups_count and self.Zкч % 2 == 0:
                    self.Dк_array.append(round(new_d - 0.02, 2))
                    self.__output_data_add(f'Dкч{current} = {self.Dк_array[current - 1]}\t')
                else:                    
                    for i in range(self.n):
                        if i != self.n - 1:
                            self.Dк_array.append(round(new_d, 2))
                        else:
                            self.Dк_array.append(round(new_d - 0.02, 2))
                        self.__output_data_add(f'Dкч{current} = {self.Dк_array[current - 1]}\t')
                        current += 1
                self.__output_data_add('\n')
        else:
            self.__output_data_add(f'\tDкч1 = {self.Dк_array[0]}\t')
            for i in range(2, self.Zкч + 1):
                self.Dк_array.append(round(self.Dк_array[i - 2] + 2 * self.Sz, 2))
                self.__output_data_add(f'Dкч{i} = {self.Dк_array[i - 1]}\t')
                if i % 4 == 0:
                    self.__output_data_add('\n\t')
        self.__output_data_add('\n')

    def __part_37(self) -> None:
        """
        Независимо от схемы протяжки формулы остаются одинаковыми
        """
        self.delta_к_перех = round(self.Dкпч - self.Dк_array[self.Zкч - 1], 2)
        self.__output_data_add(f"{self.__current_part})Уточняем диаметральный припуск на переходные зубья:\n" +
                               f"\tΔк.перех = Dкпч - Dк{self.Zкч} = {self.Dкпч} - {self.Dк_array[self.Zкч - 1]} = {self.delta_к_перех} мм\n")
        
    def __part_38(self) -> None:
        if self.is_group:
            n_groups = 2
            self.n_perexod = self.n * n_groups  # Хз как правильно расчитывать для групповой схемы
            self.__output_data_add(f"{self.__current_part})Определяем подъемы на переходные группы и их диаметры:\n\tПринимаем {n_groups} переходных группы.\n")
            self.total_lift = round(self.delta_к_перех / n_groups, 3)
            self.Sg = 0.6 * self.total_lift
            self.__output_data_add(f"\tСуммарный подъем на эти группы составляет {self.delta_к_перех} / {n_groups} = {self.total_lift} мм.\n" +
                                   f"\tРаспределим его между группами. Первая получистовая группа Sg = 0.6 * {self.total_lift} = {self.Sg} мм/группа.\n" +
                                   f"\tПринимаем для него Sg = {round(self.Sg, 3)} мм/группа\n")
            self.Sg = round(self.Sg, 3)
            tmp_Sg = round(self.total_lift - self.Sg, 3)
            self.__output_data_add(f"\tТогда вторая чистовая группа снимет Sg = {self.total_lift} - {self.Sg} = {tmp_Sg} мм/группа\n")
            new_diametr_1 = round(self.Dк_array[self.Zкч - 1] + 2 * self.Sg, 3)
            new_diametr_2 = round(new_diametr_1 + 2 * tmp_Sg, 3)
            for _ in range(self.n):
                self.Dк_array.append(new_diametr_1)
            for _ in range(self.n):
                self.Dк_array.append(new_diametr_2)

            self.__output_data_add(f"\t{self.groups_count + 1} группа: Dк{self.Zкч + 1} = Dк{self.Zкч + 2} = {self.Dк_array[self.Zкч - 1]} + 2 * {self.Sg} = {new_diametr_1} мм\n")
            self.__output_data_add(f"\t{self.groups_count + 2} группа: Dк{self.Zкч + 3} = Dш{self.Zкч + 4} = {self.Dк_array[self.Zкч]} + 2 * {tmp_Sg} = {new_diametr_2} мм\n")
            self.Zкч_total = self.Zкч + self.n_perexod
            self.groups_count += n_groups
        else:
            self.n_perexod = 3
            self.__output_data_add(f"{self.__current_part})Определяем подъемы на переходные зубья и их диаметры: Принимаем {self.n_perexod} переходных зуба.\n")
            self.total_lift = round(self.delta_к_перех / 2, 3)
            self.Sz = 0.5 * self.total_lift

            self.Sz = round(self.Sz, 3)
            sz_2 = round(0.3 * self.total_lift, 3)
            sz_3 = round(self.total_lift - self.Sz - sz_2, 3)
            self.__output_data_add(f"\tСуммарный подъем на эти зубья составляет {self.delta_к_перех} / 2 = {self.total_lift} мм.\n" +
                                   f"\tРаспределим его между зубьями. Первый получистовой зуб Sz = 0.5 * {self.total_lift} = {self.Sz} мм/зуб.\n" +
                                   f'\tПринимаем для него Sz = {round(self.Sz, 3)} мм/зуб\n' +
                                   f'\tВторой чистовой зуб снимет Sz = 0.3 * {self.total_lift} = {sz_2} мм/зуб\n' +
                                   f'\tТретий чистовой зуб снимет Sz = {self.total_lift} - {self.Sz} - {sz_2} = {sz_3} мм/зуб\n')
            Dk_sz_1 = round(self.Dк_array[self.Zкч - 1] + 2 * self.Sz, 3)
            Dk_sz_2 = round(Dk_sz_1 + 2 * sz_2, 3)
            Dk_sz_3 = round(Dk_sz_2 + 2 * sz_3, 3)
            self.__output_data_add(f"\tDк{self.Zкч + 1} = {self.Dк_array[self.Zкч - 1]} + 2 * {self.Sz} = {Dk_sz_1} мм\n" +
                                   f'\tDк{self.Zкч + 2} = {Dk_sz_1} + 2 * {sz_2} = {Dk_sz_2} мм\n' +
                                   f'\tDк{self.Zкч + 3} = {Dk_sz_2} + 2 * {sz_3} = {Dk_sz_3} мм\n')
            self.Zкч_total = self.Zкч + self.n_perexod

    def __part_39(self) -> None:
        if self.is_group:
            self.Zkk = 2
            self.tk = 0.75 * self.tp
            self.__output_data_add(f'{self.__current_part}) Калибрующие зубья:\n')
            self.__output_data_add(f"\tПо таблице 7 число калибрующих зубьев Zкк = {self.Zkk}\n" + 
                                   f"\tШаг между зубьями tк= 0,75tр = 0,75 * {self.tp} = {self.tk} мм\n" +
                                   f"\tПо таблице 2 выбираем hk = {self.hk} мм. Диаметры калибрующих зубьев равны:\n")
            self.Dк_array.append(self.Dкпч);
            self.Dк_array.append(self.Dкпч);
            self.__output_data_add(f"\tDш{self.Zкч_total + 1} = Dш{self.Zкч_total + 2} = {self.Dкпч} мм\n")
        else:
            self.Zkk = 7
            self.__output_data_add(f"{self.__current_part})По табл. 7 количество калибрующих зубьев Zкк=7. Диаметры калибрующих зубьев равны:\n" +
                                   f"\tDк{self.Zкч_total + 1} = ... = Dк{self.Zкч_total + self.Zkk} = {self.Dкпч} мм\n" +
                                   f"\tШаг между ними tк = 0,75tр = 0,75 * {self.tp} = {self.tk} мм. По таблице 2 выбираем hk = {self.hk} мм\n")
    
    def __part_40(self) -> None:
        self.lраб_к = self.tp * (self.Zкч_total - 1) + self.tk * self.Zkk
        self.__output_data_add(f"{self.__current_part})Длина круглой части протяжки:\n" +
                               f"\tlраб.к = tp * (Zкч - 1) + tk * Zкк = {self.tp} * ({self.Zкч_total} - 1) + {self.tk} * {self.Zkk} = {self.lраб_к} мм\n")
        
    def __part_41(self) -> None:
        self.__output_data_add(f"{self.__current_part})Определим необходимость стружкоразделительных канавок на режущих зубьях.\n")
        if self.is_group:
            self.b = round(1.7 * m.sqrt(self.d), 2)
            self.__output_data_add(f"По табл. 8 находим при Sг = {self.Sg} мм/группа и hk = {self.hk} мм, близким к нашим значениям,\n" +
                                   f"ширина режущей кромки, при которой стружка свертывается в спиральный валик, равна:\n" +
                                   f"\tb = 1.7√d = 1.7 * √{self.d} = {self.b} мм\n")
            self.bk = round(self.Bрк / self.nz, 2)
            self.__output_data_add(f"В рассматриваемом случае ширина режущей кромки круглого зуба равна расстоянию между шлицами:\n" +
                                   f"\tbк = Bрк / nz = {self.Bрк} / {self.nz} = {self.bk} мм.\n")
            need = ["bк < b", "не нужны"] if self.bk < self.b else ["bк > b", "нужны"]
            self.__output_data_add(f"Поскольку {need[0]}, то стружкоразделительные канавки {need[1]}.\n")
        else:
            self.b = round(1.7 * m.sqrt(self.d), 2)
            self.__output_data_add(f"По табл. 8 находим при Sz = {self.Sz} мм/зуб и hk = {self.hk} мм, близким к нашим значениям,\n" +
                                   f"ширина режущей кромки, при которой стружка свертывается в спиральный валик, равна:\n" +
                                   f"\tb = 1.7√d = 1.7 * √{self.d} = {self.b} мм\n")
            self.bk = round(self.Bрк / self.nz, 2)
            self.__output_data_add(f"В рассматриваемом случае ширина режущей кромки круглого зуба равна расстоянию между шлицами:\n" +
                                   f"\tbк = Bрк / nz = {self.Bрк} / {self.nz} = {self.bk} мм.\n")
            need = ["bк < b", "не нужны"] if self.bk < self.b else ["bк > b", "нужны"]
            self.__output_data_add(f"Поскольку {need[0]}, то стружкоразделительные канавки {need[1]}.\n")

    def __part_42(self) -> None:
        self.lкн = round(0.75 * self.L, 2)
        self.__output_data_add(f"{self.__current_part})Длина заднего направления протяжки lкн = 0,75L = 0.75 * {self.data['L']} = {self.lкн} мм\n")

    def __part_43(self):
        self.Lпр = self.L1 + self.lраб_к + self.lраб_ф + self.lраб_ш + 3 * 1.5 * self.tp + self.lкн
        self.__output_data_add(f"{self.__current_part})По выражению (1.29) общая длина протяжки равна:\n" +
                               f"\tLпр = L1 + lраб.к + lраб.ф + lраб.ш + 3 * 1.5tp + lкн = {self.L1} + {self.lраб_к} + {self.lраб_ф} + {self.lраб_ш} + 3 * 1.5 * {self.tp} + {self.lкн} = {self.Lпр} мм\n")
        lenght_tmp = self.Lпр
        lenght_tmp_floor = m.floor(lenght_tmp)
        while lenght_tmp_floor % 10 != 0:
            lenght_tmp_floor += 1
        self.Lпр = lenght_tmp_floor
        difference = self.Lпр - lenght_tmp
        if difference != 0:
            self.__output_data_add(f"\tПринимаем Lпр = {self.Lпр} мм\n" +
                                   f"\tПри этом длину заднего направления увеличим до {self.lкн + difference} мм.\n")
            self.lкн += difference

    def __part_44(self):
        self.Lпр_max = 40 * self.D
        greater = "> 2000 мм" if self.Lпр_max > 2000 else "< 2000 мм"
        self.__output_data_add(f"{self.__current_part})Допустимая длина протяжки:\n" +
                               f"\tLпр.max = 40 * D = 40 * {self.D} = {self.Lпр_max} мм {greater}\n")
        if greater[0] == '>':
            self.__output_data_add(f"Принимаем Lпр.max = 2000 мм\n")
            self.Lпр_max = 2000

    def __part_45(self):
        self.lp_x = self.L + self.lраб_к + self.lраб_ф + self.lраб_ш + 3 * 1.5 * self.tp
        self.__output_data_add(f"{self.__current_part})Необходимая длина рабочего хода при протягивании:\n" +
                               f"\tlp.x = L + lраб.к + lраб.ф + lраб.ш + 3 * 1.5tp = {self.L} + {self.lраб_к} + {self.lраб_ф} + {self.lраб_ш} + 3 * 1.5 * {self.tp} = {self.lp_x} мм\n")
        if self.lp_x > self.Lпр_max:
            self.__output_data_add(f'\tПри длине рабочего хода lp.x = {self.lp_x} мм, нет станка удовлетворяющего этой длине\n' +
                                   f'\tНеободимо изготовить комплект протяжек.\n')
        else:
            if self.lp_x < self.move_polzyn:
                self.__output_data_add(f'\tДлина lp.x меньше наибольшего рабочего хода станка {self.stanok} мм\n' + 
                                       f'\tСледовательно, нет необходимости изготавливать комплект протяжек\n')
            else:
                self.__output_data_add(f'\tДлина lp.x больше наибольшего рабочего хода ползуна станка {self.stanok},\n' +
                                       f'\tоднако меньше чем максимальная длина протяжки Lпр.max = {self.Lпр_max} мм\n' + 
                                       f'\tСледовательно, можно взять другой станок, например:\n')
                tmp_lpx = round(self.lp_x)
                while tmp_lpx not in t.table_six['move_polzyn']:
                    tmp_lpx += 1
                current = t.table_six['move_polzyn'].index(tmp_lpx)
                stanok = t.table_six['stanok'][current]
                move_polzyn = t.table_six['move_polzyn'][current]
                self.__output_data_add(f'\tПринимаем станок {stanok} с наибольшим ходом ползуна = {move_polzyn} мм\n')

    def __part_46(self):
        self.__output_data_add(f"{self.__current_part})Передний угол на всех режущих и калибрующих зубьях γр=γк=12ͦ, задний угол на режущих зубьях αр=3ͦ, на калибрующих зубьях αк=1ͦ \n")

    def __create_main_variant_params(self) -> None:
        self.nz = self.data['n']
        self.d  = self.data['d']
        self.D  = self.data['D']
        self.b  = self.data['b']
        self.f  = self.data['f']
        self.Tf = self.data['Tf']
        self.L  = self.data['L']
        self.r  = self.data['r']
        self.stanok = self.data['stanok']
        self.steel = 'Сталь 40'
        self.L = 30 if self.L < 30 else self.L
        self.is_group = False

    def __output_data_add(self, info: str) -> None:
        self.__output_str += info

    def tp_space_find(self, left: float, right: float) -> None:
        tp_1 = round(left * m.sqrt(self.L), 2)
        tp_2 = round(right * m.sqrt(self.L), 2)
        self.tp = round((tp_1 + tp_2) / 2)

        if self.tp < 4.5:
            self.tp = 4.5
        elif self.tp % 2 != 0:
            if self.tp + 1 > tp_2:
                self.tp -= 1
            else:
                self.tp += 1

        for i in range(len(t.table_second['tp'])):
            if t.table_second['tp'][i] == self.tp:
                self.hk = t.table_second['hx'][i]
                self.Fk = t.table_second['Fk'][i]
                break
        
        if self.is_group:
            if 8 > tp_1 and 8 < tp_2:
                self.tp = 8
        self.__output_data_add(f'\ttp = ({left} - {right}) * √L = ({left} - {right}) * √{self.L} = ({tp_1} - {tp_2}) мм\n' +
                               f'\tПринимаем tp = {self.tp} мм; hк = {self.hk} мм; Fк = {self.Fk} мм²(табл.2)\n')

    def __calulate_zmax_saved(self) -> float:
        return round(self.L / self.saved_tp + 1)
    