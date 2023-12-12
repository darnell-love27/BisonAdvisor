import json
import os
from pymongo import MongoClient
from pymongo_get_database import get_database

class Course: #Course Creator
    def __init__(self, name = " ", CRN = " ", department = " ", professors = [], prereq=[]):
        #Initialized for student characteristics
        self.name = name
        self.CRN = CRN
        self.department = department
        self.professors = professors
        self.prereq = prereq

    @classmethod
    def from_dict(source):
        #Class method that creates a Course object from a dictionary
        return Student(
            source.get('name', ''),
            source.get('CRN', ''),
            source.get('department', ''),
            source.get('professors', []),
            source.get('Previous Courses', [])
        )

    def to_dict(self):
        # Method to convert a Course object into a dictionary 
        return {
            'name': self.name,
            'Course Reference Number': self.CRN,
            'Department': self.department,
            'Professors': self.professors,
            'Prerequsite Courses': self.prereq

        }

    def add_values_to_keys(self):
        # Method to take user input
        # Set Course object attributes
        self.name = input("Enter course name: ")
        self.studentID = input("Enter course reference number: ")
        self.major = input("Enter department: ")
        self.professors = input("Enter professors that teach the course: ")
        course_input = input("Enter prerequsite courses: ")
        self.prereq = course_input.split(',')

    def __repr__(self):
        # String representation of Course Object
        return f"Course(\
                name={self.name}, \
                CRN={self.studentID}, \
                department={self.major}, \
                professors={self.classification}, \
                Prerequsites={self.prev_courses}\
            )"

# Function that reads existing JSON data from a file
def read_existing_data(file_name):
    existing_data = []
    #Checks if file exists and non-empty
    if os.path.exists("CourseDatabase.json") and os.path.getsize("CourseDatabase.json") > 0:
        try:
            # Load existing JSON data from the file
            with open("CourseDatabase.json", 'r') as file:
                existing_data = json.load(file)
        except json.JSONDecodeError as e:
            # Handles JSON decoding error if the file doesn't contain valid JSON data
            print(f"Error reading JSON data: {e}")
            return existing_data
    return existing_data           


# Adds new student data to the existing JSON file
def append_course_data(file_name):
    while True:
        # Create student
        course = Course()
        # Assign values
        course.add_values_to_keys()
        # Convert to dictionary
        course_dict = course.to_dict()

        # Append new student data to existing data
        existing_data = read_existing_data(file_name)
        existing_data.append(course_dict)

        # Write updated data to the JSON file
        with open(file_name, 'w') as file:
            json.dump(existing_data, file, indent=4)

        choice = input("Do you want to add another course? (yes/no): ")
        if choice.lower() != 'yes':
            break

def pushToMongoDB():
    file_name = "CourseDatabase.json"

    with open(file_name, 'r') as file:
        existing_data = json.load(file)

    dbname = get_database()
    collection_name = dbname["CourseData"]
    collection_name.insert_many(existing_data)

if __name__ == "__main__":
    file_name = "CourseDatabase.json"
    append_course_data(file_name)
    print(f"Course data has been appended to '{file_name}' as a JSON file.")
    pushToMongoDB()
