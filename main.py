import tkinter as tk
from tkinter import filedialog, messagebox, Listbox, EXTENDED, font as tkFont


from crnConverter import crnConverter
from conflictChecker import conflictChecker
from moveToLargerRooms import moveToLargerRooms
from crn2Splitter import crn2Splitter

def raise_frame(frame):
    frame.tkraise()
def ask_save_as_filename(default_name):
    file_path = filedialog.asksaveasfilename(defaultextension=".xlsx",
                                             filetypes=[("Excel files", "*.xlsx")],
                                             initialfile=default_name)
    return file_path if file_path else None

def run_crnConverter(file_listbox):
    students_file_path = files.get("Students File")
    if students_file_path:
        try:
            
            save_path = ask_save_as_filename("combined_courses_CRN2")
            if save_path:
               
                output = crnConverter.crnConverter(students_file_path, save_path)
                messagebox.showinfo("Result", f"File Updated: '{save_path}' has been created/updated.")
            else:
                messagebox.showwarning("Operation Cancelled", "File save operation was cancelled.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
    else:
        messagebox.showwarning("Missing File", "Please upload the 'Students File' for CRN Convert to CRN2.")



def format_dataframe(df):
    return df.to_string(index=False) if not df.empty else "None"

def format_list(lst):
    return ', '.join(lst) if lst else 'None'

def display_results_in_scrolling_window(results_summary):
    top = tk.Toplevel(root)
    top.title("Conflict Check Results")

    scrollbar = tk.Scrollbar(top)
    scrollbar.pack(side="right", fill="y")

    text = tk.Text(top, wrap="word", yscrollcommand=scrollbar.set)
    text.pack(expand=True, fill="both")

    text.insert(tk.END, results_summary)
    scrollbar.config(command=text.yview)


def run_conflictChecker(file_listbox):
    if "Possible Schedule File" in files and "Students File" in files and "Room Capacities File" in files:
        try:
            possible_schedule_file = files["Possible Schedule File"]
            students_file_path = files["Students File"]
            room_capacities_file = files["Room Capacities File"]

            # Call methods from function2
            faculty_conflicts = conflictChecker.count_faculty_conflicts(possible_schedule_file)
            student_conflicts, students_with_conflicts = conflictChecker.count_student_conflicts(students_file_path, possible_schedule_file)
            room_conflicts, conflict_details = conflictChecker.count_room_conflicts(room_capacities_file, possible_schedule_file)
            students_with_multiple_exams_count, students_with_multiple_exams_details = conflictChecker.count_students_with_multiple_exams(students_file_path, possible_schedule_file)
            double_booked_rooms_count, double_booked_rooms_details = conflictChecker.count_double_booked_rooms(possible_schedule_file)

            conflict_details_str = conflict_details.to_string(index=False) if not conflict_details.empty else "None"
            students_with_multiple_exams_details_str = students_with_multiple_exams_details.to_string(index=False) if not students_with_multiple_exams_details.empty else "None"
            double_booked_rooms_details_str = double_booked_rooms_details.to_string(index=False) if not double_booked_rooms_details.empty else "None"
            
            results_summary = (f"Faculty Conflicts: {faculty_conflicts}\n" +
                               f"Student Conflicts: {student_conflicts}\n" +
                               f"Students with Conflicts: {format_list(students_with_conflicts)}\n" +
                               f"Room Conflicts: {room_conflicts}\nDetails of Room Conflicts:\n{conflict_details_str}\n" +
                               f"Students with Multiple Exams: {students_with_multiple_exams_count}\nDetails:\n{students_with_multiple_exams_details_str}\n" +
                               f"Double Booked Rooms: {double_booked_rooms_count}\nDetails:\n{double_booked_rooms_details_str}")

            display_results_in_scrolling_window(results_summary)
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
    else:
        messagebox.showwarning("Missing Files", "Please upload all required files for Schedule Conflicts Checker.")




def run_moveToLargerRooms(file_listbox):
    if "Possible Schedule File" in files and "Room Capacities File" in files:
        try:
            possible_schedule_file = files["Possible Schedule File"]
            room_capacities_file = files["Room Capacities File"]
            
            save_path = ask_save_as_filename("optimized_rooms.xlsx")
            if save_path:
                optimized_schedule = moveToLargerRooms.optimize_room_assignments(possible_schedule_file, room_capacities_file, save_path)
                messagebox.showinfo("File Created", f"The optimized schedule file '{save_path}' has been created.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
    else:
        messagebox.showwarning("Missing Files", "Please upload the required files for Room Optimizer.")


def run_crn2Splitter(file_listbox):
    combined_crn2_file_path = files.get("Combined CRN2 File")
    if combined_crn2_file_path:
        try:
            
            save_path = ask_save_as_filename("Split_CRNs_Schedule.xlsx")
            if save_path:
                
                output = crn2Splitter.crn2Splitter(combined_crn2_file_path, save_path)
                messagebox.showinfo("Result", f"File Created: '{save_path}' has been created.")
            else:
                messagebox.showwarning("Operation Cancelled", "File save operation was cancelled.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
    else:
        messagebox.showwarning("Missing File", "Please upload the 'Combined CRN2 File' for CRN2 Separation.")


def run_schedule():
    run_crnConverter()
    run_conflictChecker()
    run_moveToLargerRooms()
    run_crn2Splitter()


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
tk.Button(function1_frame, text="Run CRN Converter", command=lambda: run_crnConverter(file_listbox1)).pack()
tk.Button(function1_frame, text="Back to Main Menu", command=lambda: raise_frame(main_frame)).pack()

# Function 2 Frame widgets
tk.Label(function2_frame, text="Schedule Conflicts Checker requires the 'Students File', 'Possible Schedule File', and 'Room Capacities File'").pack()
file_listbox2 = Listbox(function2_frame, selectmode=EXTENDED, width=100, height=10)
file_listbox2.pack(pady=20)
tk.Button(function2_frame, text="Upload Students File", command=lambda: add_file('Students File', file_listbox2)).pack()
tk.Button(function2_frame, text="Upload Schedule File", command=lambda: add_file('Possible Schedule File', file_listbox2)).pack()
tk.Button(function2_frame, text="Upload Room Capacities File", command=lambda: add_file('Room Capacities File', file_listbox2)).pack()
tk.Button(function2_frame, text="Delete Selected File", command=lambda: delete_file(file_listbox2)).pack()
tk.Button(function2_frame, text="Run Schedule Conflicts Checker", command=lambda: run_conflictChecker(file_listbox2)).pack()
tk.Button(function2_frame, text="Back to Main Menu", command=lambda: raise_frame(main_frame)).pack()

# Function 3 Frame widgets
tk.Label(function3_frame, text="Room Optimizer requires the 'Possible Schedule File' and 'Room Capacities File'").pack()
file_listbox3 = Listbox(function3_frame, selectmode=EXTENDED, width=100, height=10)
file_listbox3.pack(pady=20)
tk.Button(function3_frame, text="Upload Schedule File", command=lambda: add_file('Possible Schedule File', file_listbox3)).pack()
tk.Button(function3_frame, text="Upload Room Capacities File", command=lambda: add_file('Room Capacities File', file_listbox3)).pack()
tk.Button(function3_frame, text="Delete Selected File", command=lambda: delete_file(file_listbox3)).pack()
tk.Button(function3_frame, text="Run Room Optimizer", command=lambda: run_moveToLargerRooms(file_listbox3)).pack()
tk.Button(function3_frame, text="Back to Main Menu", command=lambda: raise_frame(main_frame)).pack()

# Function 4 Frame widgets
tk.Label(function4_frame, text="CRN2 Separator requires the 'Combined CRN2 File'").pack()
file_listbox4 = Listbox(function4_frame, selectmode=EXTENDED, width=100, height=10)
file_listbox4.pack(pady=20)
tk.Button(function4_frame, text="Upload Combined CRN2 File", command=lambda: add_file('Combined CRN2 File', file_listbox4)).pack()
tk.Button(function4_frame, text="Delete Selected File", command=lambda: delete_file(file_listbox4)).pack()
tk.Button(function4_frame, text="Run CRN2 Separator", command=lambda: run_crn2Splitter(file_listbox4)).pack()
tk.Button(function4_frame, text="Back to Main Menu", command=lambda: raise_frame(main_frame)).pack()

raise_frame(main_frame)
root.mainloop()