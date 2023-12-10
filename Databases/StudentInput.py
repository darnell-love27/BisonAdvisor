import json
import os
from pymongo import MongoClient
from pymongo_get_database import get_database


class Student:
    def __init__(self, name="", classification="", major="", studentID=0, courses=None):
        # Initialize student characteristics
        self.name = name
        self.studentID = studentID
        self.major = major
        self.classification = classification
        self.courses = courses if courses else []

    @classmethod
    def from_dict(cls, source):
        # Class method that creates a Student object from a dictionary
        return cls(
            source.get('name', ''),
            source.get('classification', ''),
            source.get('major', ''),
            source.get('studentID', 0),
            source.get('courses', [])
        )

    def to_dict(self):
        # Method to convert a Student object into a dictionary
        return {
            'name': self.name,
            'studentID': self.studentID,
            'major': self.major,
            'classification': self.classification,
            'courses': self.courses
        }

    def add_values_to_keys(self):
    # Method to take user input and set Student object attributes
        self.name = input("Enter student name: ")
        self.studentID = input("Enter student ID: ")
        self.major = input("Enter student major: ")
        self.classification = input("Enter student classification: ")
        courses_input = input("Enter courses taken separated by commas (course_code,course_name): ")
        self.courses = courses_input.split(",")


    def __repr__(self):
        # String representation of Student Object
        return f"Student(\
            name={self.name}, \
            studentID={self.studentID}, \
            major={self.major}, \
            classification={self.classification}, \
            courses={self.courses}\
        )"

# Function that reads existing JSON data from a file
def read_existing_data(file_name):
    existing_data = []
    # Checks if file exists and non-empty
    if os.path.exists(file_name) and os.path.getsize(file_name) > 0:
        try:
            # Load existing JSON data from the file
            with open(file_name, 'r') as file:
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

def pushToMongoDB():
    file_name = "StudentDatabase.json"

    with open(file_name, 'r') as file:
        existing_data = json.load(file)

    dbname = get_database()
    collection_name = dbname["StudentData"]
    collection_name.insert_many(existing_data)

if __name__ == "__main__":
    file_name = "StudentDatabase.json"
    append_student_data(file_name)
    print(f"Student data has been appended to '{file_name}' as a JSON file.")
    pushToMongoDB()
