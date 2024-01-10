import pandas as pd

class Schedule:
    @staticmethod
    def function1():
        path_to_f23_students = r"C:\Users\richa\Downloads\COOP\F23_Students.xlsx"
        path_to_f23_courses = r"C:\Users\richa\Downloads\COOP\F23_Courses_2.xlsx"

        df_students = pd.read_excel(path_to_f23_students)
        df_courses = pd.read_excel(path_to_f23_courses)

        # Filtering
        df_students_filtered = df_students[
        (df_students['CREDIT'] != 0) #& 
        #(~df_students['title'].str.lower().str.startswith('studio')) &
        #(df_students['title'].str.upper() != 'DESIGN AS RESEARCH') &
        #(df_students['title'].str.upper() != 'GLOBAL RESEARCH  STUDIO') &
        #(df_students['title'].str.upper() != 'METHODS OF HIST, THRY & CRIT')
        ]       


        # Group by instructor and title, and combine CRNs
        combined_courses_filtered = df_students_filtered.groupby(['course_instructor', 'title'])['CRN'].apply(
            lambda x: '-'.join(sorted(set(x.astype(str))))
        ).reset_index()

        # Renaming the columns
        combined_courses_filtered.rename(columns={'CRN': 'CRN2', 'course_instructor': 'Instructor'}, inplace=True)

        # Reordering the columns
        combined_courses_filtered = combined_courses_filtered[['CRN2', 'Instructor', 'title']]

        # Exclude certain CRN2s
        excluded_crn2 = {'11642-11643-11645', '11678', '11689-12782', '11692-11694-11696', '11698', '11702-11705-11708', '11805', '11810-11811', '11812', '11814', '11821', '11823', '11829', '11830', '11834', '11835', '11838', '11840', '11843', '11847', '11910-11918', '11966-11967', '11986-11988', '12045-12051', '12052', '12070', '12071', '12086', '12160', '12255', '12256', '12258', '12259', '12260', '12261', '12279', '12311', '12313', '12336', '12359', '12361-12362', '12365', '12379', '12380', '12381', '12382-12389', '12384-12388', '12385-12387', '12390', '12393-12397-12410-12414', '12398-12409', '12423', '12426', '12442', '12443-12444', '12449', '12489', '12490', '12491', '12492', '12499', '12516', '12551', '12573', '12583-12589', '12585-12591', '12595', '12597-12601', '12599-12603-12605', '12623-12625', '12633-12635', '12641', '12648', '12650', '12655', '12667', '12669-12671', '12707', '12728', '12730', '12731', '12733', '12735', '12755', '12786', '12792', '12800', '12810', '12815', '12816', '12818', '12821', '12825', '12829', '12832', '12837', '12841', '12859', '12865', '12875', '12876', '12877', '12878', '12879'}  # Add all excluded CRN2s here
        combined_courses_filtered = combined_courses_filtered[~combined_courses_filtered['CRN2'].isin(excluded_crn2)]

        # Count the number of students for each CRN
        df_students['CRN_str'] = df_students['CRN'].astype(str)
        student_counts = df_students['CRN_str'].value_counts().reset_index()
        student_counts.columns = ['CRN', 'Student Count']

        # Merge the student count with the combined course details
        # Split CRN2 and explode to match with individual CRNs
        combined_courses_filtered['CRN2_split'] = combined_courses_filtered['CRN2'].str.split('-')
        exploded_combined_courses = combined_courses_filtered.explode('CRN2_split')

        # Merge with student counts
        merged_data = pd.merge(exploded_combined_courses, student_counts, left_on='CRN2_split', right_on='CRN', how='left')

        # Group by CRN2 and sum the student counts
        final_data = merged_data.groupby(['CRN2', 'Instructor', 'title'])['Student Count'].sum().reset_index()

        # Saving to Excel
        final_data.to_excel("combined_courses_filtered_with_counts.xlsx", index=False)

        return final_data.head()

# To call the function and see the output
output = Schedule.function1()
print(output)