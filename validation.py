def validate_student_name(name):
    if not isinstance(name, str):
        raise ValueError("Student name must be a string.")
    if not name.strip():  # Check if the name is empty or contains only whitespace
        raise ValueError("Student name cannot be empty.")
    if not name.replace(" ", "").isalpha():  # Check if the name contains only alphabets and spaces
        raise ValueError("Student name can only contain alphabets.")
    return name


def validate_age(age):
    age = int(age)
    if age < 17 or age > 93:
        raise ValueError("Age must be between 17 and 93.")
    return age

def validate_mobile_number(mobile_number):
    try:
        mobile_number = str(mobile_number)
        if len(mobile_number) != 10:
            raise ValueError("Mobile number must be 10 digits long!")
        if mobile_number[0] not in ['6', '7', '8', '9']:
            raise ValueError("Mobile number must start with digits 6, 7, 8, or 9!")
        return int(mobile_number)
    except ValueError:
        raise ValueError("Mobile number must be numeric and 10 digits long!")

def validate_gender(gender):
    gender = gender.lower()
    if gender not in ['male', 'female', 'other']:
        raise ValueError("Invalid gender! Gender must be 'Male', 'Female', or 'Other'.")
    return gender

def validate_student_id(student_id):
    try:
        student_id = int(student_id)
        if student_id <= 0:
            raise ValueError("Student ID must be a positive integer.")
        return student_id
    except ValueError:
        raise ValueError("Student ID must be a positive integer.")

def validate_teacher_id(teacher_id):
    try:
        teacher_id = int(teacher_id)
        if teacher_id <= 0:
            raise ValueError("Teacher ID must be a positive integer.")
        return teacher_id
    except ValueError:
        raise ValueError("Teacher ID must be a positive integer.")


def validate_course(course, allowed_courses):
    if course not in allowed_courses:
        raise ValueError(f"Invalid course! Allowed courses are: {', '.join(allowed_courses)}")
    return course
