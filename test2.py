import pandas as pd
import time
import re

class ConflictChecker:

    def count_faculty_conflicts(path_to_possible_schedule):
        start_time = time.time()
        df_possible_schedule = pd.read_excel(path_to_possible_schedule)

        def has_time_overlap(schedule):
            time_slots = schedule['NewTime'].tolist()
            return len(time_slots) != len(set(time_slots))  # Overlap if duplicates exist

        faculty_conflicts = 0

        for instructor in df_possible_schedule['INSTRUCTOR'].unique():
            instructor_schedule = df_possible_schedule[df_possible_schedule['INSTRUCTOR'] == instructor]
            if has_time_overlap(instructor_schedule):
                faculty_conflicts += 1
        end_time = time.time() 
        execution_time = end_time - start_time 
        print(f"Execution time for count_faculty_conflicts: {execution_time} seconds")

        return faculty_conflicts
    
    @staticmethod
    def count_student_conflicts(path_to_merged_data):
        start_time = time.time()

        df_merged = pd.read_excel(path_to_merged_data)
        
        df_merged = df_merged[df_merged['CREDIT'] != 0]

        def has_time_overlap(schedule):
            time_slots = schedule['NewTime'].tolist()
            return len(time_slots) != len(set(time_slots))

        student_conflicts = 0
        students_with_conflicts = []

        # Check for conflicts
        for student in df_merged['STUDENT NAME'].unique():
            student_schedule = df_merged[df_merged['STUDENT NAME'] == student]
            if has_time_overlap(student_schedule):
                student_conflicts += 1
                students_with_conflicts.append(student)

        end_time = time.time()
        execution_time = end_time - start_time
        print(f"Execution time for count_student_conflicts: {execution_time} seconds")

        return student_conflicts, students_with_conflicts

    
    @staticmethod
    def count_room_conflicts(path_to_room_capacities, path_to_possible_schedule):
        
        start_time = time.time()
        
        df_room_capacities = pd.read_excel(path_to_room_capacities)
        df_possible_schedule = pd.read_excel(path_to_possible_schedule)


        # Merge the possible schedule with room capacities
        df_merged = pd.merge(df_possible_schedule, df_room_capacities, left_on='Final Exam Room', right_on='ROOM NAME', how='left')

        # Identify conflicts where the number of students exceeds room capacity
        conflict_rooms = df_merged[df_merged['Count'] > df_merged['CAPACITY']]

        # Count the number of conflicts
        num_conflicts = conflict_rooms.shape[0]

        # Extract details of the conflicts
        conflict_details = conflict_rooms[['Final Exam Room', 'Count', 'CAPACITY']]

        end_time = time.time() 
        execution_time = end_time - start_time 
        print(f"Execution time for count_room_conflicts: {execution_time} seconds")

        return num_conflicts, conflict_details
    
    def count_students_with_multiple_exams(path_to_merged_data):
        start_time = time.time()

        
        df_merged = pd.read_excel(path_to_merged_data)

        
        df_filtered = df_merged[df_merged['CREDIT'] != 0]

        
        # Count exams per student per day
        exam_count_per_student = df_filtered.groupby(['STUDENT NAME', 'EXAM DAY']).size().reset_index(name='Exam Count')

        # Identify students with three or more exams on the same day
        students_with_multiple_exams = exam_count_per_student[exam_count_per_student['Exam Count'] >= 3]

        # Sorting function for natural sort of student names
        def atoi(text):
            return int(text) if text.isdigit() else text

        def natural_keys(text):
            return [atoi(c) for c in re.split(r'(\d+)', text)]

        # Apply natural sort to student names
        students_with_multiple_exams['sort_key'] = students_with_multiple_exams['STUDENT NAME'].apply(lambda x: natural_keys(x))
        students_sorted_naturally = students_with_multiple_exams.sort_values(by='sort_key').drop('sort_key', axis=1)

        num_students = students_sorted_naturally['STUDENT NAME'].nunique()

        end_time = time.time()
        execution_time = end_time - start_time
        print(f"Execution time for count_students_with_multiple_exams: {execution_time} seconds")

        return num_students, students_sorted_naturally[['STUDENT NAME', 'EXAM DAY', 'Exam Count']]
    

    @staticmethod
    def count_double_booked_rooms(path_to_possible_schedule):
        start_time = time.time()
        df_possible_schedule = pd.read_excel(path_to_possible_schedule)

        # Group by room and NewTime
        room_booking_counts = df_possible_schedule.groupby(['Final Exam Room', 'NewTime']).size().reset_index(name='Booking Count')

        # Identify double bookings where a room is booked more than once at the same time
        double_booked_rooms = room_booking_counts[room_booking_counts['Booking Count'] > 1]

        # Count the number of double booked instances
        num_double_bookings = double_booked_rooms.shape[0]

        end_time = time.time() 
        execution_time = end_time - start_time 
        print(f"Execution time for count_double_booked_rooms: {execution_time} seconds")

        return num_double_bookings, double_booked_rooms
    
path_to_merged_data = r"changedstudent.xlsx"

#conflicts, students = ConflictChecker.count_student_conflicts(path_to_merged_data)
#print(f"Total conflicts found: {conflicts}")
#print("Students with conflicts:", students)



num_students, students_with_multiple_exams = ConflictChecker.count_students_with_multiple_exams(path_to_merged_data)
print(f"Number of students with three or more exams on the same day: {num_students}")
print("Details of the students and their exam counts on those days:", students_with_multiple_exams)