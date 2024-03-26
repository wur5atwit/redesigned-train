import pandas as pd

def aggregate_student_counts(possible_schedule_df):
    day_counts = possible_schedule_df.groupby('EXAM DAY')['Count'].sum().reset_index()
    day_counts_sorted = day_counts.sort_values(by='Count', ascending=False)
    print("Day counts sorted by student numbers:")
    print(day_counts_sorted)
    return day_counts_sorted

def get_user_day_order(day_counts_sorted):
    print("Please rank the days based on your preference for scheduling (e.g., 3,1,4,2):")
    user_order = input("Enter your preferred order of days: ")
    ordered_days = [int(day.strip()) for day in user_order.split(",") if day.strip().isdigit()]
    return ordered_days

def remap_exam_days_based_on_user_preference(possible_schedule_df, user_day_order):
    """
    Adjusted function to ensure correct mapping based on user preferences.
    
    Parameters:
    - possible_schedule_df: DataFrame containing the exam schedule.
    - user_day_order: List indicating the user's preferred order of days.
    
    Ensures that 'EXAM DAY' is accurately remapped to reflect user preferences.
    """
    unique_days = sorted(possible_schedule_df['EXAM DAY'].unique())
    day_mapping = {original: preferred for original, preferred in zip(unique_days, user_day_order)}
    possible_schedule_df['EXAM DAY'] = possible_schedule_df['EXAM DAY'].apply(lambda x: day_mapping.get(x, x))
    return possible_schedule_df

def auto_assign_exam_times(possible_schedule_df, day, available_times):
    exams_that_day = possible_schedule_df[possible_schedule_df['EXAM DAY'] == day].copy()
    if exams_that_day.empty:
        print(f"No exams scheduled for Day {day}.")
        return possible_schedule_df

    best_time = int(input(f"Enter the best exam time for Day {day}: "))
    worst_time = int(input(f"Enter the worst exam time for Day {day}: "))

    exams_sorted_by_count = exams_that_day.sort_values(by='Count', ascending=False)
    exams_sorted_by_count.iloc[0, exams_sorted_by_count.columns.get_loc('EXAM TIME')] = best_time
    if len(exams_sorted_by_count) > 1:
        exams_sorted_by_count.iloc[-1, exams_sorted_by_count.columns.get_loc('EXAM TIME')] = worst_time

    room_availability = {room: [time for time in available_times if time not in [best_time, worst_time]] for room in exams_that_day['Final Exam Room'].unique()}

    for index, exam in exams_sorted_by_count.iloc[1:-1].iterrows():
        room = exam['Final Exam Room']
        for time in room_availability[room]:
            if not possible_schedule_df[(possible_schedule_df['Final Exam Room'] == room) & (possible_schedule_df['EXAM TIME'] == time)].empty:
                continue  
            exams_sorted_by_count.at[index, 'EXAM TIME'] = time
            break

    for index, row in exams_sorted_by_count.iterrows():
        possible_schedule_df.loc[possible_schedule_df['CRN2'] == row['CRN2'], 'EXAM TIME'] = row['EXAM TIME']

    return possible_schedule_df

def change_exam_time_if_desired(possible_schedule_df, available_times):
    while True:
        change = input("Do you want to change the time for any exam? (yes/no): ").lower()
        if change != 'yes':
            break

        crn = input("Enter the CRN of the exam you want to change: ")
        new_time = int(input(f"Enter the new exam time (Available times are: {available_times}): "))

        if new_time not in available_times:
            print(f"Invalid time selected. Please choose from the available times: {available_times}")
            continue

        if crn in possible_schedule_df['CRN2'].values:
            possible_schedule_df.loc[possible_schedule_df['CRN2'] == crn, 'EXAM TIME'] = new_time
            print("Exam time updated.")
        else:
            print("CRN not found. Please try again.")

def update_schedule_with_new_times(possible_schedule_df, ordered_days, available_times):
    possible_schedule_df = remap_exam_days_based_on_user_preference(possible_schedule_df, ordered_days)
    for day in ordered_days:
        possible_schedule_df = auto_assign_exam_times(possible_schedule_df, day, available_times)
    return possible_schedule_df

# Script execution begins here
available_times = [1, 2, 3, 4]
possible_schedule_df = pd.read_excel("Possible_Schedule.xlsx")
day_counts_sorted = aggregate_student_counts(possible_schedule_df)
ordered_days = get_user_day_order(day_counts_sorted)

# Update the schedule based on new day order and then assign times
possible_schedule_df_updated = update_schedule_with_new_times(possible_schedule_df, ordered_days, available_times)

# Optionally, allow changes to exam times
change_exam_time_if_desired(possible_schedule_df_updated, available_times)

# Save the updated schedule
possible_schedule_df_updated.to_excel("Updated_Possible_Schedule.xlsx", index=False)
print("Updated schedule saved to 'Updated_Possible_Schedule.xlsx'.")
