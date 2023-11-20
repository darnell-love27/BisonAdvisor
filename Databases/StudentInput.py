import json
import os

class Student: #Student Creator
    def __init__(self, name = " ", classification = " ", major = " ", studentID = 0, prev_courses=[]):
        #Initialized for student characteristics
        self.name = name
        self.studentID = studentID
        self.major = major
        self.classification = classification
        self.prev_courses = prev_courses

    @classmethod
    def from_dict(source):
        #Class method that creates a Student object from a dictionary
        return Student(
            source.get('name', ''),
            source.get('classification', ''),
            source.get('major', ''),
            source.get('studentID', 0),
            source.get('Previous Courses', [])
        )

    def to_dict(self):
        # Method to convert a Student object into a dictionary 
        return {
            'name': self.name,
            'studentID': self.studentID,
            'major': self.major,
            'classification': self.classification,
            'Previous Courses': self.prev_courses

        }

    def add_values_to_keys(self):
        # Method to take user input
        # Set Student object attributes
        self.name = input("Enter student name: ")
        self.studentID = input("Enter student ID: ")
        self.major = input("Enter student major: ")
        self.classification = input("Enter student classification: ")
        course_input = input("Enter courses taken separated by commas: ")
        self.prev_courses = course_input.split(',')

    def __repr__(self):
        # String representation of Student Object
        return f"Student(\
                name={self.name}, \
                studentID={self.studentID}, \
                major={self.major}, \
                classification={self.classification}, \
                Previous Courses={self.prev_courses}\
            )"

# Function that reads existing JSON data from a file
def read_existing_data(file_name):
    existing_data = []
    #Checks if file exists and non-empty
    if os.path.exists("StudentDatabase.json") and os.path.getsize("StudentDatabase.json") > 0:
        try:
            # Load existing JSON data from the file
            with open("StudentDatabase.json", 'r') as file:
                existing_data = json.load(file)
        except json.JSONDecodeError as e:
            # Handles JSON decoding error if the file doesn't contain valid JSON data
            print(f"Error reading JSON data: {e}")
            return existing_data
    return existing_data           


# Adds new student data to the existing JSON file
def append_student_data(file_name):
    while True:
        # Create student
        student = Student()
        # Assign values
        student.add_values_to_keys()
        # Convert to dictionary
        student_dict = student.to_dict()

        # Append new student data to existing data
        existing_data = read_existing_data(file_name)
        existing_data.append(student_dict)

        # Write updated data to the JSON file
        with open(file_name, 'w') as file:
            json.dump(existing_data, file, indent=4)

        choice = input("Do you want to add another student? (yes/no): ")
        if choice.lower() != 'yes':
            break

if __name__ == "__main__":
    file_name = "StudentDatabase.json"
    append_student_data(file_name)
    print(f"Student data has been appended to '{file_name}' as a JSON file.")
