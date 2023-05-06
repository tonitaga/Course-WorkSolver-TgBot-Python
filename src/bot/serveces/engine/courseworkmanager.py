# Copyright (C) 2023 Gubaydullin Nurislam - All Rights Reserved
# You can't use this code to generate the answer to your course work
#
# You can write me in telegram about course work ― @tonitaga
# If not, prease use the telegram bot or visit   ― @CalculatorlevlevBot

from . import tables as t
from .broach import CourseWorkPartBroach
from .basecourseworkpart import BaseCourseWorkPart
from .cuttercircle import CourseWorkPartCutterCircle
from .cutterprismatic import CourseWorkPartCutterPrismatic


class CourseWorkPartSolverManager:
    """
    The main class that manage all parts of course work
    that inherits from BaseCourseWorkPart class
    """

    def __init__(self) -> None:
        self.__course_work_part = None

    def set_course_part(self, course_work_part: BaseCourseWorkPart) -> None:
        self.__course_work_part = course_work_part

    def calculate_part(self) -> None:
        self.__course_work_part.calculate_part()

    def save_data(self, path: str) -> None:
        self.__course_work_part.save_data(path)
