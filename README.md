# Student Management System (SMS)

SMS is a Python-based application for managing students and teachers in an educational institution. It provides functionalities for adding, viewing, updating, and deleting student and teacher records, along with various search and listing options.

## Features

- **Student Operations:**
  - Add new student
  - View student details
  - Update student information
  - Delete student record (Soft delete)
  - List all students by criteria
  - View student's current course
  - Update student's current course (Only for 1st year students)
  - View student's past courses
  - Search student by name
  - Search student by course

- **Teacher Operations:**
  - Add new teacher
  - View teacher details
  - Update teacher information (Name can't be updated)
  - Delete teacher record (Check if worked more than 1 Month) (Soft delete)
  - List all teachers (Separated by gender & course they teach)
  - View teacher's past courses (One teacher should teach at least 2 distinct courses)
  - Search teacher by name
  - Search teacher by course

## Dependencies

The project relies on the following dependencies:
- `mysql-connector-python`: For connecting to the MySQL database.
- `Python 3.x`: The programming language used to build the application.

## Installation

1. Clone the repository to your local machine:

git clone https://github.com/your-username/sms.git


2. Install the required dependencies:

pip install mysql-connector-python


3. Set up your MySQL database. You can create a new database called `sms3b` or use an existing one.

4. Update the `config.py` file with your MySQL database credentials




### Run the main.py file to start the application:
python main.py


#### Usage 
Upon running main.py, you will be presented with a menu where you can choose between student and teacher operations.
Follow the prompts to perform various actions such as adding new records, updating information, searching, and more.

