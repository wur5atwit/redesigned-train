import pandas as pd

class Schedule:
    @staticmethod
    def function1():
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

        

    
    @staticmethod
    def count_faculty_conflicts():
        path_to_possible_schedule = r"C:\Users\richa\Downloads\COOP\Possible_Schedule.xlsx"

        df_possible_schedule = pd.read_excel(path_to_possible_schedule)

        def has_time_overlap(schedule):
            for day in range(1, 8):  # Assuming 1-7 represents days of the week
                day_schedule = schedule[schedule['EXAM DAY'] == day]
                time_slots = day_schedule['NewTime'].tolist()

                # Debug print
                #if len(day_schedule) > 0:
                    #print(f"Day: {day}, Instructor: {schedule.iloc[0]['INSTRUCTOR']}, Time slots: {time_slots}")

                if len(time_slots) != len(set(time_slots)):
                    return True  # Overlap detected
            return False

        faculty_conflicts = 0

        for instructor in df_possible_schedule['INSTRUCTOR'].unique():
            instructor_schedule = df_possible_schedule[df_possible_schedule['INSTRUCTOR'] == instructor]
            if has_time_overlap(instructor_schedule):
                faculty_conflicts += 1

        return faculty_conflicts
    
    @staticmethod
    def count_student_conflicts():
        path_to_f23_students = r"C:\Users\richa\Downloads\COOP\F23_Students.xlsx"
        path_to_possible_schedule = r"C:\Users\richa\Downloads\COOP\Possible_Schedule.xlsx"

        path_to_f23_students = r"C:\Users\richa\Downloads\COOP\F23_Students.xlsx"
        path_to_possible_schedule = r"C:\Users\richa\Downloads\COOP\Possible_Schedule.xlsx"

        # Load the datasets
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
            schedule_grouped = schedule.groupby('EXAM DAY')
            for day, day_schedule in schedule_grouped:
                time_slots = day_schedule['NewTime'].tolist()
                if len(time_slots) != len(set(time_slots)):
                    return True
            return False

        student_conflicts = 0
        students_with_conflicts = []

        # Check for conflicts
        for student in df_merged['STUDENT NAME'].unique():
            student_schedule = df_merged[df_merged['STUDENT NAME'] == student]
            if has_time_overlap(student_schedule):
                student_conflicts += 1
                students_with_conflicts.append(student)

        return student_conflicts, students_with_conflicts
    
    
    
    @staticmethod
    def count_room_conflicts():
        path_to_room_capacities = r"C:\Users\richa\Downloads\COOP\RoomCapacities.xlsx"
        path_to_possible_schedule = r"C:\Users\richa\Downloads\COOP\Possible_Schedule.xlsx"

        # Load the datasets
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

        return num_conflicts, conflict_details
    
    @staticmethod
    def count_students_with_multiple_exams():
        path_to_f23_students = r"C:\Users\richa\Downloads\COOP\F23_Students.xlsx"
        path_to_possible_schedule = r"C:\Users\richa\Downloads\COOP\Possible_Schedule.xlsx"

        # Load the datasets
        df_f23_students = pd.read_excel(path_to_f23_students)
        df_possible_schedule = pd.read_excel(path_to_possible_schedule)

        # Ensure 'CRN' in 'F23 Students' is a string for consistent merging
        df_f23_students['CRN'] = df_f23_students['CRN'].astype(str)

        # Split 'CRN2' in 'Possible Schedule', convert to string and explode it for matching
        df_possible_schedule['CRN2'] = df_possible_schedule['CRN2'].astype(str).str.split('-')
        df_possible_schedule_exploded = df_possible_schedule.explode('CRN2')
            # Merge datasets on 'CRN'
        df_merged = pd.merge(df_f23_students, df_possible_schedule_exploded, left_on='CRN', right_on='CRN2')

        # Group by student name and exam day, then count the number of exams
        exam_count_per_day = df_merged.groupby(['STUDENT NAME', 'EXAM DAY']).size().reset_index(name='Exam Count')

        # Identify students with more than three exams in a single day
        students_with_multiple_exams = exam_count_per_day[exam_count_per_day['Exam Count'] > 3]

        # Count the number of such students
        num_students = students_with_multiple_exams['STUDENT NAME'].nunique()

        return num_students, students_with_multiple_exams
    
    @staticmethod
    def count_double_booked_rooms():
        path_to_possible_schedule = r"C:\Users\richa\Downloads\COOP\Possible_Schedule.xlsx"

        # Load the dataset
        df_possible_schedule = pd.read_excel(path_to_possible_schedule)

        # Group by room, exam day, and exam time
        room_booking_counts = df_possible_schedule.groupby(['Final Exam Room', 'EXAM DAY', 'NewTime']).size().reset_index(name='Booking Count')

        # Identify double bookings where a room is booked more than once at the same time
        double_booked_rooms = room_booking_counts[room_booking_counts['Booking Count'] > 1]

        # Count the number of double booked instances
        num_double_bookings = double_booked_rooms.shape[0]

        return num_double_bookings, double_booked_rooms
    
    
#To call the function and see the output
output = Schedule.function1()

#count faculty
num_conflicts = Schedule.count_faculty_conflicts()

print(f"Number of faculty conflicts: {num_conflicts}")

# To call the function and get the number of student conflicts and the list of students with conflicts
num_conflicts, students_with_conflicts = Schedule.count_student_conflicts()
print(f"Number of student conflicts: {num_conflicts}")
if num_conflicts > 0:
    print("Students with conflicts:", students_with_conflicts)


num_students, students_with_multiple_exams = Schedule.count_students_with_multiple_exams()
print(f"Number of students with more than three exams in a single day: {num_students}")
if num_students > 0:
    print("Details of students with multiple exams:\n", students_with_multiple_exams)



# To call the function and get the number of room conflicts and the details of conflicts
num_conflicts, conflict_details = Schedule.count_room_conflicts()
print(f"Number of room too small conflicts: {num_conflicts}")
if num_conflicts > 0:
    print("Details of room conflicts:\n", conflict_details)


class ScheduleOptimizer:
    def __init__(self, possible_schedule_path, room_capacity_path):
        self.possible_schedule = pd.read_excel(possible_schedule_path)
        self.room_capacities = pd.read_excel(room_capacity_path)

    def optimize_room_assignments(self):
        # Add a column for original room assignments
        self.possible_schedule['Original Room'] = self.possible_schedule['Final Exam Room']

        # Initialize DataFrame to track room availability for each day
        available_rooms = self.room_capacities.copy()
        available_rooms['Available Days'] = available_rooms.apply(lambda x: list(range(1, 8)), axis=1)  # Assuming 7 days for exams

        # Iterate through each day and NewTime slot
        for day in self.possible_schedule['EXAM DAY'].unique():
            for new_time in self.possible_schedule['NewTime'].unique():
                exams_this_slot = self.possible_schedule[(self.possible_schedule['EXAM DAY'] == day) & (self.possible_schedule['NewTime'] == new_time)]
                exams_this_slot = exams_this_slot.sort_values(by='Count', ascending=False)
                
                for index, exam in exams_this_slot.iterrows():
                    current_room = exam['Final Exam Room']
                    current_capacity = available_rooms.loc[available_rooms['ROOM NAME'] == current_room, 'CAPACITY'].values[0]

                    # Filter for bigger available rooms
                    bigger_available_rooms = available_rooms[(available_rooms['CAPACITY'] > current_capacity) & 
                                                             (available_rooms['Available Days'].apply(lambda x: day in x))]
                    if not bigger_available_rooms.empty:
                        new_room = bigger_available_rooms.iloc[0]
                        self.possible_schedule.at[index, 'Final Exam Room'] = new_room['ROOM NAME']
                        # Update the available days for the new room
                        available_rooms.loc[available_rooms['ROOM NAME'] == new_room['ROOM NAME'], 'Available Days'] = available_rooms.loc[available_rooms['ROOM NAME'] == new_room['ROOM NAME'], 'Available Days'].apply(lambda x: [d for d in x if d != day])

                    # Update the available days for the current room
                    available_rooms.loc[available_rooms['ROOM NAME'] == current_room, 'Available Days'] = available_rooms.loc[available_rooms['ROOM NAME'] == current_room, 'Available Days'].apply(lambda x: [d for d in x if d != day])

        # Format unused rooms list
        unused_rooms_formatted = available_rooms.explode('Available Days')
        unused_rooms_formatted = unused_rooms_formatted.dropna(subset=['Available Days']).reset_index(drop=True)

        # Save the updated exam schedule and formatted unused rooms to Excel
        with pd.ExcelWriter(r"C:\Users\richa\Downloads\COOP\optimized_schedule.xlsx") as writer:
            self.possible_schedule.to_excel(writer, sheet_name='Optimized Schedule', index=False)
            unused_rooms_formatted.to_excel(writer, sheet_name='Formatted Unused Rooms', index=False)

        return self.possible_schedule

# Usage
optimizer = ScheduleOptimizer(r"C:\Users\richa\Downloads\COOP\Possible_Schedule.xlsx", r"C:\Users\richa\Downloads\COOP\RoomCapacities.xlsx")
optimized_schedule = optimizer.optimize_room_assignments()




    

