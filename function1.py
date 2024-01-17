import pandas as pd
class function1:
    
    def crn2Sorter():
        path_to_f23_students = r"C:\Users\richa\Downloads\COOP\F23_Students.xlsx"
        
        df_students = pd.read_excel(path_to_f23_students)
        
        # Filtering
        df_students_filtered = df_students[
        (df_students['CREDIT'] != 0) 
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
        # Add all excluded CRN2s here
        excluded_crn2 = {""}  
        
        combined_courses_filtered = combined_courses_filtered[~combined_courses_filtered['CRN2'].isin(excluded_crn2)]

        # Saving to Excel
        combined_courses_filtered.to_excel("combined_courses_CRN2.xlsx", index=False)

        return combined_courses_filtered.head()