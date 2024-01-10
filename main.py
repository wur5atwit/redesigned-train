import pandas as pd
class Schedule():
    def function1():
        # Assuming the data is reloaded if the environment was reset
        # Replace these paths with the actual paths if different
        path_to_f23_students = r"C:\Users\richa\Downloads\COOP\F23_Students.xlsx"
        path_to_f23_courses = r"C:\Users\richa\Downloads\COOP\F23_Courses_2.xlsx"

        df_students = pd.read_excel(path_to_f23_students)
        df_courses = pd.read_excel(path_to_f23_courses)

        # Filtering out courses with 0 credits
        df_students_filtered = df_students[df_students['CREDIT'] != 0]

        combined_courses_filtered = df_students_filtered.groupby(['course_instructor', 'title'])['CRN'].apply(
            lambda x: '-'.join(sorted(set(x.astype(str))))
        ).reset_index()

        # Renaming the columns
        combined_courses_filtered = combined_courses_filtered.rename(
            columns={'CRN': 'CRN2', 'course_instructor': 'Instructor'}
        )

        # Saving to Excel and displaying the first few rows
        combined_courses_filtered.to_excel("combined_courses_filtered.xlsx", index=False)
        combined_courses_filtered.head()
    function1()