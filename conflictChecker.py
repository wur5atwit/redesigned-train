import pandas as pd
import time
class conflictChecker:
    
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
    def count_student_conflicts(path_to_f23_students, path_to_possible_schedule):
        start_time = time.time()
        df_students = pd.read_excel(path_to_f23_students)
        df_possible_schedule = pd.read_excel(path_to_possible_schedule)

        # Convert CRN to string and filter out 0 credit classes
        df_students['CRN'] = df_students['CRN'].astype(str)
        df_students_filtered = df_students[df_students['CREDIT'] != 0]

        # Prepare the possible schedule data
        df_possible_schedule['CRN'] = df_possible_schedule['CRN2'].str.split('-')
        df_possible_schedule_exploded = df_possible_schedule.explode('CRN')
        df_possible_schedule_exploded['CRN'] = df_possible_schedule_exploded['CRN'].astype(str)

        # Merge the filtered student data with the possible schedule
        df_merged = pd.merge(df_students_filtered, df_possible_schedule_exploded, on='CRN', how='left')

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
    
    @staticmethod
    def count_students_with_multiple_exams(path_to_f23_students, path_to_possible_schedule):
        start_time = time.time()
        df_f23_students = pd.read_excel(path_to_f23_students)
        df_possible_schedule = pd.read_excel(path_to_possible_schedule)

        df_f23_students['CRN'] = df_f23_students['CRN'].astype(str)

        # Split 'CRN2' in 'Possible Schedule', convert to string and explode it for matching
        df_possible_schedule['CRN2'] = df_possible_schedule['CRN2'].astype(str).str.split('-')
        df_possible_schedule_exploded = df_possible_schedule.explode('CRN2')
        
        # Merge datasets on 'CRN'
        df_merged = pd.merge(df_f23_students, df_possible_schedule_exploded, left_on='CRN', right_on='CRN2')

        # Group by student name and NewTime, then count the number of exams
        exam_count_per_newtime = df_merged.groupby(['STUDENT NAME', 'NewTime']).size().reset_index(name='Exam Count')

        # Identify students with more than three exams in a single NewTime slot
        students_with_multiple_exams = exam_count_per_newtime[exam_count_per_newtime['Exam Count'] > 3]

        # Count the number of such students
        num_students = students_with_multiple_exams['STUDENT NAME'].nunique()

        end_time = time.time() 
        execution_time = end_time - start_time 
        print(f"Execution time for count_students_with_multiple_exams: {execution_time} seconds")

        return num_students, students_with_multiple_exams
    
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
    