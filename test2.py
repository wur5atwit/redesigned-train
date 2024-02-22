import pandas as pd
import time
import re

class ConflictChecker2:

    def count_faculty_conflicts(path_to_possible_schedule):
        start_time = time.time()

        
        df_possible_schedule = pd.read_excel(path_to_possible_schedule)

        # Filter out 0 credit classes
        df_filtered = df_possible_schedule[df_possible_schedule['CREDIT'] != 0]

        faculty_conflicts = 0
        faculty_details = []

        # Function to check for time overlaps with different CRN2s
        def has_different_crn2_overlap(group):
            for new_time in group['NewTime'].unique():
                exams_at_time = group[group['NewTime'] == new_time]
                if len(exams_at_time['CRN2'].unique()) > 1:
                    return True
            return False

        # Check for conflicts for each instructor on each exam day
        for (instructor, exam_day), group in df_filtered.groupby(['INSTRUCTOR', 'EXAM DAY']):
            if has_different_crn2_overlap(group):
                faculty_conflicts += 1
                faculty_details.append((instructor, exam_day))

        end_time = time.time()
        execution_time = end_time - start_time
        print(f"Execution time for count_faculty_conflicts: {execution_time} seconds")

        return faculty_conflicts, faculty_details
    
    
    def count_student_conflicts(path_to_merged_data):
        start_time = time.time()

        
        df_merged = pd.read_excel(path_to_merged_data)
        df_merged = df_merged[df_merged['CREDIT'] != 0]

        # Modified function to check for time overlaps with different CRN2s
        def has_different_crn2_overlap(schedule):
            # Group by NewTime to find overlaps
            for new_time, group in schedule.groupby('NewTime'):
                if len(group['CRN2'].unique()) > 1:  # More than one unique CRN2 at the same NewTime indicates a conflict
                    return True
            return False

        student_conflicts = 0
        students_with_conflicts = []

        # Check for conflicts
        for student in df_merged['STUDENT NAME'].unique():
            student_schedule = df_merged[df_merged['STUDENT NAME'] == student]
            if has_different_crn2_overlap(student_schedule):
                student_conflicts += 1
                students_with_conflicts.append(student)

        end_time = time.time()
        execution_time = end_time - start_time
        print(f"Execution time for count_student_conflicts: {execution_time} seconds")

        return student_conflicts, students_with_conflicts

    
    def count_room_conflicts(path_to_room_capacities, path_to_possible_schedule):
        
        start_time = time.time()

        df_possible_schedule = pd.read_excel(path_to_possible_schedule)
        df_room_capacities = pd.read_excel(path_to_room_capacities)

        df_possible_schedule_filtered = df_possible_schedule[df_possible_schedule['CREDIT'] != 0]

       
        df_merged = pd.merge(df_possible_schedule_filtered, df_room_capacities, left_on='Final Exam Room', right_on='ROOM NAME', how='left')

        # Identify and count conflicts
        conflict_rooms = df_merged[df_merged['Count'] > df_merged['CAPACITY']]
        num_conflicts = conflict_rooms.shape[0]

        
        conflict_details = conflict_rooms[['Final Exam Room', 'Count', 'CAPACITY']]

        end_time = time.time() 
        execution_time = end_time - start_time 
        print(f"Execution time for count_room_conflicts: {execution_time} seconds")

        return num_conflicts, conflict_details
    
    def count_students_with_multiple_exams(path_to_merged_data):
        start_time = time.time()

        df_merged = pd.read_excel(path_to_merged_data)

        df_filtered = df_merged[df_merged['CREDIT'] != 0].copy()

        # Count exams per student per day
        exam_count_per_student = df_filtered.groupby(['STUDENT NAME', 'EXAM DAY']).size().reset_index(name='Exam Count')

        # Identify students with three or more exams on the same day
        students_with_multiple_exams = exam_count_per_student[exam_count_per_student['Exam Count'] >= 3].copy()  # Explicit copy

        # Sorting function for natural sort of student names
        def atoi(text):
            return int(text) if text.isdigit() else text

        def natural_keys(text):
            return [atoi(c) for c in re.split(r'(\d+)', text)]

        # Apply natural sort to student names.
        students_with_multiple_exams['sort_key'] = students_with_multiple_exams['STUDENT NAME'].apply(natural_keys)
        students_sorted_naturally = students_with_multiple_exams.sort_values(by='sort_key').drop('sort_key', axis=1)

        num_students = students_sorted_naturally['STUDENT NAME'].nunique()

        end_time = time.time()
        execution_time = end_time - start_time
        print(f"Execution time for count_students_with_multiple_exams: {execution_time} seconds")

        return num_students, students_sorted_naturally[['STUDENT NAME', 'EXAM DAY', 'Exam Count']]
    
    
    
    def count_double_booked_rooms(path_to_possible_schedule):
        start_time = time.time()
        df_possible_schedule = pd.read_excel(path_to_possible_schedule)

        
        df_filtered = df_possible_schedule[df_possible_schedule['CREDIT'] != 0]

        unique_bookings = df_filtered[['Final Exam Room', 'NewTime', 'CRN2']].drop_duplicates()

        # Group by room and time to see if there are multiple CRN2s for the same room and time
        grouped_bookings = unique_bookings.groupby(['Final Exam Room', 'NewTime'])

        # Identify groups where the count of unique CRN2s is more than 1, indicating a conflict
        conflicts = grouped_bookings.filter(lambda x: x['CRN2'].nunique() > 1)

        # Count the number of conflicts by grouping again 
        conflict_count = conflicts.groupby(['Final Exam Room', 'NewTime']).size().reset_index(name='Conflicts')

        num_conflicts = conflict_count.shape[0]

        end_time = time.time()
        execution_time = end_time - start_time
        print(f"Execution time for count_double_booked_rooms: {execution_time} seconds")

        return num_conflicts, conflict_count
# """"
# path_to_merged_data = r"C:\Users\richa\Downloads\COOP\changedstudent.xlsx"
# path_to_room = r"C:\Users\richa\Downloads\COOP\RoomCapacities.xlsx"
# faculty = ConflictChecker2.count_faculty_conflicts(path_to_merged_data)
# print("facutly with conflicts:", faculty)

# conflicts, students = ConflictChecker2.count_student_conflicts(path_to_merged_data)
# print(f"Total conflicts found: {conflicts}")
# print("Students with conflicts:", students)

# conflicts, rooms = ConflictChecker2.count_room_conflicts(path_to_room, path_to_merged_data)
# print(f"Total conflicts found: {conflicts}")
# print("rooms with conflicts", rooms)


# num_students, students_with_multiple_exams = ConflictChecker2.count_students_with_multiple_exams(path_to_merged_data)
# print(f"Number of students with three or more exams on the same day: {num_students}")
# print("Details of the students and their exam counts on those days:", students_with_multiple_exams)

# conflicts, rooms = ConflictChecker2.count_double_booked_rooms(path_to_merged_data)
# print(f"Total conflicts found: {conflicts}")
# print("rooms doubled booked conflicts", rooms)
# """
