import pandas as pd
class function2:
    
    def count_faculty_conflicts(path_to_possible_schedule):
        
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
    def count_student_conflicts(path_to_f23_students, path_to_possible_schedule):
        

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
    def count_students_with_multiple_exams(path_to_f23_students, path_to_possible_schedule):
       

        # Load the datasets
        df_f23_students = pd.read_excel(path_to_f23_students)
        df_possible_schedule = pd.read_excel(path_to_possible_schedule)

    
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
    def count_double_booked_rooms(path_to_possible_schedule):
       

        # Load the dataset
        df_possible_schedule = pd.read_excel(path_to_possible_schedule)

        # Group by room, exam day, and exam time
        room_booking_counts = df_possible_schedule.groupby(['Final Exam Room', 'EXAM DAY', 'NewTime']).size().reset_index(name='Booking Count')

        # Identify double bookings where a room is booked more than once at the same time
        double_booked_rooms = room_booking_counts[room_booking_counts['Booking Count'] > 1]

        # Count the number of double booked instances
        num_double_bookings = double_booked_rooms.shape[0]

        return num_double_bookings, double_booked_rooms
    

    # Replace the file paths with your actual file paths
faculty_conflicts = function2.count_faculty_conflicts(r"C:\Users\richa\Downloads\COOP\excel2.xlsx")
student_conflicts, students_with_conflicts = function2.count_student_conflicts(r"C:\Users\richa\Downloads\COOP\File1ForRichard.xlsx", r"C:\Users\richa\Downloads\COOP\excel2.xlsx")

students_with_multiple_exams, num_students = function2.count_students_with_multiple_exams(r"C:\Users\richa\Downloads\COOP\File1ForRichard.xlsx", r"C:\Users\richa\Downloads\COOP\excel2.xlsx")

# Print the results
print("Faculty Conflicts:", faculty_conflicts)
print("Student Conflicts:", student_conflicts, students_with_conflicts)

print("Students with Multiple Exams:", students_with_multiple_exams)