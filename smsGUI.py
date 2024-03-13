import tkinter as tk
from tkinter import messagebox, simpledialog
import mysql.connector

# Establishing connection to MySQL database
db_connection = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="Veena@12345",
    database="sms3b"
)
db_cursor = db_connection.cursor()


# Function to add new student
def add_new_student():
    name = name_entry.get()
    age = age_entry.get()
    parent_details = parent_details_entry.get()
    address = address_entry.get()
    mobile_number = mobile_number_entry.get()
    gender = gender_var.get()
    school_details = school_details_entry.get()
    course = course_entry.get()
    year = year_entry.get()

    try:
        age = int(age)
        mobile_number = int(mobile_number)

        # Inserting student data into the database
        sql = "INSERT INTO students (name, age, parent_details, address, mobile_number, gender, school_details, current_course, year) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        val = (name, age, parent_details, address, mobile_number, gender, school_details, course, year)
        db_cursor.execute(sql, val)
        db_connection.commit()
        messagebox.showinfo("Success", "New student added successfully!")
    except ValueError:
        messagebox.showerror("Error", "Age and mobile number must be integers!")


# Function to view student details
def view_student_details():
    student_id = simpledialog.askinteger("Student ID", "Enter Student ID:")
    if student_id is not None:
        try:
            sql = "SELECT * FROM students WHERE id = %s"
            db_cursor.execute(sql, (student_id,))
            student_record = db_cursor.fetchone()
            if student_record:
                show_student_info(student_record)
            else:
                messagebox.showerror("Error", "Student not found!")
        except ValueError:
            messagebox.showerror("Error", "Student ID must be an integer!")


# Function to delete student record
def delete_student_record():
    student_id = simpledialog.askinteger("Student ID", "Enter Student ID:")
    if student_id is not None:
        try:
            sql = "DELETE FROM students WHERE id = %s"
            db_cursor.execute(sql, (student_id,))
            db_connection.commit()
            messagebox.showinfo("Success", "Student record deleted successfully!")
        except ValueError:
            messagebox.showerror("Error", "Student ID must be an integer!")


# Function to display student information in a new window
def show_student_info(student_info):
    info_window = tk.Toplevel(root)
    info_window.title("Student Information")

    labels = ["ID", "Name", "Age", "Parent Details", "Address", "Mobile Number", "Gender", "School Details", "Course",
              "Year"]

    for i, label in enumerate(labels):
        tk.Label(info_window, text=f"{label}:").grid(row=i, column=0, sticky="w")
        tk.Label(info_window, text=student_info[i]).grid(row=i, column=1, sticky="w")


# Function to view student's current course
def view_student_current_course():
    student_id = simpledialog.askinteger("Student ID", "Enter Student ID:")
    if student_id is not None:
        try:
            sql = "SELECT current_course FROM students WHERE id = %s"
            db_cursor.execute(sql, (student_id,))
            current_course = db_cursor.fetchone()
            if current_course:
                course_window = tk.Toplevel(root)
                course_window.title("Student's Current Course")
                tk.Label(course_window, text="Student's current course:").pack()
                tk.Label(course_window, text=current_course[0]).pack()
            else:
                messagebox.showerror("Error", "Student not found!")
        except ValueError:
            messagebox.showerror("Error", "Student ID must be an integer!")


# Function to view student's past courses
def view_student_past_courses():
    student_id = simpledialog.askinteger("Student ID", "Enter Student ID:")
    if student_id is not None:
        try:
            sql = "SELECT past_course FROM students WHERE id = %s"
            db_cursor.execute(sql, (student_id,))
            past_courses = db_cursor.fetchone()
            if past_courses:
                past_courses_window = tk.Toplevel(root)
                past_courses_window.title("Student's Past Courses")
                tk.Label(past_courses_window, text=f"Past courses for student ID {student_id}:").pack()
                tk.Label(past_courses_window, text=past_courses[0]).pack()
            else:
                messagebox.showinfo("Information", f"No past courses found for student ID {student_id}")
        except ValueError:
            messagebox.showerror("Error", "Student ID must be an integer!")


# Function to search student by name
def search_student_by_name():
    name = simpledialog.askstring("Student Name", "Enter Student Name:")
    if name:
        try:
            sql = "SELECT * FROM students WHERE name = %s"
            val = (name,)
            db_cursor.execute(sql, val)
            student_records = db_cursor.fetchall()
            if student_records:
                result_window = tk.Toplevel(root)
                result_window.title("Search Results")
                for i, student in enumerate(student_records):
                    tk.Label(result_window, text=f"Student {i + 1}").grid(row=i, column=0, sticky="w")
                    for j, data in enumerate(student):
                        tk.Label(result_window, text=f"{data}").grid(row=i, column=j + 1, sticky="w")
            else:
                messagebox.showinfo("Information", f"No student found with the name '{name}'")
        except Exception as e:
            messagebox.showerror("Error", str(e))


# Function to search students by course
def search_students_by_course():
    current_course = simpledialog.askstring("Course", "Enter Course:")
    if current_course:
        try:
            sql = "SELECT name FROM students WHERE current_course = %s"
            val = (current_course,)
            db_cursor.execute(sql, val)
            student_records = db_cursor.fetchall()
            if student_records:
                result_window = tk.Toplevel(root)
                result_window.title("Search Results")
                for i, student in enumerate(student_records):
                    tk.Label(result_window, text=f"Student {i + 1}").grid(row=i, column=0, sticky="w")
                    tk.Label(result_window, text=f"{student[0]}").grid(row=i, column=1, sticky="w")
            else:
                messagebox.showinfo("Information", f"No students found for the course '{current_course}'")
        except Exception as e:
            messagebox.showerror("Error", str(e))


# Function to add new teacher
def add_new_teacher():
    name = simpledialog.askstring("Teacher Name", "Enter Teacher Name:")
    address = simpledialog.askstring("Teacher Address", "Enter Teacher Address:")
    mobile_number = simpledialog.askstring("Mobile Number", "Enter Mobile Number:")
    gender = simpledialog.askstring("Gender", "Enter Gender:")
    course_can_teach1 = simpledialog.askstring("Course Can Teach 1", "Enter Course Can Teach 1:")
    course_can_teach2 = simpledialog.askstring("Course Can Teach 2", "Enter Course Can Teach 2:")

    try:
        mobile_number = str(mobile_number)
        if len(mobile_number) != 10:
            messagebox.showerror("Error", "Mobile number must be 10 digits long!")
            return
        mobile_number = int(mobile_number)

        sql = "INSERT INTO teachers (name, address, mobile_number, gender, course_can_teach1, course_can_teach2) VALUES (%s, %s, %s, %s, %s, %s)"
        val = (name, address, mobile_number, gender, course_can_teach1, course_can_teach2)
        db_cursor.execute(sql, val)
        db_connection.commit()
        messagebox.showinfo("Success", "New teacher added successfully!")
    except ValueError:
        messagebox.showerror("Error", "Mobile number must be numeric!")


# Function to view teacher details
def view_teacher_details():
    teacher_id = simpledialog.askinteger("Teacher ID", "Enter Teacher ID:")
    if teacher_id is not None:
        try:
            teacher_id = int(teacher_id)
            sql = "SELECT * FROM teachers WHERE id=%s"
            db_cursor.execute(sql, (teacher_id,))
            teacher_records = db_cursor.fetchall()
            if teacher_records:
                result_window = tk.Toplevel(root)
                result_window.title("Teacher Details")
                for i, teacher in enumerate(teacher_records):
                    tk.Label(result_window, text=f"Teacher {i + 1}").grid(row=i, column=0, sticky="w")
                    for j, data in enumerate(teacher):
                        tk.Label(result_window, text=f"{data}").grid(row=i, column=j + 1, sticky="w")
            else:
                messagebox.showinfo("Information", f"No teacher found with ID {teacher_id}")
        except ValueError:
            messagebox.showerror("Error", "Teacher ID must be an integer!")


# Function to delete teacher record
def delete_teacher_record():
    teacher_id = simpledialog.askinteger("Teacher ID", "Enter Teacher ID:")
    if teacher_id is not None:
        try:
            teacher_id = int(teacher_id)
            # Assuming worked more than 1 month means they have taught at least one course
            sql = "DELETE FROM teachers WHERE id = %s"
            val = (teacher_id,)
            db_cursor.execute(sql, val)
            db_connection.commit()
            messagebox.showinfo("Success", "Teacher record deleted successfully!")
        except ValueError:
            messagebox.showerror("Error", "Teacher ID must be an integer!")


# Function to view teacher's past courses
def view_teacher_past_courses():
    teacher_id = simpledialog.askinteger("Teacher ID", "Enter Teacher ID:")
    if teacher_id is not None:
        try:
            teacher_id = int(teacher_id)
            sql = "SELECT past_course FROM teachers WHERE id = %s"
            val = (teacher_id,)
            db_cursor.execute(sql, val)
            past_courses = db_cursor.fetchone()
            if past_courses:
                past_courses_window = tk.Toplevel(root)
                past_courses_window.title("Teacher's Past Courses")
                tk.Label(past_courses_window, text=f"Past courses for teacher ID {teacher_id}:").pack()
                tk.Label(past_courses_window, text=past_courses[0]).pack()
            else:
                messagebox.showinfo("Information", f"No past courses found for teacher ID {teacher_id}")
        except ValueError:
            messagebox.showerror("Error", "Teacher ID must be an integer!")


# Function to search teacher by name
def search_teacher_by_name():
    name = simpledialog.askstring("Teacher Name", "Enter Teacher Name:")
    if name:
        try:
            sql = "SELECT * FROM teachers WHERE name LIKE %s"
            val = ('%' + name + '%',)
            db_cursor.execute(sql, val)
            teacher_records = db_cursor.fetchall()
            if teacher_records:
                result_window = tk.Toplevel(root)
                result_window.title("Search Results")
                for i, teacher in enumerate(teacher_records):
                    tk.Label(result_window, text=f"Teacher {i + 1}").grid(row=i, column=0, sticky="w")
                    for j, data in enumerate(teacher):
                        tk.Label(result_window, text=f"{data}").grid(row=i, column=j + 1, sticky="w")
            else:
                messagebox.showinfo("Information", f"No teacher found with the name '{name}'")
        except Exception as e:
            messagebox.showerror("Error", str(e))


# Function to search teacher by course
def search_teacher_by_course():
    course = simpledialog.askstring("Course", "Enter Course:")
    if course:
        try:
            sql = "SELECT name FROM teachers WHERE course_can_teach1 = %s"
            val = (course,)
            db_cursor.execute(sql, val)
            teacher_records = db_cursor.fetchall()
            if teacher_records:
                result_window = tk.Toplevel(root)
                result_window.title("Search Results")
                for i, teacher in enumerate(teacher_records):
                    tk.Label(result_window, text=f"Teacher {i + 1}").grid(row=i, column=0, sticky="w")
                    tk.Label(result_window, text=f"{teacher[0]}").grid(row=i, column=1, sticky="w")
            else:
                messagebox.showinfo("Information", f"No teacher found for the course '{course}'")
        except Exception as e:
            messagebox.showerror("Error", str(e))


def update_student_current_course():
    student_id = simpledialog.askinteger("Student ID", "Enter Student ID:")
    new_course = simpledialog.askstring("New Course", "Enter New Course:")

    if student_id is not None and new_course:
        try:
            student_id = int(student_id)
            # Get the current course of the student
            sql_get_current_course = "SELECT current_course FROM students WHERE id = %s"
            db_cursor.execute(sql_get_current_course, (student_id,))
            current_course_result = db_cursor.fetchone()

            # Check if the student exists and is in the first year
            if current_course_result:
                current_course = current_course_result[0]
                if current_course != new_course:
                    # Update the current course and move the previous current course to past courses
                    sql_update_current_course = "UPDATE students SET past_course = CONCAT(IFNULL(past_course, ''), ', ', %s), current_course = %s WHERE id = %s AND year = 1"
                    val = (current_course, new_course, student_id)
                    db_cursor.execute(sql_update_current_course, val)
                    db_connection.commit()

                    if db_cursor.rowcount > 0:
                        messagebox.showinfo("Success", "Student's current course updated successfully!")
                    else:
                        messagebox.showinfo("Information", "Student not found or not in first year!")
                else:
                    messagebox.showinfo("Information", "New course is the same as the current course.")
            else:
                messagebox.showinfo("Information", "Student not found!")
        except ValueError:
            messagebox.showerror("Error", "Student ID must be an integer!")

def update_teacher_information():
    teacher_id = simpledialog.askinteger("Teacher ID", "Enter Teacher ID:")
    new_address = simpledialog.askstring("New Address", "Enter New Address:")
    new_mobile_number = simpledialog.askinteger("New Mobile Number", "Enter New Mobile Number:")
    new_course = simpledialog.askstring("New Course", "Enter New Course:")

    if teacher_id is not None and new_address and new_mobile_number is not None and new_course:
        try:
            teacher_id = int(teacher_id)
            new_mobile_number = str(new_mobile_number)
            if len(new_mobile_number) != 10:
                messagebox.showerror("Error", "Mobile number must be 10 digits long!")
                return
            new_mobile_number = int(new_mobile_number)

            # Fetch the current values
            sql_fetch_current_values = "SELECT course_can_teach1, past_course FROM teachers WHERE id = %s"
            db_cursor.execute(sql_fetch_current_values, (teacher_id,))
            current_values = db_cursor.fetchone()

            if current_values:
                current_course1, current_past_courses = current_values
            else:
                messagebox.showinfo("Information", "Teacher not found!")
                return

            # Update past_course with the current value of course_can_teach1
            updated_past_courses = current_past_courses + " " + current_course1

            # Update the teacher information
            sql_update_teacher_info = "UPDATE teachers SET address = %s, mobile_number = %s, course_can_teach1 = %s, past_course = %s WHERE id = %s"
            val = (new_address, new_mobile_number, new_course, updated_past_courses, teacher_id)
            db_cursor.execute(sql_update_teacher_info, val)
            db_connection.commit()
            messagebox.showinfo("Success", "Teacher information updated successfully!")

        except ValueError:
            messagebox.showerror("Error", "Teacher ID must be an integer!")

def list_teachers_by_criteria(gender=None, course=None):
    if gender is None:
        gender = simpledialog.askstring("Gender", "Enter gender (optional, leave blank to ignore): ")
    if course is None:
        course = simpledialog.askstring("Course", "Enter course (optional, leave blank to ignore): ")

    sql = "SELECT * FROM teachers"
    conditions = []

    if gender:
        conditions.append("gender = %s")
    if course:
        conditions.append("course_can_teach1 = %s OR course_can_teach1 = %s")

    if conditions:
        sql += " WHERE " + " AND ".join(conditions)

    val = tuple(filter(None, [gender, course, course]))
    db_cursor.execute(sql, val)
    teacher_records = db_cursor.fetchall()

    result_window = tk.Toplevel(root)
    result_window.title("Teachers List")
    for i, teacher in enumerate(teacher_records):
        tk.Label(result_window, text=f"Teacher {i + 1}").grid(row=i, column=0, sticky="w")
        for j, data in enumerate(teacher):
            tk.Label(result_window, text=f"{data}").grid(row=i, column=j + 1, sticky="w")

def list_students_by_criteria(course=None, year=None, gender=None):
    if course is None:
        course = simpledialog.askstring("Course", "Enter course (optional, leave blank to ignore): ")
    if year is None:
        year = simpledialog.askinteger("Year", "Enter year (optional, leave blank to ignore): ")
    if gender is None:
        gender = simpledialog.askstring("Gender", "Enter gender (optional, leave blank to ignore): ")

    sql = "SELECT * FROM students WHERE 1=1"  # Always true to avoid syntax issues
    conditions = []
    val = []

    if course:
        conditions.append("current_course = %s")
        val.append(course)
    if year:
        conditions.append("year = %s")
        val.append(year)
    if gender:
        conditions.append("gender = %s")
        val.append(gender)

    if conditions:
        sql += " AND " + " AND ".join(conditions)

    db_cursor.execute(sql, val)
    student_records = db_cursor.fetchall()

    result_window = tk.Toplevel(root)
    result_window.title("Students List")
    for i, student in enumerate(student_records):
        tk.Label(result_window, text=f"Student {i + 1}").grid(row=i, column=0, sticky="w")
        for j, data in enumerate(student):
            tk.Label(result_window, text=f"{data}").grid(row=i, column=j + 1, sticky="w")


def update_student_information():
    student_id = simpledialog.askinteger("Student ID", "Enter Student ID:")
    if student_id is not None:
        new_age = simpledialog.askinteger("New Age", "Enter New Age:")
        new_parent_details = simpledialog.askstring("New Parent Details", "Enter New Parent Details:")
        new_address = simpledialog.askstring("New Address", "Enter New Address:")
        new_mobile_number = simpledialog.askstring("New Mobile Number", "Enter New Mobile Number:")
        new_school_details = simpledialog.askstring("New School Details", "Enter New School Details:")
        new_course = simpledialog.askstring("New Course", "Enter New Course:")
        year = simpledialog.askinteger("Year", "Enter Year:")

        try:
            student_id = int(student_id)
            new_age = int(new_age)
            new_mobile_number = str(new_mobile_number)
            if len(new_mobile_number) != 10:
                messagebox.showerror("Error", "Mobile number must be 10 digits long!")
                return
            new_mobile_number = int(new_mobile_number)

            # Fetching the current_course, past_course, and year of the student
            db_cursor.execute("SELECT current_course, past_course, year FROM students WHERE id = %s", (student_id,))
            result = db_cursor.fetchone()
            current_course, past_course, student_year = result[0], result[1], result[2]

            # Check if the student is in the first year
            if student_year == 1:
                # Updating the student information
                sql = ("UPDATE students SET age = %s, parent_details = %s, address = %s, "
                       "mobile_number = %s, school_details = %s, current_course = %s WHERE id = %s")
                val = (new_age, new_parent_details, new_address, new_mobile_number, new_school_details, new_course,
                       student_id)
                db_cursor.execute(sql, val)

                # Adding current course to past courses
                if past_course is None:
                    past_course = current_course
                else:
                    past_course += ", " + current_course
                sql_add_past_course = "UPDATE students SET past_course = %s WHERE id = %s"
                db_cursor.execute(sql_add_past_course, (past_course, student_id))

                db_connection.commit()
                messagebox.showinfo("Success", "Student information updated successfully!")
            else:
                messagebox.showerror("Error", "Cannot update student information. Only first-year students are eligible.")
        except ValueError:
            messagebox.showerror("Error", "Student ID and age must be integers. Mobile number must be numeric and 10 digits long!")



# GUI setup
root = tk.Tk()
root.title("Student Management System")

tk.Label(root, text="Name:").grid(row=0, column=0, sticky="w")
tk.Label(root, text="Age:").grid(row=1, column=0, sticky="w")
tk.Label(root, text="Parent Details:").grid(row=2, column=0, sticky="w")
tk.Label(root, text="Address:").grid(row=3, column=0, sticky="w")
tk.Label(root, text="Mobile Number:").grid(row=4, column=0, sticky="w")
tk.Label(root, text="Gender:").grid(row=5, column=0, sticky="w")
tk.Label(root, text="School Details:").grid(row=6, column=0, sticky="w")
tk.Label(root, text="Course:").grid(row=7, column=0, sticky="w")
tk.Label(root, text="Year:").grid(row=8, column=0, sticky="w")

# Entry fields
name_entry = tk.Entry(root)
name_entry.grid(row=0, column=1)
age_entry = tk.Entry(root)
age_entry.grid(row=1, column=1)
parent_details_entry = tk.Entry(root)
parent_details_entry.grid(row=2, column=1)
address_entry = tk.Entry(root)
address_entry.grid(row=3, column=1)
mobile_number_entry = tk.Entry(root)
mobile_number_entry.grid(row=4, column=1)
gender_var = tk.StringVar(root)
gender_var.set("Male")
gender_menu = tk.OptionMenu(root, gender_var, "Male", "Female", "Other")
gender_menu.grid(row=5, column=1)
school_details_entry = tk.Entry(root)
school_details_entry.grid(row=6, column=1)
course_entry = tk.Entry(root)
course_entry.grid(row=7, column=1)
year_entry = tk.Entry(root)
year_entry.grid(row=8, column=1)

# Buttons
add_button = tk.Button(root, text="Add Student", command=add_new_student)
add_button.grid(row=9, column=0, columnspan=2)

view_button = tk.Button(root, text="View Student Details", command=view_student_details)
view_button.grid(row=11, column=0, columnspan=2)

delete_button = tk.Button(root, text="Delete Student Record", command=delete_student_record)
delete_button.grid(row=12, column=0, columnspan=2)

# New labels and buttons for search functions
tk.Label(root, text="Search Students by Name:").grid(row=13, column=0, sticky="w")
search_name_button = tk.Button(root, text="Search", command=search_student_by_name)
search_name_button.grid(row=13, column=1, columnspan=2)

tk.Label(root, text="Search Students by Course:").grid(row=14, column=0, sticky="w")
search_course_button = tk.Button(root, text="Search", command=search_students_by_course)
search_course_button.grid(row=14, column=1, columnspan=2)

# New labels and buttons for teacher functions
tk.Label(root, text="Add New Teacher:").grid(row=15, column=0, sticky="w")
add_teacher_button = tk.Button(root, text="Add Teacher", command=add_new_teacher)
add_teacher_button.grid(row=15, column=1, columnspan=2)

tk.Label(root, text="View Teacher Details:").grid(row=16, column=0, sticky="w")
view_teacher_button = tk.Button(root, text="View Teacher Details", command=view_teacher_details)
view_teacher_button.grid(row=16, column=1, columnspan=2)

tk.Label(root, text="Delete Teacher Record:").grid(row=17, column=0, sticky="w")
delete_teacher_button = tk.Button(root, text="Delete Teacher Record", command=delete_teacher_record)
delete_teacher_button.grid(row=17, column=1, columnspan=2)

tk.Label(root, text="View Teacher Past Courses:").grid(row=18, column=0, sticky="w")
view_teacher_past_button = tk.Button(root, text="View Teacher Past Courses", command=view_teacher_past_courses)
view_teacher_past_button.grid(row=18, column=1, columnspan=2)

tk.Label(root, text="Search Teacher by Name:").grid(row=19, column=0, sticky="w")
search_teacher_name_button = tk.Button(root, text="Search", command=search_teacher_by_name)
search_teacher_name_button.grid(row=19, column=1, columnspan=2)

tk.Label(root, text="Search Teacher by Course:").grid(row=20, column=0, sticky="w")
search_teacher_course_button = tk.Button(root, text="Search", command=search_teacher_by_course)
search_teacher_course_button.grid(row=20, column=1, columnspan=2)

update_course_button = tk.Button(root, text="Update Student Current Course", command=update_student_current_course)
update_course_button.grid(row=21, column=0, columnspan=2)

# Button to update teacher information
update_info_button = tk.Button(root, text="Update Teacher Information", command=update_teacher_information)
update_info_button.grid(row=22, column=0, columnspan=2)

# New labels and buttons for teacher management
tk.Label(root, text="List Teachers by Criteria:").grid(row=23, column=0, sticky="w")
list_teachers_button = tk.Button(root, text="List Teachers", command=list_teachers_by_criteria)
list_teachers_button.grid(row=23, column=1, columnspan=2)

tk.Label(root, text="List Students by Criteria:").grid(row=24, column=0, sticky="w")
list_students_button = tk.Button(root, text="List Students", command=list_students_by_criteria)
list_students_button.grid(row=24, column=1, columnspan=2)

update_info_button = tk.Button(root, text="Update Student Information", command=update_student_information)
update_info_button.grid(row=25, column=0, columnspan=2)


root.mainloop()
