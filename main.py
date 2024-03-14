from functionalities import *
from validation import *

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

# Function to main menu
def main_menu():
    while True:
        display_menu()
        choice = input("Enter your choice: ")

        if choice == "1":
            student_menu()
        elif choice == "2":
            teacher_menu()
        elif choice == "3":
            # Exit
            break
        else:
            print("Invalid choice. Please enter a valid option.")

# Function for student menu
# Function for student menu
# Function for student menu
def student_menu():
    while True:
        display_student_menu()
        student_choice = input("Enter your choice: ")

        if student_choice == "1":
            # Prompt user for student details
            name = input("Enter student name: ")
            age = input("Enter student age: ")
            parent_details = input("Enter parent details: ")
            address = input("Enter address: ")
            mobile_number = input("Enter mobile number: ")
            gender = input("Enter gender: ")
            school_details = input("Enter school details: ")
            current_course = input("Enter current course: ")
            year = input("Enter year: ")
            add_new_student(name, age, parent_details, address, mobile_number, gender, school_details, current_course, year, courses)
        elif student_choice == "2":
            student_id = input("Enter student ID: ")
            view_student_details(student_id)
        elif student_choice == "3":
            student_id = input("Enter student ID: ")
            new_age = input("Enter new age: ")
            new_parent_details = input("Enter new parent details: ")
            new_address = input("Enter new address: ")
            new_mobile_number = input("Enter new mobile number: ")
            new_school_details = input("Enter new school details: ")
            new_course = input("Enter new course: ")
            year = input("Enter year: ")
            update_student_information(student_id, new_age, new_parent_details, new_address, new_mobile_number, new_school_details, new_course, year)
        elif student_choice == "4":
            student_id = input("Enter student ID: ")
            delete_student_record(student_id)
        elif student_choice == "5":
            list_students_by_criteria()
        elif student_choice == "6":
            student_id = input("Enter student ID: ")
            view_student_current_course(student_id)
        elif student_choice == "7":
            student_id = input("Enter student ID: ")
            new_course = input("Enter new course: ")
            update_student_current_course(student_id, new_course)
        elif student_choice == "8":
            student_id = input("Enter student ID: ")
            view_student_past_courses(student_id)
        elif student_choice == "9":
            name = input("Enter student name: ")
            search_student_by_name(name)
        elif student_choice == "10":
            current_course = input("Enter course: ")
            search_students_by_course(current_course)
        elif student_choice == "11":
            break
        else:
            print("Invalid choice. Please enter a valid option.")


# Function for teacher menu
def teacher_menu():
    while True:
        display_teacher_menu()
        teacher_choice = input("Enter your choice: ")

        if teacher_choice == "1":
            name = input("Enter teacher's name: ")
            address = input("Enter teacher's address: ")
            mobile_number = input("Enter teacher's mobile number: ")
            gender = input("Enter teacher's gender: ")
            course_can_teach1 = input("Enter the first course the teacher can teach: ")
            course_can_teach2 = input("Enter the second course the teacher can teach: ")
            add_new_teacher(name, address, mobile_number, gender, course_can_teach1, course_can_teach2)
        elif teacher_choice == "2":
            teacher_id = input("Enter teacher's ID: ")
            view_teacher_details(teacher_id)  # Pass the teacher_id
        elif teacher_choice == "3":
            teacher_id = input("Enter teacher's ID: ")
            new_address = input("Enter new address: ")
            new_mobile_number = input("Enter new mobile number: ")
            new_course = input("Enter new course: ")
            update_teacher_information(teacher_id, new_address, new_mobile_number, new_course)
        elif teacher_choice == "4":
            teacher_id = input("Enter teacher's ID: ")
            delete_teacher_record(teacher_id)  # Pass the teacher_id
        elif teacher_choice == "5":
            list_teachers_by_criteria()
        elif teacher_choice == "6":
            teacher_id = input("Enter teacher's ID: ")
            view_teacher_past_courses(teacher_id)  # Pass the teacher_id
        elif teacher_choice == "7":
            teacher_name = input("Enter teacher's name: ")
            search_teacher_by_name(teacher_name)  # Pass the teacher's name
        elif teacher_choice == "8":
            course_can_teach = input("Enter course the teacher can teach: ")
            search_teacher_by_course(course_can_teach)  # Pass the course
        elif teacher_choice == "9":
            break
        else:
            print("Invalid choice. Please enter a valid option.")

if __name__ == "__main__":
    main_menu()
