import pandas as pd

class specificStudent:
    @staticmethod
    def find_student_conflicts(student_name):
        path_to_f23_students = r"C:\Users\richa\Downloads\COOP\F23_Students.xlsx"
        path_to_possible_schedule = r"C:\Users\richa\Downloads\COOP\Possible_Schedule.xlsx"

        df_students = pd.read_excel(path_to_f23_students)
        df_possible_schedule = pd.read_excel(path_to_possible_schedule)

        student_courses = df_students[df_students['STUDENT NAME'] == student_name].copy()
        student_courses['CRN'] = student_courses['CRN'].astype(str)
        df_possible_schedule['CRN'] = df_possible_schedule['CRN2'].str.split('-')
        df_possible_schedule_exploded = df_possible_schedule.explode('CRN')
        df_possible_schedule_exploded['CRN'] = df_possible_schedule_exploded['CRN'].astype(str)

        student_exam_schedule = pd.merge(student_courses, df_possible_schedule_exploded, on='CRN', how='left')

        def find_conflicting_courses(schedule):
            conflicts = {}
            schedule_grouped = schedule.groupby('EXAM DAY')
            for day, day_schedule in schedule_grouped:
                day_conflicts = day_schedule[day_schedule.duplicated(['NewTime'], keep=False)]
                if not day_conflicts.empty:
                    conflicts[day] = day_conflicts[['CRN', 'NewTime', 'title']].to_dict('records')
            return conflicts

        student_conflicts = find_conflicting_courses(student_exam_schedule)
        return student_conflicts

# Find conflicts for student W1
conflicts_for_w1 = specificStudent.find_student_conflicts('W3095')
print(f"Student W1 has conflicts on these days and courses: {conflicts_for_w1}")