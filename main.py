from functionalities import *
from validation import *

courses = ["Zoology", "Maths", "Biology", "Physics", "Chemistry"]
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
    print("11. Export student data")
    print("12. Import student data")
    print("13. Back to main menu")

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
    print("9. Export teacher data")
    print("10. Import teacher data")
    print("11. Back to main menu")

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
            print("Exiting!!!   ")
            # Exit
            break
        else:
            print("Invalid choice. Please enter a valid option.")

# Function for student menu
def student_menu():
    while True:
        display_student_menu()
        student_choice = input("Enter your choice: ")

        if student_choice == "1":
            add_new_student(courses)
        elif student_choice == "2":
            student_id = input("Enter student ID: ")
            view_student_details(student_id)
        elif student_choice == "3":
            update_student_information(db_cursor, db_connection)
        elif student_choice == "4":
            student_id = input("Enter student ID: ")
            delete_student_record(student_id)
        elif student_choice == "5":
            list_students_by_criteria()
        elif student_choice == "6":
            student_id = input("Enter student ID: ")
            view_student_current_course(student_id)
        elif student_choice == "7":
            update_student_current_course()
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
            export_table_to_csv("students", "/home/nineleaps/Downloads/student - Sheet1.csv")
        elif student_choice == "12":
            add_data_from_csv()
        elif student_choice == "13":
            break
        else:
            print("Invalid choice. Please enter a valid option.")


# Function for teacher menu
def teacher_menu():
    while True:
        display_teacher_menu()
        teacher_choice = input("Enter your choice: ")

        if teacher_choice == "1":
            add_new_teacher()
        elif teacher_choice == "2":
            teacher_id = input("Enter teacher's ID: ")
            view_teacher_details(teacher_id)  # Pass the teacher_id
        elif teacher_choice == "3":
            update_teacher_information()
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
            export_table_to_csv("teachers", "/home/nineleaps/Downloads/teachers - Sheet1.csv")
        elif teacher_choice == "10":
            file_path = input("Enter the path to the teachers CSV file: ")
            add_teachers_from_csv(file_path)
        elif teacher_choice == "11":
            break
        else:
            print("Invalid choice. Please enter a valid option.")

if __name__ == "__main__":
    main_menu()
