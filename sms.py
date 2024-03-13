import mysql.connector

# Establishing connection to MySQL database
db_connection = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="Veena@12345",
    database="sms3b"
)
db_cursor = db_connection.cursor()


# Function to display menu
def display_menu():
    print("Menu:")
    print("1. Student Operations")
    print("2. Teacher Operations")
    print("3. Exit")


# Function to display student operations menu
def display_student_menu():
    print("Student Operations:")
    print("1. Add new student")
    print("2. View student details")
    print("3. Update student information")
    print("4. Delete student record (Soft delete)")
    print("5. List all students by criteria")
    print("6. View student's current course")
    print("7. Update student's current course (Only for 1st year students)")
    print("8. View student's past courses")
    print("9. Search student by name")
    print("10. Search student by course")
    print("11. Back to main menu")


# Function to display teacher operations menu
def display_teacher_menu():
    print("Teacher Operations:")
    print("1. Add new teacher")
    print("2. View teacher details")
    print("3. Update teacher information (Name can't be updated)")
    print("4. Delete teacher record (Check if worked more than 1 Month) (Soft delete)")
    print("5. List all teachers (Separated by gender & course they teach)")
    print("6. View teacher's past courses (One teacher should teach at least 2 distinct courses)")
    print("7. Search teacher by name")
    print("8. Search teacher by course")
    print("9. Back to main menu")


# Function to view student details
def update_student_information(student_id, new_age, new_parent_details, new_address, new_mobile_number, new_school_details, new_course, new_year):
    try:
        student_id = int(student_id)
        new_mobile_number = str(new_mobile_number)
        if len(new_mobile_number) != 10:
            print("Mobile number must be 10 digits long!")
            return
        new_mobile_number = int(new_mobile_number)

        # Retrieve the current information of the student
        sql_get_current_info = "SELECT current_course, past_course, student_year FROM students WHERE id = %s"
        db_cursor.execute(sql_get_current_info, (student_id,))
        result = db_cursor.fetchone()

        if result is not None:
            current_course, past_course, student_year = result
        else:
            print("Student not found!")
            return

        # Update the student's information
        sql_update_student_info = "UPDATE students SET age = %s, parent_details = %s, address = %s, mobile_number = %s, school_details = %s, current_course = %s, student_year = %s, past_course = %s WHERE id = %s"
        val = (new_age, new_parent_details, new_address, new_mobile_number, new_school_details, new_course, new_year, current_course, student_id)
        db_cursor.execute(sql_update_student_info, val)
        db_connection.commit()
        print("Student information updated successfully!")

    except ValueError:
        print("Student ID must be an integer!")


def view_student_details(student_id):
    try:
        student_id = int(student_id)
        sql = "SELECT * FROM students WHERE id = %s"
        db_cursor.execute(sql, (student_id,))
        student_record = db_cursor.fetchone()
        if student_record:
            print(student_record)
        else:
            print("Student not found!")
    except ValueError:
        print("Student ID must be an integer!")


# Function to update student information
def update_student_information(student_id, new_age, new_parent_details, new_address, new_mobile_number,
                               new_school_details, new_course, year):
    try:
        student_id = int(student_id)
        new_age = int(new_age)
        new_mobile_number = str(new_mobile_number)
        if len(new_mobile_number) != 10:
            print("Mobile number must be 10 digits long!")
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
            val = (new_age, new_parent_details, new_address, new_mobile_number, new_school_details, new_course, student_id)
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


# Function to delete student record
# Function to delete student record (Soft delete)
def delete_student_record(student_id):
    try:
        student_id = int(student_id)
        sql = "DELETE FROM students WHERE id = %s"
        val = (student_id,)
        db_cursor.execute(sql, val)
        db_connection.commit()
        print("Student record deleted successfully!")
    except ValueError:
        print("Student ID must be an integer!")


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
        student_id = int(student_id)
        sql = "SELECT current_course FROM students WHERE id = %s"
        val = (student_id,)
        db_cursor.execute(sql, val)
        current_courses = db_cursor.fetchone()
        if current_courses:
            print("Student's current course:", current_courses[0])
        else:
            print("Student not found!")
    except ValueError:
        print("Student ID must be an integer!")


# Function to update student's current course
# Function to update student's current course
# Function to update student's current course
def update_student_current_course(student_id, new_course):
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
                    print("Student's current course updated successfully!")
                else:
                    print("Student not found or not in first year!")
            else:
                print("New course is the same as the current course.")
        else:
            print("Student not found!")
    except ValueError:
        print("Student ID must be an integer!")


# Function to view student's past courses
def view_student_past_courses(student_id):
    try:
        student_id = int(student_id)
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
    except ValueError:
        print("Student ID must be an integer!")


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
        mobile_number = str(mobile_number)
        if len(mobile_number) != 10:
            print("Mobile number must be 10 digits long!")
            return
        mobile_number = int(mobile_number)

        sql = "INSERT INTO teachers (name, address, mobile_number, gender, course_can_teach1, course_can_teach2) VALUES (%s, %s, %s, %s, %s, %s)"
        val = (name, address, mobile_number, gender, course_can_teach1, course_can_teach2)
        db_cursor.execute(sql, val)
        db_connection.commit()
        print("New teacher added successfully!")
    except ValueError:
        print("Mobile number must be numeric!")


def view_teacher_details(teacher_id):
    try:
        teacher_id = int(teacher_id)
        sql = "SELECT * FROM teachers WHERE id=%s"
        db_cursor.execute(sql, (teacher_id,))
        teacher_records = db_cursor.fetchall()
        if teacher_records:
            print(teacher_records)
        else:
            print("Teacher not found!")
    except ValueError:
        print("Teacher ID must be an integer!")


# Function to update teacher information

def update_teacher_information(teacher_id, new_address, new_mobile_number, new_course):
    try:
        teacher_id = int(teacher_id)
        new_mobile_number = str(new_mobile_number)
        if len(new_mobile_number) != 10:
            print("Mobile number must be 10 digits long!")
            return
        new_mobile_number = int(new_mobile_number)

        # Fetch the current values
        sql_fetch_current_values = "SELECT course_can_teach1, past_course FROM teachers WHERE id = %s"
        db_cursor.execute(sql_fetch_current_values, (teacher_id,))
        current_values = db_cursor.fetchone()

        if current_values:
            current_course1, current_past_courses = current_values
        else:
            print("Teacher not found!")
            return

        # Update past_course with the current value of course_can_teach1
        updated_past_courses = current_past_courses + " " +current_course1

        # Update the teacher information
        sql_update_teacher_info = "UPDATE teachers SET address = %s, mobile_number = %s, course_can_teach1 = %s, past_course = %s WHERE id = %s"
        val = (new_address, new_mobile_number, new_course, updated_past_courses, teacher_id)
        db_cursor.execute(sql_update_teacher_info, val)
        db_connection.commit()
        print("Teacher information updated successfully!")

    except ValueError:
        print("Teacher ID must be an integer!")


# Function to delete teacher record
def delete_teacher_record(teacher_id):
    try:
        teacher_id = int(teacher_id)
        # Assuming worked more than 1 month means they have taught at least one course
        sql = "DELETE FROM teachers WHERE id = %s"
        val = (teacher_id,)
        db_cursor.execute(sql, val)
        db_connection.commit()
        print("Teacher record deleted successfully!")
    except ValueError:
        print("Teacher ID must be an integer!")


# Function to list teachers by criteria
def list_teachers_by_criteria(gender=None, course=None):
    if gender is None:
        gender = input("Enter gender (optional, leave blank to ignore): ")
    if course is None:
        course = input("Enter course (optional, leave blank to ignore): ")

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
    for teacher in teacher_records:
        print(teacher)



# Function to view teacher's past courses
def view_teacher_past_courses(teacher_id):
    try:
        teacher_id = int(teacher_id)
        sql = "SELECT past_course FROM teachers WHERE id = %s"
        val = (teacher_id,)
        db_cursor.execute(sql, val)
        past_courses = db_cursor.fetchone()
        if past_courses:
            print("Past courses for teacher ID", teacher_id, ":")
            # Joining the elements of the tuple into a single string without commas
            print(''.join(map(str, past_courses)))
        else:
            print("No past courses found for teacher ID", teacher_id)
    except ValueError:
        print("Teacher ID must be an integer!")


# Function to search teacher by name
def search_teacher_by_name(name):
    sql = "SELECT * FROM teachers WHERE name LIKE %s"
    val = ('%' + name + '%',)
    db_cursor.execute(sql, val)
    teacher_records = db_cursor.fetchall()
    if teacher_records:
        for teacher in teacher_records:
            print(teacher)
    else:
        print("No teacher found with the name", name)


# Function to search teacher by course
def search_teacher_by_course(course):
    sql = "SELECT name FROM teachers WHERE course_can_teach1 = %s"
    val = (course,)
    db_cursor.execute(sql, val)
    teacher_records = db_cursor.fetchall()
    if teacher_records:
        for teacher in teacher_records:
            print(teacher[0])
    else:
        print("No teacher found for the course", course)

# Main function
courses = ["Science", "Maths", "Biology", "Physics", "Chemistry"]

def main():
    while True:
        display_menu()
        choice = input("Enter your choice: ")

        if choice == '1':
            while True:
                display_student_menu()
                student_choice = input("Enter your choice: ")
                if student_choice == '1':
                    # Add new student
                    name = input("Enter student's name: ")
                    age = input("Enter student's age: ")
                    parent_details = input("Enter parent details: ")
                    address = input("Enter student's address: ")
                    mobile_number = input("Enter student's mobile number: ")
                    gender = input("Enter student's gender (Male/Female/Other): ")
                    school_details = input("Enter school details: ")
                    course = input("Enter course: ")
                    year = input("Enter year: ")

                    add_new_student(name, age, parent_details, address, mobile_number, gender, school_details, course, year, courses)
                elif student_choice == '2':
                    student_id = input("Enter student ID: ")
                    view_student_details(student_id)
                elif student_choice == '3':
                    student_id = input("Enter student ID: ")
                    new_age = input("Enter new age: ")
                    new_parent_details = input("Enter new parent details: ")
                    new_address = input("Enter new address: ")
                    new_mobile_number = input("Enter new mobile number: ")
                    new_school_details = input("Enter new school details: ")
                    new_course = input("Enter new course: ")
                    new_year = input("Enter new year: ")
                    update_student_information(student_id, new_age, new_parent_details, new_address, new_mobile_number,
                                               new_school_details, new_course, new_year)
                elif student_choice == '4':
                    student_id = input("Enter student ID: ")
                    delete_student_record(student_id)
                    print("Student record deleted successfully!")
                elif student_choice == '5':
                    list_students_by_criteria()
                elif student_choice == '6':
                    student_id = input("Enter student ID: ")
                    view_student_current_course(student_id)
                elif student_choice == '7':
                    student_id = input("Enter student ID: ")
                    new_course = input("Enter new course: ")
                    update_student_current_course(student_id, new_course)
                elif student_choice == '8':
                    student_id = input("Enter student ID: ")
                    view_student_past_courses(student_id)
                elif student_choice == '9':
                    name = input("Enter student's name: ")
                    search_student_by_name(name)
                elif student_choice == '10':
                    course = input("Enter course: ")
                    search_students_by_course(course)
                elif student_choice == '11':
                    break
                else:
                    print("Invalid choice. Please enter a valid option.")

        elif choice == '2':
            while True:
                display_teacher_menu()
                teacher_choice = input("Enter your choice: ")
                if teacher_choice == '1':
                    name = input("Enter teacher's name: ")
                    address = input("Enter teacher's address: ")
                    mobile_number = input("Enter teacher's mobile number: ")
                    gender = input("Enter teacher's gender (Male/Female/Other): ")
                    course_can_teach1 = input("Enter first course teacher can teach: ")
                    course_can_teach2 = input("Enter second course teacher can teach: ")
                    add_new_teacher(name, address, mobile_number, gender, course_can_teach1, course_can_teach2)
                    pass
                elif teacher_choice == '2':
                    teacher_id = input("Enter teacher ID: ")
                    view_teacher_details(teacher_id)
                elif teacher_choice == '3':
                    teacher_id = input("Enter teacher ID: ")
                    new_address = input("Enter new address: ")
                    new_mobile_number = input("Enter new mobile number: ")
                    new_course = input("Enter new course: ")
                    update_teacher_information(teacher_id, new_address, new_mobile_number, new_course)
                elif teacher_choice == '4':
                    teacher_id = input("Enter teacher ID: ")
                    delete_teacher_record(teacher_id)
                elif teacher_choice == '5':
                    list_teachers_by_criteria()
                elif teacher_choice == '6':
                    teacher_id = input("Enter teacher ID: ")
                    view_teacher_past_courses(teacher_id)
                elif teacher_choice == '7':
                    name = input("Enter teacher's name: ")
                    search_teacher_by_name(name)
                elif teacher_choice == '8':
                    course = input("Enter course: ")
                    search_teacher_by_course(course)
                elif teacher_choice == '9':
                    break
                else:
                    print("Invalid choice. Please enter a valid option.")

        elif choice == '3':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please enter a valid option.")

    # Closing connection
    db_connection.close()


if __name__ == "__main__":
    main()
