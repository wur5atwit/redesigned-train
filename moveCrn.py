import pandas as pd
import time
import re
class ConflictChecker:
    def count_faculty_conflicts(df_possible_schedule):
        start_time = time.time()
        

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
    
    def count_student_conflicts(df_students, df_possible_schedule):
        start_time = time.time()

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

    def count_room_conflicts(df_room_capacities, df_possible_schedule):
        
        start_time = time.time()

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

    def count_students_with_multiple_exams(df_students, df_possible_schedule):
        start_time = time.time()


        # Prepare CRN fields for merging
        df_students['CRN'] = df_students['CRN'].astype(str)
        df_possible_schedule['CRN2'] = df_possible_schedule['CRN2'].astype(str).str.split('-')
        df_possible_schedule_exploded = df_possible_schedule.explode('CRN2')

        df_merged = pd.merge(df_students, df_possible_schedule_exploded, left_on='CRN', right_on='CRN2')

        exam_count_per_student = df_merged.groupby(['STUDENT NAME', 'EXAM DAY']).size().reset_index(name='Exam Count')

        # Identify students with three or more exams on the same day
        students_with_multiple_exams = exam_count_per_student[exam_count_per_student['Exam Count'] >= 3].copy()

        # Function to extract numbers from the string for sorting
        def atoi(text):
            return int(text) if text.isdigit() else text

        def natural_keys(text):
            return [atoi(c) for c in re.split(r'(\d+)', text)]

        # Apply natural sort
        students_with_multiple_exams.sort_values(by='STUDENT NAME', key=lambda x: x.map(natural_keys), inplace=True)

        num_students = students_with_multiple_exams['STUDENT NAME'].nunique()

        end_time = time.time() 
        execution_time = end_time - start_time 
        print(f"Execution time for count_students_with_multiple_exams: {execution_time} seconds")

        return num_students, students_with_multiple_exams

    def count_double_booked_rooms(df_possible_schedule):
        start_time = time.time()

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



def move_crn_to_all_new_times_and_check_conflicts(crn2_str, exam_schedule_df, room_capacities_df, f23_students_df):
    newtime_mapping = {
        0: (1, 1), 1: (2, 1), 2: (2, 2), 3: (3, 1), 4: (3, 2), 5: (1, 2),
        6: (4, 1), 7: (4, 2), 8: (2, 3), 9: (4, 3), 10: (3, 3), 11: (1, 3),
        12: (2, 4), 13: (1, 4), 14: (3, 4), 15: (4, 4)
    }

    for newtime, (new_day, new_time) in newtime_mapping.items():
        modified_schedule = exam_schedule_df.copy()

        # Find rows where CRN2 matches the crn2_str and update them
        crn2_exists = modified_schedule['CRN2'].str.contains(crn2_str)
        modified_schedule.loc[crn2_exists, 'EXAM DAY'] = new_day
        modified_schedule.loc[crn2_exists, 'EXAM TIME'] = new_time
        modified_schedule.loc[crn2_exists, 'NewTime'] = newtime

        print(f"\nConflicts for new time {newtime}:")
        faculty_conflicts = ConflictChecker.count_faculty_conflicts(modified_schedule)
        student_conflicts, students_with_conflicts = ConflictChecker.count_student_conflicts(f23_students_df, modified_schedule)
        room_conflicts, conflict_details = ConflictChecker.count_room_conflicts(room_capacities_df, modified_schedule)
        students_with_multiple_exams, students_with_multiple_exams_details = ConflictChecker.count_students_with_multiple_exams(f23_students_df, modified_schedule)
        double_booked_rooms, double_booked_rooms_details = ConflictChecker.count_double_booked_rooms(modified_schedule)

        # Display conflict summary for the current newtime
        print(f"Faculty Conflicts: {faculty_conflicts}")
        print(f"Student Conflicts: {student_conflicts}")
        if students_with_conflicts:
            print(f"Students with Conflicts: {', '.join(students_with_conflicts)}")
        print(f"Room Conflicts: {room_conflicts}")
        if not conflict_details.empty:
            print("Detailed Room Conflicts:")
            print(conflict_details.to_string(index=False))
        print(f"Students with Multiple Exams: {students_with_multiple_exams}")
        if not students_with_multiple_exams_details.empty:
            print("Details of Students with Multiple Exams:")
            print(students_with_multiple_exams_details.to_string(index=False))
        print(f"Double Booked Rooms: {double_booked_rooms}")
        if not double_booked_rooms_details.empty:
            print("Details of Double Booked Rooms:")
            print(double_booked_rooms_details.to_string(index=False))



exam_schedule_path = "C:/Users/richa/Downloads/COOP/Possible_Schedule.xlsx"
room_capacities_path = "C:/Users/richa/Downloads/COOP/RoomCapacities.xlsx"
f23_students_path = "C:/Users/richa/Downloads/COOP/F23_Students.xlsx"


exam_schedule_df = pd.read_excel(exam_schedule_path)
room_capacities_df = pd.read_excel(room_capacities_path)
f23_students_df = pd.read_excel(f23_students_path)


crn2_str = "12264-12265-12266-12267-12778"


move_crn_to_all_new_times_and_check_conflicts(crn2_str, exam_schedule_df, room_capacities_df, f23_students_df)
