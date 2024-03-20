from validation import *
import mysql.connector
from main import *
import csv
from validation import *



# Establishing connection to MySQL database
db_connection = mysql.connector.connect(
   host="localhost",
   user="root",
   passwd="Veena@12345",
   database="sms3d"
)
db_cursor = db_connection.cursor()

courses = ["Zoology", "Maths", "Biology", "Physics", "Chemistry"]

# Function to add a new student
def add_new_student(courses=None):
   while True:
      try:
         # Prompt user for student details
         name = input("Enter student name: ")
         name = validate_student_name(name)

         age = None
         while age is None:
            age_input = input("Enter student age: ")
            try:
               age = validate_age(age_input)
            except ValueError as e:
               print("Error:", e)

         parent_details = input("Enter parent name: ")

         address = input("Enter address: ")

         mobile_number = None
         while mobile_number is None:
            mobile_number_input = input("Enter mobile number(should start from 6,7,8 or 9): ")
            try:
               mobile_number = validate_mobile_number(mobile_number_input)
            except ValueError as e:
               print("Error:", e)

         gender = None
         while gender is None:
            gender_input = input("Enter gender(male/female/others): ")
            try:
               gender = validate_gender(gender_input)
            except ValueError as e:
               print("Error:", e)

         school_details = input("Enter school name: ")

         current_course = None
         while current_course is None:
            course_input = input("Enter current course (Courses:Zoology, Maths, Biology, Physics, Chemistry): ")
            if course_input in courses:
               current_course = course_input
            else:
               print("Invalid course! Please select from the available courses.")

         year = input("Enter year: ")

         # Inserting the new student into the database
         sql = "INSERT INTO students (name, age, parent_details, address, mobile_number, gender, school_details, current_course, year) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
         val = (name, age, parent_details, address, mobile_number, gender, school_details, current_course, year)
         db_cursor.execute(sql, val)
         db_connection.commit()
         print("New student added successfully!")
         break  # Break out of the loop once all inputs are valid and added to the database
      except ValueError as e:
         print("Error:", e)


def update_student_information(db_cursor, db_connection):
   while True:
      try:
         student_id = input("Enter student ID: ")
         student_id = validate_student_id(student_id)

         while True:
            new_age = input("Enter new age: ")
            try:
               new_age = validate_age(new_age)
               break
            except ValueError as e:
               print("Error:", e)

         new_address = input("Enter new address: ")

         while True:
            new_mobile_number = input("Enter new mobile number(should start from 6,7,8 or 9): ")
            try:
               new_mobile_number = validate_mobile_number(new_mobile_number)
               break
            except ValueError as e:
               print("Error:", e)

         new_school_details = input("Enter new school name: ")

         new_course = None
         while new_course is None:
            course_input = input("Enter new course (Courses:Zoology, Maths, Biology, Physics, Chemistry): ")
            if course_input in courses:
               new_course = course_input
            else:
               print("Invalid course! Please select from the available courses.")

         year = input("Enter year: ")

         # Fetching the current_course, past_course, and year of the student
         db_cursor.execute("SELECT current_course, past_course, year FROM students WHERE id = %s and is_deleted=0", (student_id,))
         result = db_cursor.fetchone()
         current_course, past_course, student_year = result[0], result[1], result[2]

         # Check if the student is in the first year
         if student_year == 1:
            # Updating the student information
            sql = ("UPDATE students SET age = %s, address = %s, "
                   "mobile_number = %s, school_details = %s, current_course = %s , year = %s WHERE id = %s")
            val = (new_age, new_address, new_mobile_number, new_school_details, new_course,
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
            break  # Exit the loop if everything is successful
         else:
            print("Cannot update student information. Only first-year students are eligible.")
            break  # Exit the loop if there's an error
      except ValueError as e:
         print("Error:", e)


# Add your code for option 4 here
def view_student_details(student_id):
   while True:
      try:
         student_id = validate_student_id(student_id)
         sql = "SELECT * FROM students WHERE id = %s and is_deleted=0"
         db_cursor.execute(sql, (student_id,))
         student_record = db_cursor.fetchone()
         if student_record:
            print(student_record)
         else:
            print("Student not found!")
         break  # Exit the loop if everything is successful
      except ValueError as e:
         print("Error:", e)
         # Prompt for input again if there's an error
         student_id = input("Enter student ID: ")


def delete_student_record(student_id):
   while True:
      try:
         student_id = validate_student_id(student_id)
         sql = "UPDATE students SET is_deleted = TRUE WHERE id = %s"
         val = (student_id,)
         db_cursor.execute(sql, val)
         db_connection.commit()
         print("Student record soft-deleted successfully!")
         break  # Exit the loop if everything is successful
      except ValueError as e:
         print("Error:", e)
         # Prompt for input again if there's an error
         student_id = input("Enter student ID: ")

def list_students_by_criteria(course=None, year=None, gender=None):
   while True:
      try:
         if course is None:
            course = input("Enter course (optional, leave blank to ignore)/(Courses:Zoology, Maths, Biology, Physics, Chemistry): ")
         if year is None:
            year = input("Enter year (optional, leave blank to ignore): ")
         if gender is None:
            gender = input("Enter gender (optional, leave blank to ignore)/(male,female,others): ")

         sql = "SELECT * FROM students WHERE 1=1 and is_deleted=0"  # Always true to avoid syntax issues
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
         break  # Exit the loop if everything is successful
      except ValueError as e:
         print("Error:", e)


def view_student_current_course(student_id):
   while True:
      try:
         student_id = validate_student_id(student_id)
         sql = "SELECT current_course FROM students WHERE id = %s and is_deleted=0"
         val = (student_id,)
         db_cursor.execute(sql, val)
         current_courses = db_cursor.fetchone()
         if current_courses:
            print("Student's current course:", current_courses[0])
         else:
            print("Student not found!")
         break  # Exit the loop if everything is successful
      except ValueError as e:
         print("Error:", e)
         # Prompt for input again if there's an error
         student_id = input("Enter student ID: ")


def update_student_current_course():
    while True:
        try:
            student_id = input("Enter student ID: ")
            student_id = validate_student_id(student_id)

            new_course = input("Enter new course (Courses:Zoology, Maths, Biology, Physics, Chemistry): ")
            new_course = validate_course(new_course, allowed_courses=['Zoology', 'Chemistry', 'Maths', 'Biology','Physics',])  # Adjust allowed courses as needed

            # Get the current course of the student
            sql_get_current_course = "SELECT current_course FROM students WHERE id = %s and is_deleted=0"
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
            break  # Exit the loop if everything is successful
        except ValueError as e:
            print("Error:", e)


def view_student_past_courses(student_id):
   while True:
      try:
         student_id = validate_student_id(student_id)
         sql = "SELECT past_course FROM students WHERE id = %s and is_deleted=0"
         val = (student_id,)
         db_cursor.execute(sql, val)
         past_courses = db_cursor.fetchone()
         if past_courses:
            print("Past courses for student ID", student_id, ":")
            # Joining the elements of the tuple into a single string without commas
            print(''.join(map(str, past_courses)))
         else:
            print("No past courses found for student ID", student_id)
         break  # Exit the loop if everything is successful
      except ValueError as e:
         print("Error:", e)
         # Prompt for input again if there's an error
         student_id = input("Enter student ID: ")


def search_student_by_name(name):
   while True:
      try:
         sql = "SELECT * FROM students WHERE name = %s and is_deleted=0"
         val = (name,)  # Note the comma to create a single-element tuple
         db_cursor.execute(sql, val)
         student_records = db_cursor.fetchall()
         if student_records:
            for student in student_records:
               print(student)
         else:
            print("No student found with the name", name)
         break  # Exit the loop if everything is successful
      except ValueError as e:
         print("Error:", e)
         # Prompt for input again if there's an error
         name = input("Enter student name: ")


def search_students_by_course(current_course):
   while True:
      try:
         sql = "SELECT name FROM students WHERE current_course = %s and is_deleted=0"
         val = (current_course,)
         db_cursor.execute(sql, val)
         student_records = db_cursor.fetchall()
         if student_records:
            for student in student_records:
               print(student[0])  # Print each student's name individually
         else:
            print("No students found for the course", current_course)
         break  # Exit the loop if everything is successful
      except ValueError as e:
         print("Error:", e)
         # Prompt for input again if there's an error
         current_course = input("Enter current course: ")


def add_new_teacher():
   while True:
      try:
         name = input("Enter teacher name: ")
         # Validate name
         name = validate_student_name(name)

         address = input("Enter address: ")

         while True:
            try:
               mobile_number = input("Enter mobile number(should start from 6,7,8 or 9): ")
               # Validate mobile number
               mobile_number = validate_mobile_number(mobile_number)
               break  # Move to the next input field if mobile number is valid
            except ValueError as e:
               print("Error:", e)
               # Prompt for mobile number again if it's invalid

         while True:
            try:
               gender = input("Enter gender(male/female/others): ")
               # Validate gender
               gender = validate_gender(gender)
               break  # Move to the next input field if gender is valid
            except ValueError as e:
               print("Error:", e)
               # Prompt for gender again if it's invalid

         course_can_teach1 = input("Enter course can teach 1 (Courses:Zoology, Maths, Biology, Physics, Chemistry): ")
         course_can_teach2 = input("Enter course can teach 2 (Courses:Zoology, Maths, Biology, Physics, Chemistry): ")

         # Insert data into the database
         sql = "INSERT INTO teachers (name, address, mobile_number, gender, course_can_teach1, course_can_teach2) VALUES (%s, %s, %s, %s, %s, %s)"
         val = (name, address, mobile_number, gender, course_can_teach1, course_can_teach2)
         db_cursor.execute(sql, val)
         db_connection.commit()
         print("New teacher added successfully!")
         break  # Exit the loop if everything is successful
      except ValueError as e:
         print("Error:", e)
         # Continue the loop to re-enter the current invalid input
         continue


def view_teacher_details(teacher_id):
   while True:
      try:
         teacher_id = validate_teacher_id(teacher_id)
         sql = "SELECT * FROM teachers WHERE id=%s and is_deleted=0"
         db_cursor.execute(sql, (teacher_id,))
         teacher_records = db_cursor.fetchall()
         if teacher_records:
            print(teacher_records)
         else:
            print("Teacher not found!")
         break  # Exit the loop if everything is successful
      except ValueError as e:
         print("Error:", e)
         # Prompt for input again if there's an error
         teacher_id = input("Enter teacher ID: ")


def update_teacher_information():
    try:
        while True:
            teacher_id = input("Enter teacher's ID: ")
            try:
                teacher_id = int(teacher_id)
                if teacher_id <= 0:
                    raise ValueError("Teacher ID must be a positive integer.")
                break
            except ValueError as e:
                print("Invalid teacher ID:", e)

        new_address = input("Enter new address: ")

        while True:
            new_mobile_number = input("Enter new mobile number(should start from 6,7,8 or 9): ")
            try:
                new_mobile_number = validate_mobile_number(new_mobile_number)
                break
            except ValueError as e:
                print("Invalid mobile number:", e)

        new_course = input("Enter new course (Courses:Zoology, Maths, Biology, Physics, Chemistry): ")

        # Fetch the current values
        sql_fetch_current_values = "SELECT address, mobile_number, course_can_teach1, course_can_teach2, past_course FROM teachers WHERE id = %s and is_deleted=0"
        db_cursor.execute(sql_fetch_current_values, (teacher_id,))
        current_values = db_cursor.fetchone()

        # Update only if the new values are different from the current ones
        if current_values:
            current_address, current_mobile, current_course1, current_course2, past_course = current_values
            if current_address != new_address or current_mobile != new_mobile_number or current_course1 != new_course:
                # Update past courses
                if past_course:
                    past_course += ", " + current_course1
                else:
                    past_course = current_course1

                # Update the database
                sql_update_teacher_info = "UPDATE teachers SET address = %s, mobile_number = %s, course_can_teach1 = %s, course_can_teach2 = %s, past_course = %s WHERE id = %s"
                val = (new_address, new_mobile_number, new_course, current_course1, past_course, teacher_id)
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
   while True:
      try:
         teacher_id = validate_teacher_id(teacher_id)
         sql = "UPDATE teachers SET is_deleted = TRUE WHERE id = %s"
         val = (teacher_id,)
         db_cursor.execute(sql, val)
         db_connection.commit()
         print("Teacher record soft-deleted successfully!")
         break  # Exit the loop if everything is successful
      except ValueError as e:
         print("Error:", e)
         # Prompt for input again if there's an error
         teacher_id = input("Enter teacher ID: ")

def list_teachers_by_criteria(course=None, gender=None):
   while True:
      try:
         if course is None:
            course = input("Enter course (optional,leave blank to ignore)/(Courses:Zoology, Maths, Biology, Physics, Chemistry): ")
         if gender is None:
            gender = input("Enter gender (optional, leave blank to ignore)/(male,female,others): ")

         sql = "SELECT * FROM teachers WHERE 1=1 and is_deleted=0"  # Always true to avoid syntax issues
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
         break  # Exit the loop if everything is successful
      except ValueError as e:
         print("Error:", e)


def view_teacher_past_courses(teacher_id):
   while True:
      try:
         teacher_id = validate_teacher_id(teacher_id)
         sql = "SELECT past_course FROM teachers WHERE id=%s and is_deleted=0"
         db_cursor.execute(sql, (teacher_id,))
         past_courses = db_cursor.fetchone()
         if past_courses:
            print("Past courses for teacher ID", teacher_id, ":")
            # Joining the elements of the tuple into a single string without commas
            print(''.join(map(str, past_courses)))
         else:
            print("No past courses found for teacher ID", teacher_id)
         break  # Exit the loop if everything is successful
      except ValueError as e:
         print("Error:", e)
         # Prompt for input again if there's an error
         teacher_id = input("Enter teacher ID: ")


def search_teacher_by_name(name):
   while True:
      try:
         sql = "SELECT * FROM teachers WHERE name = %s and is_deleted=0"
         val = (name,)  # Note the comma to create a single-element tuple
         db_cursor.execute(sql, val)
         teacher_records = db_cursor.fetchall()
         if teacher_records:
            for teacher in teacher_records:
               print(teacher)
         else:
            print("No teacher found with the name", name)
         break  # Exit the loop if everything is successful
      except ValueError as e:
         print("Error:", e)
         # Prompt for input again if there's an error
         name = input("Enter teacher name: ")


def search_teacher_by_course(course_can_teach):
   while True:
      try:
         sql = "SELECT name FROM teachers WHERE course_can_teach1 = %s OR course_can_teach2 = %s and is_deleted=0"
         val = (course_can_teach, course_can_teach)
         db_cursor.execute(sql, val)
         teacher_records = db_cursor.fetchall()
         if teacher_records:
            for teacher in teacher_records:
               print(teacher[0])  # Print each teacher's name individually
         else:
            print("No teacher found for the course", course_can_teach)
         break  # Exit the loop if everything is successful
      except ValueError as e:
         print("Error:", e)
         # Prompt for input again if there's an error
         course_can_teach = input("Enter course can teach: ")





def export_table_to_csv(table_name, file_name):
  try:
      # Fetch data from the specified table
      sql = f"SELECT * FROM {table_name}"
      db_cursor.execute(sql)
      data = db_cursor.fetchall()
      # Get column names
      column_names = [i[0] for i in db_cursor.description]

      # Write data to CSV file
      with open(file_name, 'w', newline='') as csvfile:
          writer = csv.writer(csvfile)
          # Write column headers
          writer.writerow(column_names)
          # Write data rows
          writer.writerows(data)

      print(f"Data from table '{table_name}' exported to '{file_name}' successfully!")
  except Exception as e:
      print("Error:", e)

#for student data
def add_data_from_csv():
    try:
        file_path = input("Enter the path to the CSV file: ")
        with open(file_path, 'r') as csvfile:
            csv_reader = csv.reader(csvfile)
            next(csv_reader)  # Skip the header row
            for row in csv_reader:
                # Extract data from each row
                name, age, parent_details, address, mobile_number, gender, school_details, past_course, current_course, year, is_deleted = row

                # Insert the data into the database
                sql = "INSERT INTO students (name, age, parent_details, address, mobile_number, gender, school_details, past_course, current_course, year, is_deleted) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                val = (name, int(age), parent_details, address, int(mobile_number), gender, school_details, past_course,
                       current_course, int(year), int(is_deleted))
                db_cursor.execute(sql, val)
                db_connection.commit()

        print("Data from CSV file inserted into the database successfully!")
    except Exception as e:
        print("Error:", e)



#for teachers data
def add_teachers_from_csv(file_path):
    try:
        with open(file_path, 'r') as csvfile:
            csv_reader = csv.reader(csvfile)
            next(csv_reader)  # Skip the header row
            for row in csv_reader:
                name, address, mobile_number, gender, course_can_teach1, course_can_teach2, past_course, is_deleted = row

                # Insert the data into the database
                sql = "INSERT INTO teachers (name, address, mobile_number, gender, course_can_teach1, course_can_teach2, past_course, is_deleted) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
                val = (name, address, mobile_number, gender, course_can_teach1, course_can_teach2, past_course,
                       int(is_deleted))
                db_cursor.execute(sql, val)
                db_connection.commit()

        print("Data from teachers CSV file inserted into the database successfully!")
    except Exception as e:
        print("Error:", e)





