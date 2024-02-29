import pandas as pd
def swap_courses_within_same_day(schedule_df, day, most_popular_time_slot):
    classes_on_day = schedule_df[schedule_df['EXAM DAY'] == day]
    if classes_on_day.empty:
        print(f"No classes found for Day {day}.")
        return

    # Attempt to find a class to swap with at the most popular time slot
    class_at_popular_time = classes_on_day[classes_on_day['EXAM TIME'] == most_popular_time_slot]
    max_students_class = classes_on_day.sort_values('Count', ascending=False).head(1)

    if max_students_class.empty:
        print(f"No classes on Day {day} to consider for swapping.")
        return

    max_students_class_idx = max_students_class.index[0]
    max_students_crn = schedule_df.loc[max_students_class_idx, 'CRN2']

    # If there is no class at the most popular time slot or if the class with the most students is already there
    if class_at_popular_time.empty or max_students_class_idx in class_at_popular_time.index:
        print(f"Day {day}: No swap needed or possible for '{max_students_crn}'.")
    else:
        class_at_popular_time_idx = class_at_popular_time.index[0]
        target_crn = schedule_df.loc[class_at_popular_time_idx, 'CRN2']

        # Swap the EXAM TIME between these two classes
        temp_time = schedule_df.loc[max_students_class_idx, 'EXAM TIME']
        schedule_df.loc[max_students_class_idx, 'EXAM TIME'] = most_popular_time_slot
        schedule_df.loc[class_at_popular_time_idx, 'EXAM TIME'] = temp_time

        print(f"Day {day}: Swapped '{max_students_crn}' with '{target_crn}' to move to time slot {most_popular_time_slot}.")



def popular_time_day_schedule(possible_schedule_df, popular_day_number, least_popular_day_number, most_popular_time_slot):
    newtime_mapping = {
        (1, 1): 0, 
        (2, 1): 1,
        (2, 2): 2,
        (3, 1): 3,
        (3, 2): 4,
        (1, 2): 5,
        (4, 1): 6,
        (4, 2): 7,
        (2, 3): 8,
        (4, 3): 9,
        (3, 3): 10,
        (1, 3): 11,
        (2, 4): 12,
        (1, 4): 13,
        (3, 4): 14,
        (4, 4): 15
    }
    possible_schedule_df['Day Letter'] = possible_schedule_df['EXAM DAY'].map(lambda x: {1: 'A', 2: 'B', 3: 'C', 4: 'D'}.get(x))
    students_per_lettered_day = possible_schedule_df.groupby('Day Letter')['Count'].sum()

    # Identify the lettered day with the most and least student
    most_students_day_letter = students_per_lettered_day.idxmax()
    least_students_day_letter = students_per_lettered_day.idxmin()

    # Assign the most and least popular days
    print(f"Day {most_students_day_letter} has the most students and is assigned to popular day {popular_day_number}.")
    print(f"Day {least_students_day_letter} has the least students and is assigned to least popular day {least_popular_day_number}.")

    # Update 'EXAM DAY' for the most and least populated days
    possible_schedule_df.loc[possible_schedule_df['Day Letter'] == most_students_day_letter, 'EXAM DAY'] = popular_day_number
    possible_schedule_df.loc[possible_schedule_df['Day Letter'] == least_students_day_letter, 'EXAM DAY'] = least_popular_day_number

    for day in possible_schedule_df['EXAM DAY'].unique():
        swap_courses_within_same_day(possible_schedule_df, day, most_popular_time_slot)
    
    possible_schedule_df['NewTime'] = possible_schedule_df.apply(lambda row: newtime_mapping.get((row['EXAM DAY'], row['EXAM TIME'])), axis=1)
    
    return possible_schedule_df

possible_schedule_path = r"C:\Users\richa\Downloads\COOP\Possible_Schedule.xlsx" 
possible_schedule_df = pd.read_excel(possible_schedule_path)
optimized_schedule_df = popular_time_day_schedule(possible_schedule_df, 2, 4, 2)
optimized_output_path = "popular_time_day_schedule.xlsx"
optimized_schedule_df.to_excel(optimized_output_path, index=False)

