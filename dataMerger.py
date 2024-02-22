import pandas as pd
import time
def addExamToStudent(student_schedule_path, exam_schedule_path, output_file_path):

    start = time.time()
    student_schedule = pd.read_excel(student_schedule_path)
    exam_schedule = pd.read_excel(exam_schedule_path)

    # Rename 'course_instructor' in student_schedule to 'INSTRUCTOR' to match exam_schedule
    student_schedule.rename(columns={'course_instructor': 'INSTRUCTOR'}, inplace=True)

    # Define the columns to merge on
    merge_keys = ['COURSE NUMBER', 'INSTRUCTOR', 'SUBJECT']
    for key in merge_keys:
        if key not in student_schedule.columns or key not in exam_schedule.columns:
            raise KeyError(f"'{key}' column not found in one or both DataFrames.")

    
    merged_schedule = pd.merge(student_schedule, exam_schedule, on=merge_keys, how='left')

   
    merged_schedule.to_excel(output_file_path, index=False)
    end_time = time.time() 
    execution_time = end_time - start 
    print(f"Execution time to split CRN2's: {execution_time} seconds") 

    return merged_schedule

