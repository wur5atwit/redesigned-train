import pandas as pd
def swap_courses_time_slots(schedule_df, source_idx, target_idx):
    
    source_course = schedule_df.at[source_idx, 'CRN2']
    target_course = schedule_df.at[target_idx, 'CRN2']
    
    # Perform the swap of EXAM DAY and EXAM TIME
    temp = schedule_df.loc[source_idx, ['EXAM DAY', 'EXAM TIME']].copy()
    schedule_df.loc[source_idx, ['EXAM DAY', 'EXAM TIME']] = schedule_df.loc[target_idx, ['EXAM DAY', 'EXAM TIME']]
    schedule_df.loc[target_idx, ['EXAM DAY', 'EXAM TIME']] = temp

    print(f"Swapped '{source_course}' to the popular time slot, moving '{target_course}' to another time slot.")


def popular_time_day_schedule(possible_schedule_df, popular_day_number=2, least_popular_day_number=4, most_popular_time_slot=2):
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

    # Update 'EXAM DAY' for the most and least student-populated days
    possible_schedule_df.loc[possible_schedule_df['Day Letter'] == most_students_day_letter, 'EXAM DAY'] = popular_day_number
    possible_schedule_df.loc[possible_schedule_df['Day Letter'] == least_students_day_letter, 'EXAM DAY'] = least_popular_day_number

    # Assign the most popular time slot to the class with the most students on each day
    for day in possible_schedule_df['EXAM DAY'].unique():
        day_classes = possible_schedule_df[possible_schedule_df['EXAM DAY'] == day]
        max_students_class_idx = day_classes['Count'].idxmax()  # Class with the most students on this day
        popular_time_class = possible_schedule_df[(possible_schedule_df['EXAM DAY'] == popular_day_number) & (possible_schedule_df['EXAM TIME'] == most_popular_time_slot)]

        if not popular_time_class.empty:
            popular_time_class_idx = popular_time_class.index[0]
            # Perform swap if the class with the most students is not already in the popular time slot
            if max_students_class_idx != popular_time_class_idx:
                swap_courses_time_slots(possible_schedule_df, max_students_class_idx, popular_time_class_idx)

    
    possible_schedule_df['NewTime'] = possible_schedule_df.apply(lambda row: newtime_mapping[(row['EXAM DAY'], row['EXAM TIME'])], axis=1)

    return possible_schedule_df

possible_schedule_path = r"C:\Users\richa\Downloads\COOP\Possible_Schedule.xlsx" 
possible_schedule_df = pd.read_excel(possible_schedule_path)
optimized_schedule_df = popular_time_day_schedule(possible_schedule_df, popular_day_number=2, least_popular_day_number=4)
optimized_output_path = "popular_time_day_schedule.xlsx"
optimized_schedule_df.to_excel(optimized_output_path, index=False)

