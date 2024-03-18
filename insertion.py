import mysql.connector
import random

# Establishing connection to MySQL database
db_connection = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="Veena@12345",
    database="sms3b"
)
db_cursor = db_connection.cursor()

# Creating table for students
db_cursor.execute("CREATE TABLE IF NOT EXISTS students ("
                  "id INT AUTO_INCREMENT PRIMARY KEY, "
                  "name VARCHAR(255), "
                  "age INT, "
                  "parent_details VARCHAR(255), "
                  "address VARCHAR(255), "
                  "mobile_number VARCHAR(20), "
                  "gender ENUM('Male', 'Female', 'Other'), "
                  "school_details VARCHAR(255), "
                  "past_course VARCHAR(255), "
                  "current_course VARCHAR(255), "
                  "year INT)"
                  )

# Check if current_course column exists, if not, add it
db_cursor.execute("SHOW COLUMNS FROM students LIKE 'current_course'")
if not db_cursor.fetchone():
    db_cursor.execute("ALTER TABLE students ADD COLUMN current_course VARCHAR(255)")

# Adding the new "year" column to the table if it doesn't already exist
db_cursor.execute("SHOW COLUMNS FROM students LIKE 'year'")
if not db_cursor.fetchone():
    db_cursor.execute("ALTER TABLE students ADD COLUMN year INT")


# Creating table for teachers
db_cursor.execute("CREATE TABLE IF NOT EXISTS teachers ("
                  "id INT AUTO_INCREMENT PRIMARY KEY, "
                  "name VARCHAR(255), "
                  "address VARCHAR(255), "
                  "mobile_number VARCHAR(20), "
                  "gender ENUM('Male', 'Female', 'Other'), "
                  "course_can_teach1 VARCHAR(255),"
                  "course_can_teach2 VARCHAR(255),"
                  "past_course VARCHAR(255))"
                  )

# List of real-life student names
student_names = [
    "Rohan", "Aarav", "Priya", "Avni", "Aditya", "Arjun", "Ananya", "Kavya", "Ishaan", "Riya",
    "Aryan", "Ishita", "Akshay", "Alisha", "Ritvik", "Anika", "Sarthak", "Neha", "Vivaan", "Jia",
    "Amit", "Sandeep", "Rajesh", "Vikas", "Gaurav", "Anita", "Preeti", "Neha", "Ritu", "Shweta",
    "Deepak", "Vishal", "Rahul", "Nitin", "Sanjay", "Pooja", "Sakshi", "Simran", "Aarti", "Kiran",
    "Prakash", "Suresh", "Ashok", "Geeta", "Suman", "Rashmi", "Manish", "Vinod", "Sangeeta", "Vijay",
    "Neeraj", "Nidhi", "Rajni", "Mukesh", "Seema", "Sonu", "Kavita", "Alok", "Rani", "Avinash",
    "Suman", "Rajiv", "Sushil", "Rohit", "Lalita", "Vijay", "Varsha", "Anil", "Nisha", "Sumit",
    "Ritu", "Ramesh", "Kamini", "Arun", "Madhu", "Sunil", "Raj", "Poonam", "Satish", "Savita",
    "Praveen", "Kiran", "Rakesh", "Shilpa", "Amar", "Indu", "Alok", "Usha", "Avinash", "Swati",
    "Sanjeev", "Anjali", "Vikram", "Ruchi"
]

# List of real-life parent names
parent_names = [
    "Amit", "Sandeep", "Rajesh", "Vikas", "Gaurav", "Anita", "Preeti", "Neha", "Ritu", "Shweta",
    "Deepak", "Vishal", "Rahul", "Nitin", "Sanjay", "Pooja", "Sakshi", "Simran", "Aarti", "Kiran",
    "Prakash", "Suresh", "Ashok", "Geeta", "Suman", "Rashmi", "Manish", "Vinod", "Sangeeta", "Vijay",
    "Neeraj", "Nidhi", "Rajni", "Mukesh", "Seema", "Sonu", "Kavita", "Alok", "Rani", "Avinash",
    "Suman", "Rajiv", "Sushil", "Rohit", "Lalita", "Vijay", "Varsha", "Anil", "Nisha", "Sumit",
    "Ritu", "Ramesh", "Kamini", "Arun", "Madhu", "Sunil", "Raj", "Poonam", "Satish", "Savita",
    "Praveen", "Kiran", "Rakesh", "Shilpa", "Amar", "Indu", "Alok", "Usha", "Avinash", "Swati",
    "Sanjeev", "Anjali", "Vikram", "Ruchi"
]

# List of real addresses from Delhi, India
delhi_addresses = [
    "Connaught Place, New Delhi",
    "Chandni Chowk, Old Delhi",
    "Karol Bagh, New Delhi",
    "Lajpat Nagar, New Delhi",
    "Saket, New Delhi",
    "Hauz Khas, New Delhi",
    "Dwarka, New Delhi",
    "Nehru Place, New Delhi",
    "Rohini, New Delhi",
    "Pitampura, New Delhi",
    "Greater Kailash, New Delhi",
    "Green Park, New Delhi",
    "Vasant Kunj, New Delhi",
    "Mayur Vihar, New Delhi",
    "Rohini Sector 9, New Delhi",
    "Janakpuri, New Delhi",
    "Tilak Nagar, New Delhi",
    "Rajouri Garden, New Delhi",
    "Patel Nagar, New Delhi",
    "Malviya Nagar, New Delhi",
    "Shahdara, New Delhi",
    "Uttam Nagar, New Delhi",
    "Punjabi Bagh, New Delhi",
    "Dwarka Sector 12, New Delhi",
    "Sarita Vihar, New Delhi",
    "Kalkaji, New Delhi",
    "Paschim Vihar, New Delhi",
    "Vasundhara Enclave, New Delhi",
    "Saket, New Delhi",
    "Rohini Sector 15, New Delhi"
]

# List of courses for teachers
courses = ["Science", "Maths", "Biology", "Physics", "Chemistry"]

# Function to generate random mobile number
def generate_mobile_number():
    return random.choice(['6', '7', '8', '9']) + ''.join(random.choices('0123456789', k=9))

# Function to add 50 random students
def add_students():
    for _ in range(100):
        name = random.choice(student_names)
        age = random.randint(17, 23)
        parent_details = random.choice(parent_names)
        address = random.choice(delhi_addresses)
        mobile_number = generate_mobile_number()
        gender = "Male" if name[-1].lower() != 'a' else "Female"  # Assuming gender based on name
        school_details = "St Stephen's College"
        current_course = random.choice(courses) # Assigning the same course as the current course
        year = random.randint(1, 4)  # Generating a random year

        sql = "INSERT INTO students (name, age, parent_details, address, mobile_number, gender, school_details, current_course, year) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        val = (name, age, parent_details, address, mobile_number, gender, school_details, current_course, year)
        db_cursor.execute(sql, val)

    db_connection.commit()
    print("Students added successfully!")

# Function to add 25 random teachers
def add_teachers():
    for _ in range(10):
        name = random.choice(parent_names)  # Using parent names for teachers
        address = random.choice(delhi_addresses)
        mobile_number = generate_mobile_number()
        gender = "Male" if name[-1].lower() != 'a' else "Female"  # Assuming gender based on name
        course1 = random.choice(courses)  # Extracting a single course
        course2 = random.choice(courses)
        past_course = ""

        sql = "INSERT INTO teachers (name, address, mobile_number, gender, course_can_teach1, course_can_teach2, past_course) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        val = (name, address, mobile_number, gender, course1, course2, past_course)
        db_cursor.execute(sql, val)

    db_connection.commit()
    print("Teachers added successfully!")

# Adding 25 random students
add_students()

# Adding 25 random teachers
add_teachers()

# Closing connection
db_connection.close()
