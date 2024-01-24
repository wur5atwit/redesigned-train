import tkinter as tk
from tkinter import filedialog, messagebox, Listbox, EXTENDED, font as tkFont


from function1 import function1
from function2 import function2
from function3 import function3
from function4 import function4

def raise_frame(frame):
    frame.tkraise()

def run_function1(file_listbox):
    students_file_path = files.get("Students File")
    if students_file_path:
        try:
            output = function1.crn2Sorter(students_file_path)  
            messagebox.showinfo("Result", "File Created: 'combined_courses_CRN2.xlsx' has been created.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
    else:
        messagebox.showwarning("Missing File", "Please upload the 'Students File' for CRN Convert to CRN2.")

def format_dataframe(df):
    return df.to_string(index=False) if not df.empty else "No Data"

def format_list(lst):
    return ', '.join(lst) if lst else 'None'



def run_function2(file_listbox):
    if "Possible Schedule File" in files and "Students File" in files and "Room Capacities File" in files:
        try:
            possible_schedule_file = files["Possible Schedule File"]
            students_file_path = files["Students File"]
            room_capacities_file = files["Room Capacities File"]

            # Call methods from function2
            faculty_conflicts = function2.count_faculty_conflicts(possible_schedule_file)
            student_conflicts, students_with_conflicts = function2.count_student_conflicts(students_file_path, possible_schedule_file)
            room_conflicts, conflict_details = function2.count_room_conflicts(room_capacities_file, possible_schedule_file)
            students_with_multiple_exams_count, students_with_multiple_exams_details = function2.count_students_with_multiple_exams(students_file_path, possible_schedule_file)
            double_booked_rooms_count, double_booked_rooms_details = function2.count_double_booked_rooms(possible_schedule_file)

            # Formatting the results for display
            results_summary = (f"Faculty Conflicts: {faculty_conflicts}\n" +
                               f"Student Conflicts: {student_conflicts}\n" +
                               f"Students with Conflicts: {format_list(students_with_conflicts)}\n" +
                               f"Room Conflicts: {room_conflicts}\nDetails of Room Conflicts:\n{format_dataframe(conflict_details)}\n" +
                               f"Students with Multiple Exams: {students_with_multiple_exams_count}\nDetails:\n{format_dataframe(students_with_multiple_exams_details)}\n" +
                               f"Double Booked Rooms: {double_booked_rooms_count}\nDetails:\n{format_dataframe(double_booked_rooms_details)}")
            
            messagebox.showinfo("Results", results_summary)
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
    else:
        messagebox.showwarning("Missing Files", "Please upload all required files for Schedule Conflicts Checker.")




def run_function3(file_listbox):
    if "Possible Schedule File" in files and "Room Capacities File" in files:
        try:
            possible_schedule_file = files["Possible Schedule File"]
            room_capacities_file = files["Room Capacities File"]

            optimized_schedule = function3.optimize_room_assignments(possible_schedule_file, room_capacities_file)
            messagebox.showinfo("File Created", "The optimized schedule file has been created.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
    else:
        messagebox.showwarning("Missing Files", "Please upload the required files for Room Optimizer.")


def run_function4(file_listbox):
    combined_crn2_file_path = files.get("Combined CRN2 File")
    if combined_crn2_file_path:
        try:
            output = function4.crn2Splitter(combined_crn2_file_path)  
            messagebox.showinfo("Result", "File Created: 'Split_CRNs_Schedule.xlsx' has been created.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
    else:
        messagebox.showwarning("Missing File", "Please upload the 'Combined CRN2 File' for CRN2 Separation.")

def run_schedule():
    run_function1()
    run_function2()
    run_function3()
    run_function4()


def add_file(file_label, file_listbox):
    file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx")])
    if file_path:
        files[file_label] = file_path
        file_listbox.insert(tk.END, f"{file_label}: {file_path}")

def delete_file(file_listbox):
    selected_indices = file_listbox.curselection()
    for index in reversed(selected_indices):
        selected_file_label = file_listbox.get(index)
        file_label = selected_file_label.split(":")[0].strip()
        if file_label in files:
            del files[file_label]
        file_listbox.delete(index)

def show_file_requirements():
    description = (
        "Please upload the following files:\n\n"
        "1) Students File - Contains student data.\n"
        "2) Schedule File - Contains scheduling data.\n"
        "3) Room Capacities File - Contains room capacity data.\n"
        "   Expected format: Excel file with room capacity details."
    )
    messagebox.showinfo("File Requirements", description)

files = {}
root = tk.Tk()
root.title("File Management")
root.geometry('800x600')

# Styling
default_font = tkFont.nametofont("TkDefaultFont")
default_font.configure(size=12)
root.option_add("*Font", default_font)
bg_color = "#f0f0f0"
button_color = "#e1e1e1"
root.configure(bg=bg_color)

# Frames
main_frame = tk.Frame(root, bg=bg_color)
function1_frame = tk.Frame(root, bg=bg_color)
function2_frame = tk.Frame(root, bg=bg_color)
function3_frame = tk.Frame(root, bg=bg_color)
function4_frame = tk.Frame(root, bg=bg_color)

for frame in (main_frame, function1_frame, function2_frame, function3_frame, function4_frame):
    frame.grid(row=0, column=0, sticky='news')

# Main Frame widgets
tk.Button(main_frame, text="CRN Convert to CRN2", command=lambda: raise_frame(function1_frame), bg=button_color).pack(pady=10)
tk.Button(main_frame, text="Schedule Conflicts Checker", command=lambda: raise_frame(function2_frame), bg=button_color).pack(pady=10)
tk.Button(main_frame, text="Room Optimizer", command=lambda: raise_frame(function3_frame), bg=button_color).pack(pady=10)
tk.Button(main_frame, text="CRN2 Seperater", command=lambda: raise_frame(function4_frame), bg=button_color).pack(pady=10)


# Function 1 Frame widgets
tk.Label(function1_frame, text="CRN Converter requires the 'Students File'").pack()
file_listbox1 = Listbox(function1_frame, selectmode=EXTENDED, width=100, height=10)
file_listbox1.pack(pady=20)
tk.Button(function1_frame, text="Upload Students File", command=lambda: add_file('Students File', file_listbox1)).pack()
tk.Button(function1_frame, text="Delete Selected File", command=lambda: delete_file(file_listbox1)).pack()
tk.Button(function1_frame, text="Run CRN Converter", command=lambda: run_function1(file_listbox1)).pack()
tk.Button(function1_frame, text="Back to Main Menu", command=lambda: raise_frame(main_frame)).pack()

# Function 2 Frame widgets
tk.Label(function2_frame, text="Schedule Conflicts Checker requires the 'Students File', 'Possible Schedule File', and 'Room Capacities File'").pack()
file_listbox2 = Listbox(function2_frame, selectmode=EXTENDED, width=100, height=10)
file_listbox2.pack(pady=20)
tk.Button(function2_frame, text="Upload Students File", command=lambda: add_file('Students File', file_listbox2)).pack()
tk.Button(function2_frame, text="Upload Schedule File", command=lambda: add_file('Possible Schedule File', file_listbox2)).pack()
tk.Button(function2_frame, text="Upload Room Capacities File", command=lambda: add_file('Room Capacities File', file_listbox2)).pack()
tk.Button(function2_frame, text="Delete Selected File", command=lambda: delete_file(file_listbox2)).pack()
tk.Button(function2_frame, text="Run Schedule Conflicts Checker", command=lambda: run_function2(file_listbox2)).pack()
tk.Button(function2_frame, text="Back to Main Menu", command=lambda: raise_frame(main_frame)).pack()

# Function 3 Frame widgets
tk.Label(function3_frame, text="Room Optimizer requires the 'Possible Schedule File' and 'Room Capacities File'").pack()
file_listbox3 = Listbox(function3_frame, selectmode=EXTENDED, width=100, height=10)
file_listbox3.pack(pady=20)
tk.Button(function3_frame, text="Upload Schedule File", command=lambda: add_file('Possible Schedule File', file_listbox3)).pack()
tk.Button(function3_frame, text="Upload Room Capacities File", command=lambda: add_file('Room Capacities File', file_listbox3)).pack()
tk.Button(function3_frame, text="Delete Selected File", command=lambda: delete_file(file_listbox3)).pack()
tk.Button(function3_frame, text="Run Room Optimizer", command=lambda: run_function3(file_listbox3)).pack()
tk.Button(function3_frame, text="Back to Main Menu", command=lambda: raise_frame(main_frame)).pack()

# Function 4 Frame widgets
tk.Label(function4_frame, text="CRN2 Separator requires the 'Combined CRN2 File'").pack()
file_listbox4 = Listbox(function4_frame, selectmode=EXTENDED, width=100, height=10)
file_listbox4.pack(pady=20)
tk.Button(function4_frame, text="Upload Combined CRN2 File", command=lambda: add_file('Combined CRN2 File', file_listbox4)).pack()
tk.Button(function4_frame, text="Delete Selected File", command=lambda: delete_file(file_listbox4)).pack()
tk.Button(function4_frame, text="Run CRN2 Separator", command=lambda: run_function4(file_listbox4)).pack()
tk.Button(function4_frame, text="Back to Main Menu", command=lambda: raise_frame(main_frame)).pack()

raise_frame(main_frame)
root.mainloop()