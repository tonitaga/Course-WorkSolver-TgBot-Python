# Copyright (C) 2023 Gubaydullin Nurislam - All Rights Reserved
# You can't use this code to generate the answer to your course work
#
# You can write me in telegram about course work ― @tonitaga
# If not, prease use the telegram bot or visit   ― @CalculatorlevlevBot

import abc


class BaseCourseWorkPart(metaclass=abc.ABCMeta):
    """
    The basic class of course work parts

    Inheritors:
        CourseWorkPartCutterCircle,
        CourseWorkPartCutterPrismatic,
        CourseWorkPartBroach
    """

    @abc.abstractmethod
    def calculate_part(self) -> None:
        pass

    @abc.abstractmethod
    def save_data(self, path: str) -> None:
        pass
