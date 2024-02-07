import pandas as pd
def optimize_schedule_and_print_details(possible_schedule_df, most_popular_day=3, most_popular_time_slot=2):
    """
    Optimize the exam schedule by:
    - Assigning the most popular time slot to the class with the most students on each day.
    - Printing details about the most popular day, the class with the most students on other days, and handling missing days.
    
    Args:
    - possible_schedule_df: DataFrame containing the exam schedule.
    - most_popular_day: The designated most popular exam day.
    - most_popular_time_slot: The most popular exam time slot to assign.
    
    Returns:
    - DataFrame with the optimized exam schedule.
    """
    # Identify unique days and sort them
    unique_days = sorted(possible_schedule_df['EXAM DAY'].unique())

    # Calculate total students per day
    students_per_day = possible_schedule_df.groupby('EXAM DAY')['Count'].sum()

    # Identify the day with the highest number of students and assign it as the most popular day
    day_with_most_students = students_per_day.idxmax()
    max_students = students_per_day.max()

    print(f"Day with the most students: Day {day_with_most_students} with {max_students} students. Assigned as the most popular day.")

    # Initialize the optimized DataFrame
    optimized_schedule_df = possible_schedule_df.copy()

    # Iterate through each unique day present in the data
    for day in unique_days:
        # Find the exam with the most students for the current day
        exams_on_day = optimized_schedule_df[optimized_schedule_df['EXAM DAY'] == day]
        max_students_exam_index = exams_on_day['Count'].idxmax()
        
        # Assign the most popular time slot to this exam
        optimized_schedule_df.at[max_students_exam_index, 'EXAM TIME'] = most_popular_time_slot

        # Print details for the exam assigned to the popular time slot
        if day != day_with_most_students:  # Skip the overall most popular day to avoid redundancy
            exam_details = optimized_schedule_df.loc[max_students_exam_index]
            print(f"Day {day}: Class {exam_details['CRN2']} with {exam_details['Count']} students assigned to the most popular time slot.")

    return optimized_schedule_df

# Example usage
possible_schedule_path = r"C:\Users\richa\Downloads\COOP\Possible_Schedule.xlsx" # Specify the actual path
possible_schedule_df = pd.read_excel(possible_schedule_path)

optimized_schedule_df = optimize_schedule_and_print_details(possible_schedule_df)

# Save the optimized schedule
optimized_output_path = "save_Optimized_Schedule.xlsx"  # Specify the actual output path
optimized_schedule_df.to_excel(optimized_output_path, index=False)

