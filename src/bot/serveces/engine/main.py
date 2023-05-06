from .courseworkmanager import *


def start_calculate(data):

    manager = CourseWorkPartSolverManager()
    if data['object_type'] == "Резец - Круглый":
        manager.set_course_part(CourseWorkPartCutterCircle(data))
        manager.calculate_part()
        manager.save_data(f"./solved_cutter_circle_{data['chat_id']}.txt")
    elif data['object_type'] == "Резец - Призматический":
        manager.set_course_part(CourseWorkPartCutterPrismatic(data))
        manager.calculate_part()
        manager.save_data(f"./solved_cutter_prismatic_{data['chat_id']}.txt")
    elif data['object_type'] == "Протяжка":
        manager.set_course_part(CourseWorkPartBroach(data))
        manager.calculate_part()
        manager.save_data(f"./solved_broach_{data['chat_id']}.txt")