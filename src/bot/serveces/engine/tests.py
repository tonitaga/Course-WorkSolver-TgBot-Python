# Copyright (C) 2023 Gubaydullin Nurislam - All Rights Reserved
# You can't use this code to generate the answer to your course work
#
# You can write me in telegram about course work ― @tonitaga
# If not, prease use the telegram bot or visit   ― @CalculatorlevlevBot

from .courseworkmanager import *

from . import tables as t


def test_cutter_circle():
    """Тест работоспособности класса CourseWorkPartCutterCircle по всем вариантам"""

    D1 = [20, 22, 25, 28, 30, 32, 35, 38, 40, 42, 45, 50, 52, 55, 60]
    D2 = [16, 16, 20, 23, 22, 25, 30, 32, 32, 35, 35, 45, 45, 48, 45]
    D3 = [18, 18, 22, 25, 25, 27, 32, 34, 36, 37, 38, 50, 48, 52, 50]
    D4 = [10, 12, 10, 16, 12, 15, 17, 22, 20, 20, 26, 28, 38, 42, 30]
    R = [15, 22, 20, 25, 20, 15, 35, 30, 25, 40, 30, 25, 40, 45, 50]
    l1 = [3, 3, 3, 4, 3, 4, 3, 3, 4, 5, 4.5, 5.5, 6, 7, 8]
    l2 = [1, 2, 1, 1, 1.5, 2, 1, 1, 2, 1, 1.5, 2.5, 1.5, 2, 2.5]
    l3 = [5, 8, 8, 10, 15, 12, 9, 16, 14, 14, 20, 24, 22.5, 26, 20]
    L = [20, 25, 25, 30, 35, 30, 35, 40, 40, 45, 45, 50, 50, 55, 60]
    f = [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 1, 1, 1, 1, 1, 1, 1]
    i = 1
    for _ in D1:
        data = {
            "object_type": "Резец - Круглый",
            "D1": D1[i - 1],
            "D2": D2[i - 1],
            "D3": D3[i - 1],
            "D4": D4[i - 1],
            "l1": l1[i - 1],
            "l2": l2[i - 1],
            "l3": l3[i - 1],
            "L": L[i - 1],
            "f": f[i - 1],
            "R": R[i - 1]
        }
        manager = CourseWorkPartSolverManager()
        if data['object_type'] == "Резец - Круглый":
            manager.set_course_part(CourseWorkPartCutterCircle(data=data))
            manager.calculate_part()
            manager.save_data(f"./cutter_circle/solved_variant{i}.txt")
        i += 1
    print("===TEST_CUTTER_CIRCLE_FIINSHED===")


def test_cutter_prismatic():
    """Тест работоспособности класса CourseWorkPartCutterPrismatic по всем вариантам"""

    D = [30, 40, 32, 40, 40, 42, 60, 50, 54, 50, 55, 58, 60, 60, 60, 62]
    D1 = [35, 35, 40, 40, 45, 45, 50, 50, 55, 56, 60, 60, 62, 65, 70, 72]
    l1 = [3, 6, 5, 6, 5, 3, 10, 5, 6, 5, 4, 6, 5, 5, 10, 10]
    l2 = [10, 15, 15, 20, 20, 18, 30, 25, 24, 22, 25, 27, 25, 28, 30, 30]
    l3 = [20, 28, 27, 30, 35, 33, 45, 46, 40, 43, 42, 45, 42, 52, 50, 55]
    L = [25, 32, 35, 35, 40, 40, 50, 50, 50, 50, 52, 55, 56, 60, 60, 65]
    f = [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 1, 0.5, 1, 1, 1, 1, 1, 1, 1, 1]
    i = 1
    for _ in D:
        data = {
            "object_type": "Резец - Призматический",
            "D": D[i - 1],
            "D1": D1[i - 1],
            "l1": l1[i - 1],
            "l2": l2[i - 1],
            "l3": l3[i - 1],
            "L": L[i - 1],
            "f": f[i - 1],
        }
        manager = CourseWorkPartSolverManager()
        if data['object_type'] == "Резец - Призматический":
            manager.set_course_part(CourseWorkPartCutterPrismatic(data=data))
            manager.calculate_part()
            manager.save_data(f"./cutter_prismatic/solved_variant_{i}.txt")
        i += 1
    print("===TEST_CUTTER_PRISMATIC_FIINSHED===")


def test_broach():
    """Тест работоспособности класса CourseWorkPartBroach по всем вариантам"""
    n = [6, 6, 6, 8, 8, 8, 8, 8, 8, 8, 10, 10, 10, 10, 10, 6, 6, 6, 6, 6, 6, 6, 6, 8, 8, 8, 8, 8, 8, 8, 10, 10, 10, 10,
         10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10]
    d = [23, 26, 28, 32, 36, 42, 46, 52, 56, 62, 72, 82, 92, 102, 112, 11, 13, 16, 18, 21, 23, 26, 28, 32, 36, 42, 46,
         52, 56, 62, 72, 82, 92, 102, 112, 16, 18, 21, 23, 26, 28, 32, 36, 42, 46]
    D = [26, 30, 32, 36, 40, 46, 50, 58, 62, 68, 78, 88, 98, 108, 120, 14, 16, 20, 22, 25, 28, 32, 34, 38, 42, 48, 54,
         60, 65, 72, 82, 92, 102, 112, 125, 20, 23, 26, 29, 32, 35, 40, 45, 52, 56]
    b = [6, 6, 7, 6, 7, 8, 9, 10, 10, 12, 12, 12, 14, 16, 18, 3, 3.5, 4, 5, 5, 6, 6, 7, 6, 7, 8, 9, 10, 10, 12, 12, 12,
         14, 16, 18, 2.5, 3, 3, 4, 4, 4, 5, 5, 6, 7]
    f = [0.3, 0.3, 0.3, 0.4, 0.4, 0.4, 0.4, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.4,
         0.4, 0.4, 0.4, 0.4, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.3, 0.3, 0.3, 0.3, 0.4, 0.4, 0.4, 0.4, 0.4,
         0.5]
    Tf = [0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2,
          0.2, 0.2, 0.2, 0.2, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2,
          0.3]
    L = [30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30,
         30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30]
    r = [0.2, 0.2, 0.2, 0.3, 0.3, 0.3, 0.3, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.3,
         0.3, 0.3, 0.3, 0.3, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.2, 0.2, 0.2, 0.2, 0.3, 0.3, 0.3, 0.3, 0.3,
         0.5]

    i = 1
    for _ in D:
        data = {
            "object_type": "Протяжка",
            "n": n[i - 1],
            "d": d[i - 1],
            "D": D[i - 1],
            "b": b[i - 1],
            "f": f[i - 1],
            "Tf": Tf[i - 1],
            "L": L[i - 1],
            "r": r[i - 1],
            "stanok": '7510'
        }
        manager = CourseWorkPartSolverManager()
        if data['object_type'] == "Протяжка":
            variant = f"{data['n']}x{data['d']}x{data['D']}x{data['b']}x{data['f']}x{data['Tf']}x{data['r']}"
            if variant not in t.table_deviation['variants']:
                print(f"Нет найденного варианта: {variant}")
            else:
                manager.set_course_part(CourseWorkPartBroach(data))
                manager.calculate_part()
                manager.save_data(f"./broach/solved_variant_{i}.txt")
        i += 1
    print("===TEST_BROACH_FIINSHED===")


if __name__ == '__main__':
    test_broach()
    test_cutter_circle()
    test_cutter_prismatic()
