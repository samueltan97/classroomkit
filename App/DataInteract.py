import time
from datetime import date
import datetime
from FileJSON import FileJSON
import copy

class CKDatabase:
    """
    A class for interacting with the Classroom Kit database.
    """
    def __init__(self, path):
        """
        Initializing the database requires the path to a JSON file where the data will be stored.
        The file will be created if it does not already exist.
        :param path:
        """
        # Initialize JSON file
        self.file = FileJSON(path)
        if "courses" not in self.file.data.keys():
            self.file.write({"courses":[]})
    def currentData(self):
        """
        Returns the data of the JSON file as a dictionary.
        :return:
        """
        return self.file.data
    def write(self,new):
        """
        Overwrites database with new data passed.
        :param new:
        :return:
        """
        self.file.write(new)
    def getCourseIndex(self, courseName):
        """
        Courses in the database are stored in an array, so if you want to access them by name, use this function.
        Returns the index of the course in the list of courses.
        :param courseName:
        :return:
        """
        data = self.currentData()
        for i,course in enumerate(data["courses"]):
            if course["courseName"] == courseName:
                return i
        return -1
    def newCourse(self, courseName):
        """
        Adds a new course to the database.
        :param courseName:
        :param PiazzaID:
        :return:
        """
        # Default course value
        course = {
            "courseName": courseName,
            "PiazzaClass": None,
            "PiazzaUsername": None,
            "PiazzaPassword": None,
            "isArchived": False,
            "students": []
        }
        new = self.currentData()
        # Append course to list
        if self.getCourseIndex(courseName) == -1:
            new["courses"].append(course)
            self.write(new)
    def removeCourse(self, courseName):
        """
        Removes a course from the database.
        :param courseName:
        :return:
        """
        # Get index of course
        index = self.getCourseIndex(courseName)
        data = self.currentData()
        # Delete course by index
        del data["courses"][index]
        self.write(data)
    def archiveCourse(self, courseName):
        """
        Marks course as archived.
        :param courseName:
        :return:
        """
        # Get index of course
        index = self.getCourseIndex(courseName)
        data = self.currentData()
        # Mark as archived
        data["courses"][index]["isArchived"] = True
        self.write(data)
    def unarchiveCourse(self, courseName):
        """
        Marks course as not archived.
        :param courseName:
        :return:
        """
        # Get index of course
        index = self.getCourseIndex(courseName)
        data = self.currentData()
        # Mark as not archived
        data["courses"][index]["isArchived"] = False
        self.write(data)
    def isArchived(self, courseName):
        """
        Checks whether a course is archived.
        :param courseName:
        :return:
        """
        # Get index of course
        index = self.getCourseIndex(courseName)
        data = self.currentData()
        # Return isArchived boolean
        if data["courses"][index]["isArchived"]:
            return True
        else:
            return False
    def assignCoursePiazzaID(self, courseName, PiazzaID):
        """
        Assigns a course a unique Piazza ID.
        :param courseName:
        :param PiazzaID:
        :return:
        """
        data = self.currentData()
        # Get index of course
        index = self.getCourseIndex(courseName)
        # Set Piazza ID
        data["courses"][index]["PiazzaClass"] = PiazzaID
        self.write(data)
    def assignCoursePiazzaUserInfo(self, courseName, username, password):
        """
        Assigns user info (username and password) to a course so that the program can access Piazza class page.
        :param courseName:
        :param username:
        :param password:
        :return:
        """
        data = self.currentData()
        # Get index of course
        index = self.getCourseIndex(courseName)
        # Store user credentials
        data["courses"][index]["PiazzaUsername"] = username
        data["courses"][index]["PiazzaPassword"] = password
        self.write(data)
    def newStudent(self, courseName, studentName, OneCard):
        """
        Adds a student to a course in the database.
        Requires the name of the course, the name of the student, and the OneCard ID string.
        :param courseName:
        :param studentName:
        :param OneCard:
        :return:
        """
        # Default student value
        student = {
            "name": studentName,
            "OneCard": OneCard,
            "PiazzaID": "",
            "PiazzaReportCard": 0,
            "attendance": {
                "classPeriods": {}
            }
        }
        oldData = self.currentData()
        # Check whether student already in course
        studentAlreadyInCourse = False
        for oldstudent in oldData["courses"][self.getCourseIndex(courseName)]["students"]:
            if oldstudent["name"] == studentName:
                # print("Student already in course")
                studentAlreadyInCourse = True
        # Add class periods retroactively
        if not studentAlreadyInCourse:
            if len(oldData["courses"][self.getCourseIndex(courseName)]["students"]) > 0:
                for date in oldData["courses"][self.getCourseIndex(courseName)]["students"][0]["attendance"]["classPeriods"].keys():
                    student["attendance"]["classPeriods"][date] = {"attended": False, "late": False}
            oldData["courses"][self.getCourseIndex(courseName)]["students"].append(student)
            new = oldData
            self.write(new)
    def removeStudent(self, courseName, studentName):
        """
        Removes a student from a course by name.
        :param courseName:
        :param studentName:
        :return:
        """
        data = self.currentData()
        # Locate student
        students = data["courses"][self.getCourseIndex(courseName)]["students"]
        for i,student in enumerate(students):
            if student["name"] == studentName:
                # Delete student
                del students[i]
                break
        self.write(data)
    def studentByOneCard(self, courseName, OneCard):
        """
        Get student using their OneCard ID
        :param courseName:
        :param OneCard:
        :return:
        """
        data = self.currentData()
        students = data["courses"][self.getCourseIndex(courseName)]["students"]
        # Loop through until OneCard found
        for student in students:
            if student.OneCard == OneCard:
                # Return parent
                return student
        return None            
    def assignPiazzaID(self, courseName, studentName, PiazzaID):
        """
        Connects a student to a Piazza account using their Piazza UID.
        :param courseName:
        :param studentName:
        :param PiazzaID:
        :return:
        """
        data = self.currentData()
        students = data["courses"][self.getCourseIndex(courseName)]["students"]
        # Locate student
        for student in students:
            if student["name"] == studentName:
                # Assign ID
                student["PiazzaID"] = PiazzaID
                break
        self.write(data)
    def savePiazzaReportCard(self, courseName, PiazzaID, reportCard):
        """
        Caches a student's Piazza Report Card.
        :param courseName:
        :param PiazzaID:
        :param reportCard:
        :return:
        """
        data = self.currentData()
        students = data["courses"][self.getCourseIndex(courseName)]["students"]
        # Locate student
        for student in students:
            if student["PiazzaID"] == PiazzaID:
                # Save report card
                student["PiazzaReportCard"] = reportCard
                break
        self.write(data)
    def newClassPeriod(self, courseName):
        """
        Adds a new class period to a course.
        Returns key of class period in the database.
        Key of class period is a stringified floating point value representing the number of seconds from UNIX epoch.
        :param courseName:
        :return:
        """
        # Time
        nowString = str(date.today())
        # Default Attendance Value
        classPeriod = {"attended": False, "late": False}
        oldData = self.currentData()
        courseData = None
        # Locate course
        courseIndex = 0
        for i,course in enumerate(oldData["courses"]):
            if course["courseName"] == courseName:
                courseData = course
                courseIndex = i
        # Add class period to all students in course
        for student in courseData["students"]:
            student["attendance"]["classPeriods"][nowString] = classPeriod

        newData = oldData
        newData["courses"][courseIndex] = courseData
        # print(courseData)
        self.write(newData)
        return nowString
    def removeClassPeriod(self, courseName, classPeriod):
        """
        Removes class period from a course using the name of the course and the key of the class period.
        :param courseName:
        :param classPeriod:
        :return:
        """
        data = self.currentData()
        course = data["courses"][self.getCourseIndex(courseName)]
        students = course["students"]
        # Locate class period in each student
        for student in students:
            periods = student["attendance"]["classPeriods"]
            # Delete class period
            del periods[classPeriod]
        self.write(data)
    def signIn(self, courseName, OneCard, classPeriod):
        """
        Marks a student as present for a class period.
        :param courseName:
        :param OneCard:
        :param classPeriod:
        :return:
        """
        # Locate student
        data = copy.deepcopy(self.currentData())
        students = data["courses"][self.getCourseIndex(courseName)]["students"]
        changeTo = {}
        i = 0
        for student in students:
            if student["OneCard"] == OneCard:
                # Mark as present
                changeTo = copy.deepcopy(student)
                changeTo["attendance"]["classPeriods"][classPeriod]["attended"] = True
                break
            else:
                i += 1
        data["courses"][self.getCourseIndex(courseName)]["students"][i] = changeTo
        self.write(data)

def Test():
    """
    >>> db = CKDatabase("test.json")
    >>> db.newCourse("CS107")
    >>> db.newCourse("CS105")
    >>> db.newStudent("CS107", "Isaac", "1")
    >>> db.newStudent("CS107", "Joseph", "2")
    >>> db.newStudent("CS107", "Samuel", "3")
    >>> period = db.newClassPeriod("CS107")
    >>> db.signIn("CS107","1", period)
    >>> db.removeStudent("CS107", "Joseph")
    >>> db.archiveCourse("CS105")
    >>> data = db.currentData()
    >>> for student in data["courses"][0]["students"]:
    ...     dayData = student["attendance"]["classPeriods"][period].copy()
    ...     del student["attendance"]["classPeriods"][period]
    ...     student["attendance"]["classPeriods"]["2019-12-13"] = dayData
    >>> print(data)
    {'courses': [{'courseName': 'CS107', 'PiazzaClass': None, 'PiazzaUsername': None, 'PiazzaPassword': None, 'isArchived': False, 'students': [{'name': 'Isaac', 'OneCard': '1', 'PiazzaID': '', 'PiazzaReportCard': 0, 'attendance': {'classPeriods': {'2019-12-13': {'attended': True, 'late': False}}}}, {'name': 'Samuel', 'OneCard': '3', 'PiazzaID': '', 'PiazzaReportCard': 0, 'attendance': {'classPeriods': {'2019-12-13': {'attended': False, 'late': False}}}}]}, {'courseName': 'CS105', 'PiazzaClass': None, 'PiazzaUsername': None, 'PiazzaPassword': None, 'isArchived': True, 'students': []}]}
    """
    pass

if __name__ == "__main__":
    import doctest
    doctest.testmod()