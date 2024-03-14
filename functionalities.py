from validation import *
import mysql.connector
from main import *

# Establishing connection to MySQL database
db_connection = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="Veena@12345",
    database="sms3b"
)
db_cursor = db_connection.cursor()


# List of courses for teachers
courses = ["Science", "Maths", "Biology", "Physics", "Chemistry"]

def add_new_student(name, age, parent_details, address, mobile_number, gender, school_details,
                    current_course, year,courses=None):

    try:
        age = validate_age(age)
        mobile_number = validate_mobile_number(mobile_number)
        gender = validate_gender(gender)
        name = validate_student_name(name)

        # Checking if the input values are of the correct data types
        age = int(age)
        mobile_number = str(mobile_number)
        if len(mobile_number) != 10:
            print("Mobile number must be 10 digits long!")
            return
        mobile_number = int(mobile_number)

        # Check if the current_course is one of the available courses
        if current_course not in courses:
            raise ValueError("Invalid course! Please select from the available courses.")

        # Inserting the new student into the database
        sql = "INSERT INTO students (name, age, parent_details, address, mobile_number, gender, school_details, current_course, year) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        val = (name, age, parent_details, address, mobile_number, gender, school_details, current_course, year)
        db_cursor.execute(sql, val)
        db_connection.commit()
        print("New student added successfully!")
    except ValueError as e:
        print("Error:", e)


def update_student_information(student_id, new_age, new_parent_details, new_address, new_mobile_number,
                               new_school_details, new_course, year):
    try:
        student_id = validate_student_id(student_id)
        new_age = validate_age(new_age)
        new_mobile_number = validate_mobile_number(new_mobile_number)

        # Fetching the current_course, past_course, and year of the student
        db_cursor.execute("SELECT current_course, past_course, year FROM students WHERE id = %s", (student_id,))
        result = db_cursor.fetchone()
        current_course, past_course, student_year = result[0], result[1], result[2]

        # Check if the student is in the first year
        if student_year == 1:
            # Updating the student information
            sql = ("UPDATE students SET age = %s, parent_details = %s, address = %s, "
                   "mobile_number = %s, school_details = %s, current_course = %s , year = %s WHERE id = %s")
            val = (new_age, new_parent_details, new_address, new_mobile_number, new_school_details, new_course,
                   year, student_id)
            db_cursor.execute(sql, val)

            # Adding current course to past courses
            if past_course is None:
                past_course = current_course
            else:
                past_course += ", " + current_course
            sql_add_past_course = "UPDATE students SET past_course = %s WHERE id = %s"
            db_cursor.execute(sql_add_past_course, (past_course, student_id))

            db_connection.commit()
            print("Student information updated successfully!")
        else:
            print("Cannot update student information. Only first-year students are eligible.")
    except ValueError:
        print("Student ID and age must be integers. Mobile number must be numeric and 10 digits long!")


def view_student_details(student_id):
    try:
        student_id = validate_student_id(student_id)
        sql = "SELECT * FROM students WHERE id = %s"
        db_cursor.execute(sql, (student_id,))
        student_record = db_cursor.fetchone()
        if student_record:
            print(student_record)
        else:
            print("Student not found!")
    except ValueError as e:
        print("Error:", e)


# Function to delete student record
# Function to delete student record (Soft delete)
def delete_student_record(student_id):
    try:
        student_id = validate_student_id(student_id)
        sql = "DELETE FROM students WHERE id = %s"
        val = (student_id,)
        db_cursor.execute(sql, val)
        db_connection.commit()
        print("Student record deleted successfully!")
    except ValueError as e:
        print("Error:", e)


# Function to list students by criteria
def list_students_by_criteria(course=None, year=None, gender=None):
    if course is None:
        course = input("Enter course (optional, leave blank to ignore): ")
    if year is None:
        year = input("Enter year (optional, leave blank to ignore): ")
    if gender is None:
        gender = input("Enter gender (optional, leave blank to ignore): ")

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
    for student in student_records:
        print(student)


# Function to view student's current course
def view_student_current_course(student_id):
    try:
        student_id = validate_student_id(student_id)
        sql = "SELECT current_course FROM students WHERE id = %s"
        val = (student_id,)
        db_cursor.execute(sql, val)
        current_courses = db_cursor.fetchone()
        if current_courses:
            print("Student's current course:", current_courses[0])
        else:
            print("Student not found!")
    except ValueError as e:
        print("Error:", e)


# Function to update student's current course
# Function to update student's current course
# Function to update student's current course
def update_student_current_course(student_id, new_course):
    try:
        student_id = validate_student_id(student_id)
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
                    print("Student's current course updated successfully!")
                else:
                    print("Student not found or not in first year!")
            else:
                print("New course is the same as the current course.")
        else:
            print("Student not found!")
    except ValueError as e:
        print("Error:", e)


# Function to view student's past courses
def view_student_past_courses(student_id):
    try:
        student_id = validate_student_id(student_id)
        sql = "SELECT past_course FROM students WHERE id = %s"
        val = (student_id,)
        db_cursor.execute(sql, val)
        past_courses = db_cursor.fetchone()
        if past_courses:
            print("Past courses for student ID", student_id, ":")
            # Joining the elements of the tuple into a single string without commas
            print(''.join(map(str, past_courses)))
        else:
            print("No past courses found for student ID", student_id)
    except ValueError as e:
        print("Error:", e)


def search_student_by_name(name):
    sql = "SELECT * FROM students WHERE name = %s"
    val = (name,)  # Note the comma to create a single-element tuple
    db_cursor.execute(sql, val)
    student_records = db_cursor.fetchall()
    if student_records:
        for student in student_records:
            print(student)
    else:
        print("No student found with the name", name)


# Function to search student by course
def search_students_by_course(current_course):
    sql = "SELECT name FROM students WHERE current_course = %s"
    val = (current_course,)
    db_cursor.execute(sql, val)
    student_records = db_cursor.fetchall()
    if student_records:
        for student in student_records:
            print(student[0])  # Print each student's name individually
    else:
        print("No students found for the course", current_course)


# Function to view teacher details
def add_new_teacher(name, address, mobile_number, gender, course_can_teach1, course_can_teach2):
    try:
        mobile_number = validate_mobile_number(mobile_number)

        sql = "INSERT INTO teachers (name, address, mobile_number, gender, course_can_teach1, course_can_teach2) VALUES (%s, %s, %s, %s, %s, %s)"
        val = (name, address, mobile_number, gender, course_can_teach1, course_can_teach2)
        db_cursor.execute(sql, val)
        db_connection.commit()
        print("New teacher added successfully!")
    except ValueError as e:
        print("Error:", e)


def view_teacher_details(teacher_id):
    try:
        teacher_id = validate_teacher_id(teacher_id)
        sql = "SELECT * FROM teachers WHERE id=%s"
        db_cursor.execute(sql, (teacher_id,))
        teacher_records = db_cursor.fetchall()
        if teacher_records:
            print(teacher_records)
        else:
            print("Teacher not found!")
    except ValueError as e:
        print("Error:", e)


# Function to update teacher information

def update_teacher_information(teacher_id, new_address, new_mobile_number, new_course):
    try:
        teacher_id = validate_teacher_id(teacher_id)
        new_mobile_number = validate_mobile_number(new_mobile_number)

        # Fetch the current values
        sql_fetch_current_values = "SELECT address, mobile_number, course_can_teach1, course_can_teach2 FROM teachers WHERE id = %s"
        db_cursor.execute(sql_fetch_current_values, (teacher_id,))
        current_values = db_cursor.fetchone()

        # Update only if the new values are different from the current ones
        if current_values:
            current_address, current_mobile, current_course1, current_course2 = current_values
            if current_address != new_address or current_mobile != new_mobile_number or current_course1 != new_course:
                sql_update_teacher_info = "UPDATE teachers SET address = %s, mobile_number = %s, course_can_teach1 = %s WHERE id = %s"
                val = (new_address, new_mobile_number, new_course, teacher_id)
                db_cursor.execute(sql_update_teacher_info, val)
                db_connection.commit()
                print("Teacher information updated successfully!")
            else:
                print("No changes detected in teacher information.")
        else:
            print("Teacher not found!")
    except ValueError as e:
        print("Error:", e)


def delete_teacher_record(teacher_id):
    try:
        teacher_id = validate_teacher_id(teacher_id)
        sql = "DELETE FROM teachers WHERE id = %s"
        val = (teacher_id,)
        db_cursor.execute(sql, val)
        db_connection.commit()
        print("Teacher record deleted successfully!")
    except ValueError as e:
        print("Error:", e)


def list_teachers_by_criteria(course=None, gender=None):
    if course is None:
        course = input("Enter course (optional, leave blank to ignore): ")
    if gender is None:
        gender = input("Enter gender (optional, leave blank to ignore): ")

    sql = "SELECT * FROM teachers WHERE 1=1"  # Always true to avoid syntax issues
    conditions = []
    val = []

    if course:
        conditions.append("course_can_teach1 = %s OR course_can_teach2 = %s")
        val.extend([course, course])
    if gender:
        conditions.append("gender = %s")
        val.append(gender)

    if conditions:
        sql += " AND " + " AND ".join(conditions)

    db_cursor.execute(sql, val)
    teacher_records = db_cursor.fetchall()
    for teacher in teacher_records:
        print(teacher)


# Function to view teacher's past courses
def view_teacher_past_courses(teacher_id):
    try:
        teacher_id = validate_teacher_id(teacher_id)
        sql = "SELECT past_course FROM teachers WHERE id=%s"
        db_cursor.execute(sql, (teacher_id,))
        past_courses = db_cursor.fetchone()
        if past_courses:
            print("Past courses for teacher ID", teacher_id, ":")
            # Joining the elements of the tuple into a single string without commas
            print(''.join(map(str, past_courses)))
        else:
            print("No past courses found for teacher ID", teacher_id)
    except ValueError as e:
        print("Error:", e)


# Function to search teacher by name
def search_teacher_by_name(name):
    sql = "SELECT * FROM teachers WHERE name = %s"
    val = (name,)  # Note the comma to create a single-element tuple
    db_cursor.execute(sql, val)
    teacher_records = db_cursor.fetchall()
    if teacher_records:
        for teacher in teacher_records:
            print(teacher)
    else:
        print("No teacher found with the name", name)


# Function to search teacher by course
def search_teacher_by_course(course_can_teach):
    sql = "SELECT name FROM teachers WHERE course_can_teach1 = %s OR course_can_teach2 = %s"
    val = (course_can_teach, course_can_teach)
    db_cursor.execute(sql, val)
    teacher_records = db_cursor.fetchall()
    if teacher_records:
        for teacher in teacher_records:
            print(teacher[0])  # Print each teacher's name individually
    else:
        print("No teacher found for the course", course_can_teach)

