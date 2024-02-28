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
def notify_about_moving_multi_section_courses(crn2_str, df_student, df_schedule):
    
    moving_crn_list = crn2_str.split('-')
    moving_course_titles = df_student[df_student['CRN'].astype(str).isin(moving_crn_list)]['title'].unique()
    
    for title in moving_course_titles:
        # Find all CRNs for courses with this title, excluding the moving CRNs
        all_crns_for_title = df_student[df_student['title'] == title]['CRN'].unique()
        crns_excluding_moving = [crn for crn in all_crns_for_title if str(crn) not in moving_crn_list]
        
        if not crns_excluding_moving: 
            continue
        # Check if the remaining CRNs are part of the schedule's CRN2 
        matches = df_schedule['CRN2'].apply(lambda x: any(str(crn) in x for crn in crns_excluding_moving))
        if matches.any():
            print(f"Moving CRN2 {crn2_str} affects other sections of '{title}'. Consider exam scheduling impacts.")
            break



def find_larger_available_room(current_room, newtime, df_room_capacities, modified_schedule):
    current_capacity = df_room_capacities.loc[df_room_capacities['ROOM NAME'] == current_room, 'CAPACITY'].iloc[0]
    available_rooms = df_room_capacities[(df_room_capacities['CAPACITY'] > current_capacity) & (df_room_capacities['ROOM NAME'] != "ANXCN106")].sort_values('CAPACITY', ascending=True)
    
    for _, room_row in available_rooms.iterrows():
        room_name = room_row['ROOM NAME']
        # Check if this room is already booked at the newtime
        if not modified_schedule[(modified_schedule['Final Exam Room'] == room_name) & (modified_schedule['NewTime'] == newtime)].empty:
            continue  
        return room_name 
    
    return current_room



def move_crn_to_all_new_times_and_check_conflicts(crn2_str, exam_schedule_df, room_capacities_df, f23_students_df):
    newtime_mapping = {
        0: (1, 1), 1: (2, 1), 2: (2, 2), 3: (3, 1), 4: (3, 2), 5: (1, 2),
        6: (4, 1), 7: (4, 2), 8: (2, 3), 9: (4, 3), 10: (3, 3), 11: (1, 3),
        12: (2, 4), 13: (1, 4), 14: (3, 4), 15: (4, 4)
    }

    for newtime, (new_day, new_time) in newtime_mapping.items():
        modified_schedule = exam_schedule_df.copy()
        
        crn2_exists = modified_schedule['CRN2'].str.contains(crn2_str)
        if crn2_exists.any():
            notify_about_moving_multi_section_courses(crn2_str, f23_students_df, exam_schedule_df)
            
            original_room = modified_schedule.loc[crn2_exists, 'Final Exam Room'].iloc[0]
            larger_room = find_larger_available_room(original_room, newtime, room_capacities_df, modified_schedule)
            if larger_room != original_room and larger_room != "ANXCN106":
                print(f"CRN2 {crn2_str} moved to a larger room: {larger_room} for new time {newtime}.")
            else:
                print(f"CRN2 {crn2_str} remains in the same room: {original_room} for new time {newtime}.")

            modified_schedule.loc[crn2_exists, 'EXAM DAY'] = new_day
            modified_schedule.loc[crn2_exists, 'EXAM TIME'] = new_time
            modified_schedule.loc[crn2_exists, 'NewTime'] = newtime
            modified_schedule.loc[crn2_exists, 'Final Exam Room'] = larger_room if larger_room != "ANXCN106" else original_room

        # After updating the room assignments, check conflicts
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
df_student = pd.read_excel(f23_students_path)


crn2_str = "11615"
crn_to_title_map = df_student.set_index('CRN')['title'].to_dict()

move_crn_to_all_new_times_and_check_conflicts(crn2_str, exam_schedule_df, room_capacities_df, df_student)
