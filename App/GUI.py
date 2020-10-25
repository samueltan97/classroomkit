import tkinter as tk
import matplotlib.pyplot as mpl
from RFID import RFID
import time
from datetime import date
from piazza_class_participation.main import ScrapeApp as scraper
from tkinter import font as tkfont
from tkinter import *
from DataInteract import CKDatabase


class GUI(tk.Tk):
    """
    The runner code that makes the main window and builds all the frames
    """
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.database = CKDatabase("data.json")
        # Sets up the list of classes to display whenever we need to list all of the classes
        self.currentClasses = []
        self.archivedClasses = []
        # if its archived, it goes in the archived list, otherwise it goes in the currentclasses list.
        for course in self.database.currentData()["courses"]:
            if course["isArchived"]:
                self.archivedClasses.append(course["courseName"])
            else:
                self.currentClasses.append(course["courseName"])

        # Here we use the container to stack multiple frames on top of one another on the same point so we can switch
        # which is on the top layer.
        # This code adapted from https://stackoverflow.com/questions/34301300/tkinter-understanding-how-to-switch-frames
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        # We also keep a way to access the container in order to manipulate later.
        self.frameSet = container
        # Here we get a list of frames and frametypes, also for later use
        self.frames = {}
        self.frameTypes = {}
        # We take all the frames and render them here, and store their instances and types in the lists.
        for F in (StartPage, AttendancePage, DisplayAttendancePage, EditCourses, ParticipationPage):
            # page name is used to take the name of the class and put it into a string so we can store it in the
            # dictionary
            pageName = F.__name__
            # here we generate the frame with a controller so we can refer to all the self variables in this class
            frame = F(parent=container, controller=self)
            # we put the relevant parts into the relevant lists
            self.frames[pageName] = frame
            self.frameTypes[pageName] = F

            # Puts all pages on the same row/column, on which the stacking order decides which is visible.
            frame.grid(row=0, column=0, sticky="nsew")
        # and we show the start page first.
        self.showFrame("StartPage")

    def showFrame(self, pageName):
        '''Show a frame for the given page name'''
        frame = self.frames[pageName]
        frame.tkraise()

    def listFrames(self):
        '''Returns a list of all the non-start-page frame names'''
        return ("AttendancePage", "DisplayAttendancePage", "EditCourses", "ParticipationPage")

    def getFrameSet(self):
        '''Returns the frameset, the container'''
        return self.frameSet

    def getCurrentClasses(self):
        '''Returns all of the current classes'''
        return self.currentClasses


class StartPage(tk.Frame):
    '''StartPage is the main menu of the application, provides options to access '''
    def __init__(self, parent, controller):
        # initializes itself, sets reference to controller
        tk.Frame.__init__(self, parent)
        self.controller = controller
        # Sets up fonts for title, subtitle, then the actual title
        titleFont = tkfont.Font(size=18, weight="bold")
        subtitleFont = tkfont.Font(size=12, slant="italic")
        title = Label(self, text="Student Assessment Kit", font=titleFont)
        title.pack()
        # Sets up the three headers. First is the classes header.which lets you add/remove classes (in which you provide a name
        # and a time, with errors if there's conflicts), and archive/unarchive classes (which removes it from the "calendar",
        # preventing it from being accessed or modified, or puts it back in).
        # Each header has its own frame, which is also set up here.

        draw.changePageButton(self, controller, "Attendence Options", "AttendancePage")

        draw.changePageButton(self, controller, "Participation Options", "ParticipationPage")

        draw.changePageButton(self, controller, "Edit Courses", "EditCourses")
        # also a subtitle
        subTitle = Label(self, text="By Joseph Gentile, Issac Wasserman, and Sam Tan", font=subtitleFont)
        subTitle.pack()

        # Adds an exit button to terminate the application
        draw.addButton(self, "Exit", exit, BOTTOM)


def destroyFrame(root):
    '''Destroy the root passed to it'''
    root.destroy()


def changePage(controller, pageName):
    '''Pass the controller and the name of the page to change visible page'''
    controller.showFrame(pageName)


class AttendancePage(tk.Frame):
    '''The attendance page, has options for signing people in, enrolling people, and displaying attendance'''
    # This is the page that handles the attendence options, turning on "sign-in mode" for a sepcific class
    # (allowing new scans to update attendance), edit courses to archive/unarchive/add/delete courses, and
    # display to either show as a graph or a chart.
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        # Makes buttons to change to the aforementioned pages
        draw.addLabel(self, "Attendance Options", TOP)
        draw.addButtonArguments(self, "Sign-in Mode", signInMode, controller)
        draw.addButtonArguments(self, "Enrollment Mode", enrollmentMode, controller)
        draw.changePageButton(self, controller, "Display", "DisplayAttendancePage")
        draw.changePageButton(self, controller, "Back", "StartPage", BOTTOM)


class DisplayAttendancePage(tk.Frame):
    '''This is the page that handles display options. It shows all classes, and clicking graph/grid displays
    the data accordingly. '''
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        # labels
        draw.addLabel(self, "How do you want to sort the data?")
        # Sets up two radiobuttons to switch between ordering by date, or by student.
        # uses sortStudent as a variable that changes depending on which radiobutton is pressed.
        sortStudent = IntVar()
        switchFrame = Frame(self)
        tk.Radiobutton(switchFrame, text="Sort By Student", variable=sortStudent, value=1).pack(side=LEFT)
        tk.Radiobutton(switchFrame, text="Sort By Date", variable=sortStudent, value=0).pack(side=RIGHT)
        switchFrame.pack()
        # Lists all the classes, and buttons to display attendance as graph and as grid.
        draw.addLabel(self, "Which Class?", TOP)
        for element in controller.currentClasses:
            setFrame = Frame(self)
            draw.addLabel(setFrame, element, LEFT)
            # sets up parameters to pass to the graph/grid
            argumentDict = {"course": element, "isStudent": sortStudent, "controller" : controller}
            draw.addButtonArguments(setFrame, "Graph", displayAttendanceGraph, argumentDict, RIGHT)
            draw.addButtonArguments(setFrame, "Grid", displayAttendanceGrid, argumentDict, RIGHT)
            setFrame.pack()
        #back button
        draw.changePageButton(self, controller, "Back", "AttendancePage", BOTTOM)




def displayAttendanceGrid(argumentDict):
    '''Takes the class section and displays an attendance grid'''
    # Gets the data from the database and sets up dummy lists for the names and dates
    data = argumentDict["controller"].database.currentData()
    sectionId = argumentDict["controller"].database.getCourseIndex(argumentDict["course"])
    names = []
    dates = []
    # Sets up the window upon which we put our grid

    root = Tk()
    # Sets up counting variables
    i = 1
    j = 1
    # Time to start getting together names; this loop takes all students in the class and puts their names in the
    # names list.
    # Also, to access the dates later, stores a student object.
    referenceStudent = None
    for student in data["courses"][sectionId]["students"]:
        names.append(student["name"])
        referenceStudent = student

    # Everything following is predicated on there being students present, that is to say, that there is a reference
    # student
    if referenceStudent:
        # Here it just loads the dates list with dates
        for date in referenceStudent["attendance"]["classPeriods"].keys():
            dates.append(date[5:])
        # Now, we load the names and dates on the top and left sides of the axes respectively.
        for date in dates:
            column = Label(root, text=date)
            column.grid(row=0, column=j)
            j += 1
        for name in names:
            row = Label(root, text=name)
            row.grid(row=i, column=0)
            i += 1
        # now we set the column, row to (1,1), then start filling the whole grid in
        i = 1
        j = 1
        # In student list
        for student in data["courses"][sectionId]["students"]:
            # in list of dates for each student
            for date in student["attendance"]["classPeriods"]:
                # If the student was late on that date, it's a yellow "late"

                if student["attendance"]["classPeriods"][date]["late"]:
                    b = Label(root, text="L", bg="yellow")
                # If the student was there, it's a green "Present"
                elif student["attendance"]["classPeriods"][date]["attended"]:
                    b = Label(root, text="P", bg="green")
                # If the student was not there, it's a red "absent"
                else:
                    b = Label(root, text="A ", bg="red")
                # puts the desired label onto the grid.
                b.grid(row=i, column=j)
                j += 1
            j = 1
            i += 1
        # Lastly, since it is likely the dates/students will go off the screen when a lot are present, we have two
        # functions to make scrollbars, both adapted from http://effbot.org/tkinterbook/scrollbar.htm

        # scrollbar = Scrollbar(root)
        # scrollbar.pack(side=BOTTOM, fill=X)

        # listbox = Listbox(root, xscrollcommand=scrollbar.set)
        # for i in range(1000):
        #    listbox.insert(END, str(i))
        # listbox.pack(side=BOTTOM, fill=BOTH)

        # scrollbar.config(command=listbox.xview)


def displayAttendanceGraph(argumentDict):
    '''Takes a dictionary containing the course and a boolean and displays a graph either by date, or by student.'''
    # Gets the data, section, sectionid, and data.
    database = argumentDict["controller"].database
    section = argumentDict["course"]
    sectionId = database.getCourseIndex(section)
    isStudent = argumentDict["isStudent"].get()
    data = database.currentData()
    # sets up lists for later, which are to be put into the graph later
    names = []
    dates = []
    dateDict = {}
    freq = []
    freqDates = []
    # Checks if isStudent is true, if we're sorting by student.
    if isStudent:
        # Fills names with all the students in a class
        for student in data["courses"][sectionId]["students"]:
            names.append(student["name"])
        # Goes through every student and every class they've attended. Counts up by 1 for every class they've attended.
        for student in data["courses"][sectionId]["students"]:
            attendanceFreq = 0
            for date in student["attendance"]["classPeriods"].keys():
                day = student["attendance"]["classPeriods"][date]
                if day["attended"]:
                    attendanceFreq += 1
            # every student's attendancefrequency is added to a list
            freq.append(attendanceFreq)
        # plots the names and frequencies.
        mpl.bar(names, freq)
        mpl.ylabel("Classes Attended")
        mpl.xlabel("Student")
        mpl.show()
    else:
        # Case that we're sorting by date
        # goes through all students
        for student in data["courses"][sectionId]["students"]:
            # goes through all the dates
            for date in student["attendance"]["classPeriods"].keys():
                # if a student attended a given date, that date is counted up by one
                if student["attendance"]["classPeriods"][date]["attended"]:
                    # adds that date to the date dictionary, date list if it's not in it, otherwise
                    # increments its frequency by one.
                    if date not in dateDict:
                        dateDict[date] = 1
                        dates.append(date)
                    else:
                        dateDict[date] += 1
                # if the student didn't attend, it still adds the date to the list, but doesn't increment anything.
                else:
                    if date not in dateDict:
                        dateDict[date] = 0
                        dates.append(date)
        # Goes through all the datefrequencies and puts them in a list
        for date in dateDict:
            freqDates.append(dateDict[date])
        # plots dates and date frequencies.
        mpl.bar(dates, freqDates)
        mpl.ylabel("Number of Students Present")
        mpl.xlabel("Date")
        mpl.show()


class EditCourses(tk.Frame):
    '''This is the page that handles editing options. Add a class, archive a class, unarchive a class, or delete
    # an archived class. There's also a student button; see student page.'''
    def __init__(self, parent, controller):
        # sets up the controller, name, title label
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.name = "EditCourses"
        draw.addLabel(self, "Editing Course Options")
        # lists all the classes, with options to archive or view students.
        draw.addLabel(self, "Current Class List:")
        for element in controller.currentClasses:
            setFrame = Frame(self)
            draw.addLabel(setFrame, element, RIGHT)
            argumentDict = {"CurrentFrame": "EditCourses", "controller": controller, "Course" : element}
            draw.addButtonArguments(setFrame, "Archive", archive, argumentDict)
            draw.addButtonArguments(setFrame, "Students", seeStudents, argumentDict)
            setFrame.pack()
        # Remove semester button, which lets you remove a semester. Brings you to the removeASemester function.
        # Archive semester button, which archives a semester. Brings you to the archiveSemester function.
        argumentDict = {"CurrentFrame": "EditCourses", "controller": controller}
        draw.addButtonArguments(self, "Add a Semester", addSemester, argumentDict)
        draw.addButtonArguments(self, "Archived Semesters", archivedSemester, argumentDict)
        # back button
        draw.changePageButton(self, controller, "Back", "StartPage", BOTTOM)


# Helper methods for EditCourses

def addSemester(argumentDict):
    '''Opens up a new window, which prompts the user for the name of the semester (to be entered in text box).
    Submitting the name adds it to all lists'''
    # sets up a new window, with an entrybox. Entrybox stored in argumentDict to access later.
    root = Tk()
    draw.addLabel(root, "What will this semester be called?")
    argumentDict["entryBox"] = Entry(root)
    argumentDict["entryBox"].pack()
    # Puts root in the argumentDict so we can delete this window later
    argumentDict["Frame"] = root
    # Adds submit and exit buttons to the bottom in one frame.
    draw.addButtonArguments(root, "Exit", destroyFrame, root, BOTTOM)
    draw.addButtonArguments(root, "Submit", submitData, argumentDict, BOTTOM)


def submitData(argumentDict):
    # gets the database
    database = argumentDict["controller"].database
    # Gets the text from the entryBox and checks if its empty
    text = argumentDict["entryBox"].get()
    if text != "":
        # If there's stuff in there, it adds a new course in both the file and the currentClasses list, updates
        # the original frame, and deletes the submission page
        database.newCourse(text)
        argumentDict["controller"].currentClasses.append(text)
        updateFrame(argumentDict)
        argumentDict["Frame"].destroy()




def deleteSemesterWarning(argumentDict):
    """
    Puts up a warning screen to ask if the user is sure they want to delete their course
    :param argumentDict:
    :return:
    """
    # Opens up new window, labels asking if they want to delete it.
    root3 = Tk()
    draw.addLabel(root3, "Are you sure you want to delete " + argumentDict["Course"] + "?")
    yesNoFrame = Frame(root3)
    # Also adds root3 to the argumentdict to be destroyed
    argumentDict["Frame3"] = root3
    draw.addButtonArguments(root3, "Delete", deleteSemester, argumentDict, LEFT)
    draw.addButtonArguments(root3, "No", destroyFrame, root3, RIGHT)
    yesNoFrame.pack()


def deleteSemester(argumentDict):
    """
    Takes the coursename to get deleted, removes warning frame, and updates the archivedsemester tab
    :param argumentDict:
    :return:
    """
    # Takes the course to be deleted
    course = argumentDict["Course"]
    newList = []
    # Puts in archived classes everything except the course
    for x in argumentDict["controller"].archivedClasses:
        if x != course:
            newList.append(x)
    argumentDict["controller"].archivedClasses = newList
    # Calls removeCourse
    argumentDict["controller"].database.removeCourse(course)
    # Destroys archivedSemester frame and re-calls it, destroys warning frame
    argumentDict["Frame2"].destroy()
    archivedSemester(argumentDict)
    argumentDict["Frame3"].destroy()


def archivedSemester(argumentDict):
    """
    Opens the window that lists all archived semesters and gives the user the option to unarchive or delete them
    :param argumentDict:
    :return:
    """

    # Opens up a new window and lists the classes that are archived, with options to unarchive or delete them
    root = Tk()
    # also adds the new root to the argumentDict so we can delete/update it later
    argumentDict["Frame2"] = root
    draw.addLabel(root, "Archived Class List:")
    for element in argumentDict["controller"].archivedClasses:
        setFrame = Frame(root)
        draw.addLabel(setFrame, element, RIGHT)
        argumentDict["Course"] = element
        draw.addButtonArguments(setFrame, "Unarchive", unarchive, argumentDict)
        deleteButton = Button(setFrame, text="Delete", bg="red", command=lambda: deleteSemesterWarning(argumentDict))
        deleteButton.pack()
        setFrame.pack()
    draw.addButtonArguments(root, "Exit", destroyFrame, root, BOTTOM)


def archive(argumentDict):
    """
    Actually archives a semester. Takes the coursename and brings it from the courselist to the archivedcourselist,
    and updates the editcourse frame
    :param argumentDict:
    :return:
    """


    # Pulls the coursename from the argument dictionary, adds it to the archivedclasses list, removes it from the
    # currentclases list, updates the editcourse frame and deletes/recreates the archive frame.
    course = argumentDict["Course"]
    argumentDict["controller"].archivedClasses.append(course)
    newList = []
    for x in argumentDict["controller"].currentClasses:
        if x != course:
            newList.append(x)
    argumentDict["controller"].currentClasses = newList
    updateFrame(argumentDict)
    # Also sets the course to be archived
    argumentDict["controller"].database.archiveCourse(course)


def unarchive(argumentDict):
    """
    Unarchives a semester. Takes the coursename and brings it from the archivedcourselist to the regular courselist.
    Also refreshes editcourse frame and archived course frame.
    :param argumentDict:
    :return:
    """
    # pulls the variables from the argumentDict
    database = argumentDict["controller"].database
    course = argumentDict["Course"]
    # takes the course to unarchive and puts it in the currentClasses
    argumentDict["controller"].currentClasses.append(course)
    # Makes a new list of everything in archivedClasses except the class to be unarchived, and sets archived classes
    # equal to the same list
    newList = []
    for x in argumentDict["controller"].archivedClasses:
        if x != course:
            newList.append(x)
    argumentDict["controller"].archivedClasses = newList
    #Updates all frames, this window.
    updateFrame(argumentDict)
    argumentDict["Frame2"].destroy()
    archivedSemester(argumentDict)
    # Also sets the course to be unarchived
    database.unarchiveCourse(course)


class ParticipationPage(tk.Frame):
    '''Participation page, which handles the Piazza information; displaying the data, entering the information to get the
    data'''
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        # sets up labels, button to update scores
        draw.addLabel(self, "Participation Options")
        draw.addButtonArguments(self, "Update Scores", updateParticipation, controller)
        # lists all classes with options to set the piazza URl and display their data as a graph and grid
        for element in controller.currentClasses:
            setFrame = Frame(self)
            draw.addLabel(setFrame, element, LEFT)
            argumentDict = {"course": element, "controller": self.controller}
            draw.addButtonArguments(setFrame, "Graph", displayParticipationGraph, argumentDict, RIGHT)
            draw.addButtonArguments(setFrame, "Grid", displayParticipationGrid, argumentDict, RIGHT)
            draw.addButtonArguments(setFrame, "Set Class URL", setClassURL, argumentDict, RIGHT)
            setFrame.pack()
        # back button
        draw.changePageButton(self, controller, "Back", "StartPage", BOTTOM)


# Helper Methods for ParticipationPage


def displayParticipationGrid(argumentDict):
    '''Displays participation in the form of a graph for a given class'''
    # Gets the data from the database and sets up dummy lists for the names and dates
    section = argumentDict["course"]
    database = argumentDict["controller"].database
    data = database.currentData()
    sectionId = database.getCourseIndex(section)
    names = []
    scores = []
    # Sets up the window upon which we put our grid
    root = Tk()
    # Sets up counting variable
    i = 0
    # Needs the list of names their respective participation scores, so we make two lists
    for student in data["courses"][sectionId]["students"]:
        names.append(student["name"])
        scores.append(student["PiazzaReportCard"])
        i += 1
    # lists names on right, scores on left
    i = 0
    for name in names:
        row = Label(root, text=name)
        row.grid(row=i, column=0)
        i += 1
    i = 0
    for score in scores:
        column = Label(root, text=score)
        column.grid(row=i, column=1)
        i += 1


def displayParticipationGraph(argumentDict):
    '''displays participation in the form of a graph'''
    # Takes all the variables out of the argumentDict, sets up lists for graphing purposes
    section = argumentDict["course"]
    database = argumentDict["controller"].database
    sectionId = database.getCourseIndex(section)
    data = database.currentData()
    names = []
    participationScores = []
    #Puts all student names in the names list
    for student in data["courses"][sectionId]["students"]:
        names.append(student["name"])
    # puts all piazzareportcards in the scores list
    for student in data["courses"][sectionId]["students"]:
        participationScores.append(student["PiazzaReportCard"])
    #graphs them both
    mpl.bar(names, participationScores)
    mpl.ylabel("Participation Score")
    mpl.xlabel("Student")
    mpl.show()


def updateParticipation(controller):
    """
    Opens a page that asks for the admin's username/password; then calls another function to pass those
    to the Piazza scraper.
    :return:
    """
    # sets up a new window, with two entryboxes
    root = Tk()
    draw.addLabel(root, "Enter Piazza Username:")
    box1 = Entry(root)
    box1.pack()
    draw.addLabel(root, "Enter Piazza Password:")
    # also password, when being entered, displays * instead of the actual password
    box2 = Entry(root, show="*")
    box2.pack()
    # lists all classes, with an option to submit the piazza data
    draw.addLabel(root, "Pick the class you want to update")
    for course in controller.currentClasses:
        submissionFrame = Frame(root)
        draw.addLabel(submissionFrame, course, LEFT)
        # Sets up data to pass
        argumentDict = {"usernameBox": box1, "passwordBox": box2, "frame": root, "controller" : controller, "course" : course}
        draw.addButtonArguments(submissionFrame, "Submit", submitPiazzaData, argumentDict, RIGHT)
        submissionFrame.pack()
    #back button
    draw.addButtonArguments(root, "Cancel", destroyFrame, root, BOTTOM)


def setClassURL(argumentDict):
    '''Function that opens a page in which people can enter a class URL'''
    #unpacks all the variables from argumentdict, gets the course index
    database = argumentDict["controller"].database
    data = database.currentData()
    sectionID = database.getCourseIndex(argumentDict["course"])
    #opens new frame, sets this new root to the frame, stores the location of the piazzaclass
    root = Tk()
    argumentDict["frame"] = root
    argumentDict["PiazzaClass"] = data["courses"][sectionID]["PiazzaClass"]
    # if there is no set piazzaclass, sets it to none, so it displays that there is no set class instead of
    # breaking everything
    if not argumentDict["PiazzaClass"]:
        argumentDict["PiazzaClass"] = "None"
    # lists the currently set URL and course
    draw.addLabel(root, "Enter Class URL for " + argumentDict["course"])
    draw.addLabel(root, "Type everything after the /, i.e. for piazza.com/class/abcd, type in abcd")
    draw.addLabel(root, "Current URL set as:" + argumentDict["PiazzaClass"])
    #makes an entrybox, stores it
    URL = Entry(root)
    URL.pack()
    argumentDict["box"] = URL
    # buttons to submit or to stop
    draw.addButtonArguments(root, "Submit", submitClassURL, argumentDict)
    draw.addButtonArguments(root, "Cancel", destroyFrame, root, BOTTOM)


def submitClassURL(argumentDict):
    '''Takes the inputted URL and sets the piazza ID for the course'''
    # makes sure its not empty
    if argumentDict["box"].get() != "":
        argumentDict["controller"].database.assignCoursePiazzaID(argumentDict["course"], argumentDict["box"].get())
        argumentDict["frame"].destroy()
        setClassURL(argumentDict)


def submitPiazzaData(argumentDict):
    '''Submits username/password/course and gets the piazza data'''
    #unpacks the data from the argumentDict
    database = argumentDict["controller"].database
    username = argumentDict["usernameBox"].get()
    password = argumentDict["passwordBox"].get()
    course = argumentDict["course"]
    # makes sure that something is submitted for both
    if username != "" and password != "":
        #gets the data, sectionid, and calls for the Piazzadata
        data = database.currentData()
        sectionID = database.getCourseIndex(course)
        courseURL = data["courses"][sectionID]["PiazzaClass"]
        piazzaData = scraper().run(courseURL, username, password)[0]
        # stores the piazzadata in a student of the same name, if it exists
        for student in data["courses"][sectionID]["students"]:
            if student["name"] in piazzaData:
                student["PiazzaReportCard"] = piazzaData[student["name"]]


def seeStudents(argumentDict):
    '''Displays all the students for a class'''
    # Makes a new window, gets section ID/data
    controller = argumentDict["controller"]
    database = controller.database
    section = argumentDict["Course"]
    root = Tk()
    draw.addLabel(root, "Student List:")
    sectionId = database.getCourseIndex(section)
    data = database.currentData()
    # Lists all students, stores information in the argumentDict, and gives remove button.
    for student in data["courses"][sectionId]["students"]:
        setFrame = Frame(root)
        draw.addLabel(setFrame, student["name"], LEFT)
        argumentDict = {}
        argumentDict2 = {"Student":student,"Course": section, "Frame": root, "controller" : controller}
        draw.addButtonArguments(setFrame, "Remove", removeStudentWarning, argumentDict2, RIGHT)
        setFrame.pack()
    #back button
    draw.addButtonArguments(root, "Exit", destroyFrame, root, BOTTOM)


def setPiazzaID(argumentDict):
    '''Opens a set piazza ID window for a given student; developed in case we needed this information, but ultimately
    went unused
    Should pass an argumentdict with the coursename set to "Course" and access to the controller under "controller"
    '''
    root2 = Tk()

    argumentDict["Frame"] = root2
    draw.addLabel(root2, "Submit Student's Piazza ID")
    argumentDict["entryBox"] = Entry(root2)
    argumentDict["entryBox"].pack()
    # Adds submit and exit buttons to the bottom in one frame.
    draw.addButtonArguments(root2, "Submit", submitPiazzaID, argumentDict, BOTTOM)


def submitPiazzaID(argumentDict):
    '''Submit's student's piazza id. Went unused.'''
    database = argumentDict["controller"].database
    student = argumentDict["Student"]
    classSection = argumentDict["Course"]
    currentFrame = argumentDict["Frame"]
    piazzaID = argumentDict["entryBox"].get()
    if piazzaID != "":
        database.assignPiazzaID(classSection, student["name"], piazzaID)
        currentFrame.destroy()


def removeStudentWarning(argumentDict):
    '''Puts a warning label when trying tod elete a student so the user doesn't delete a student by accident'''
    # makes new window
    root3 = Tk()
    # Puts the window in argumentDict so we can delete it later
    argumentDict["WarningFrame"] = root3
    # Draws delete button, "no" button, and warning label
    draw.addLabel(root3, "Are you sure you want to delete " + argumentDict["Student"]["name"] + " from the course " +
                  argumentDict["Course"] + "?")
    yesNoFrame = Frame(root3)
    draw.addButtonArguments(yesNoFrame, "Delete", removeStudent, argumentDict, LEFT)
    draw.addButtonArguments(yesNoFrame, "No", destroyFrame, root3, RIGHT)
    yesNoFrame.pack()

def removeStudent(argumentDict):
    '''Removes a student and closes the window that calls it'''
    #unpacks database
    database = argumentDict["controller"].database
    # Calls the removestudent funciton, resets seestudents window, removes warning window
    database.removeStudent(argumentDict["Course"], argumentDict["Student"]["name"])
    argumentDict["Frame"].destroy()
    argumentDict["WarningFrame"].destroy()
    # displays the student page again
    seeStudents(argumentDict)


def updateFrame(argumentDict):
    '''Takes an argumentdict containing the controller and the current frame, and redraws the frames of the GUI
    to update new changes'''
    # We go in argumentFrame and get the currentframe and the controller, then pull the list of frames and the
    # container containing all the frames
    controller = argumentDict["controller"]
    topPage = argumentDict["CurrentFrame"]
    frameList = controller.listFrames()
    frameSet = controller.getFrameSet()
    # for every frame, we redraw it and put it in the container, and change the reference to these new redrawn frames
    for frameName in frameList:
        updatedFrame = controller.frameTypes[frameName](parent=frameSet, controller=controller)
        updatedFrame.grid(row=0, column=0, sticky="nsew")
        controller.frames[frameName] = updatedFrame
    # then we set the top page to the top
    changePage(controller, topPage)


def signInMode(controller):
    '''Opens a page that lets the user choose which class they want to put in signin mode'''
    #makes a new window
    root = Tk()
    draw.addLabel(root, "Which class do you want students to sign in to?:")
    # lists all the classes, with options to initiate signin mode for that class
    for element in controller.currentClasses:
        setFrame = Frame(root)
        draw.addLabel(setFrame, element, LEFT)
        # stores some values to send to setClass
        argumentDict = {"Class": element, "Frame": root, "lastStudent": "None", "controller" : controller}
        draw.addButtonArguments(setFrame, "Select", setClass, argumentDict, RIGHT)
        setFrame.pack()
    #back button
    draw.addButtonArguments(root, "Cancel", destroyFrame, root, BOTTOM)


def setClass(argumentDict):
    '''Puts the program into signinmode for some given class; choosing to scan and placing a onecard will
    update attendance for that student'''
    # unpacks the variables from argumentDict, gets the data from the database and the list of students from that
    section = argumentDict["Class"]
    baseFrame = argumentDict["Frame"]
    data = argumentDict["controller"].database.currentData()
    students = data["courses"][argumentDict["controller"].database.getCourseIndex(section)]["students"]
    # checks if there are students in the class to see if it can access past data
    if len(students) > 0:
        # if it can't find today's date some student's list of classperiods, it makes a new one and stores it
        if str(date.today()) not in students[0]["attendance"]["classPeriods"].keys():
            classPeriod = argumentDict["controller"].database.newClassPeriod(section)
        else:
        # otherwise, it sets the period to today's class
            classPeriod = str(date.today())
    else:
    # if it can't access past data, it just sets a new class period for this class.
        classPeriod = argumentDict["controller"].database.newClassPeriod(section)

    # get rid of the last frame, either to remove signInMode page or update this page with the last student called
    baseFrame.destroy()
    # new page, stores it
    root = Tk()
    argumentDict["Frame"] = root
    # passes ArgumentDict the classPeriod for later use
    argumentDict["classPeriod"] = classPeriod
    # Label, button to stop signing in
    draw.addLabel(root, "Signing in for:" + section)
    draw.addButtonArguments(root, "Stop Signing In", stopSignIn, argumentDict)
    draw.addButtonArguments(root, "Scan", scanSignIn, argumentDict)
    # If the last student called is None (first time called), says nobody signed in yet
    if argumentDict["lastStudent"] == "None":
        draw.addLabel(root, "No Students Signed In Yet This Session")
    # if we don't know who the student is, we say so
    elif argumentDict["lastStudent"] == "Unknown":
        draw.addLabel(root, "Unknown card -- enroll this student in the class first")
    else:
        # otherwise, we must have found the student, and so we put their name to let the user know it worked
        draw.addLabel(root, "Last student signed in:" + argumentDict["lastStudent"])


def scanSignIn(argumentDict):
    '''Waits for a scan from the RFID, then stores whatever it gets into the argumentDict and passes to the signInStudent'''
    oneCard = RFID.singleScan()
    argumentDict["oneCard"] = oneCard
    signInStudent(argumentDict)


def signInStudent(argumentDict):
    '''Takes a argumentDict with the onecard id stored inside, signs that student in, and updates the page to show that
    this student has signed in'''
    # uses the signin method in the database to say that the student corresponding to this onecard has arrived for that
    # given class period
    argumentDict["controller"].database.signIn(argumentDict["Class"], argumentDict["oneCard"], argumentDict["classPeriod"])
    # Looks through all the students in the class to find the last one that signed in.
    data = argumentDict["controller"].database.currentData()
    students = data["courses"][argumentDict["controller"].database.getCourseIndex(argumentDict["Class"])]["students"]
    studentFound = "Unknown"
    # Gets the name of the last student signed in by iterating through the data in the class until we find the
    # student who has the proper oneCard
    for student in students:
        if student["OneCard"] == argumentDict["oneCard"]:
            studentFound = student["name"]
    # Now that we found the student, we destroy/redraw the frame with the new student name attached
    argumentDict["lastStudent"] = studentFound
    setClass(argumentDict)


def stopSignIn(argumentDict):
    argumentDict["Frame"].destroy()
    signInMode(argumentDict["controller"])


# Enrollment Mode Notes:
# Need: coursename, studentname, onecard
# Passed the coursename, get studentname from textbox, onecard from scanner
# To get onecard, when you initialize the scanner (scanner = RFID), parameter that RFID requires is a function, which
# is passed OneCard -- type in the name (to get the class, name), then call callback function, which submits those two
# and the onecard into the datainteract stuff.

def enrollmentMode(controller):
    root = Tk()
    draw.addLabel(root, "Select which course in which to enter enrollmentMode")
    for element in controller.currentClasses:
        setFrame = Frame(root)
        draw.addLabel(setFrame, element, LEFT)
        argumentDict = {"Class": element, "Frame": root, "controller": controller}
        draw.addButtonArguments(setFrame, "Select", enrollInClass, argumentDict, RIGHT)
        setFrame.pack()
    draw.addButtonArguments(root, "Cancel", destroyFrame, root, BOTTOM)


def enrollInClass(argumentDict):
    """
    Takes a dictionary containing a frame and the coursename. This opens up a new frame in which the user can
    input a student's name and enroll them in the chosen course.
    :param argumentDict:
    :return:
    """
    # Gets rid of the enrollmentmode frame and makes a new one
    argumentDict["Frame"].destroy()
    root = Tk()
    argumentDict["Frame"] = root
    draw.addLabel(root, "Enter in the student's name, then scan their card to enroll in " + argumentDict["Class"])
    # Adds the entry box with which the student name is entered
    argumentDict["entryBox"] = Entry(root)
    argumentDict["entryBox"].pack()
    # Lists the students thus far. Grabs the data from the database, then prints all their names as labels
    draw.addLabel(root, "Students enrolled so far:")
    data = argumentDict["controller"].database.currentData()
    courseId = argumentDict["controller"].database.getCourseIndex(argumentDict["Class"])
    for student in data["courses"][courseId]["students"]:
        draw.addLabel(root, student["name"], LEFT)
    # Scan button
    draw.addButtonArguments(root, "Scan", scanEnrollment, argumentDict)
    # Adds a back button, which calls a function that stops the scanner and brings us back to the last page
    draw.addButtonArguments(root, "Stop", stopEnrollment, argumentDict)


def scanEnrollment(argumentDict):
    '''Gets data from enrollment entryBox, gets oneCard from scanner, then passes both to
    enrollStudent'''
    # makes sure the box isnt empty
    if argumentDict["entryBox"].get() != "":
        #scans for card
        oneCard = RFID.singleScan()
        #stores it
        argumentDict["oneCard"] = oneCard
        #passes it
        enrollStudent(argumentDict)


def enrollStudent(argumentDict):
    """
    From the scanner, this creates a new student given a onecard id. Only works if the enrollInClass window is open,
    to get the name/class.
    :param oneCard:
    :return:
    """

    # Gets the name from the entry box
    name = argumentDict["entryBox"].get()
    # Only updates if something was actually typed into the box
    if name != "":
        # Adds the new student into the class
        argumentDict["controller"].database.newStudent(argumentDict["Class"], name, argumentDict["oneCard"])
        # Then, it destroys the frame and re-draws it with the name of the students enrolled by re-calling the
        # enrollInClass method
        enrollInClass(argumentDict)


def stopEnrollment(argumentDict):
    '''Stops enrollmentmode, destroys enrollmentmode frame, and re-creates the enrollmentmode
    page'''
    argumentDict["Frame"].destroy()
    enrollmentMode(argumentDict["controller"])


class draw(tk.Tk):
    '''A class that makes drawing labels/buttons take up less space, since we do that a lot'''
    def addButton(parent, text, call, side=TOP):
        '''Adds a button that doesn't need arguments. Needs its root, some text, its command, and
        optionally what side it goes on'''
        button = Button(parent, text=text, command=call)
        button.pack(side=side)

    def addButtonArguments(parent, text, call, argument, side=TOP):
        '''Adds a button with arguments, limited to 1. Needs the root, some text for the button, its command, the
        argument that goes in it, and optionally, what side it goes on'''
        button = Button(parent, text=text, command=lambda: call(argument))
        button.pack(side=side)

    def addLabel(parent, text, side=TOP):
        '''Adds a label. Needs a root and what text goes on it, plus optionally what side it goes on'''
        label = Label(parent, text=text)
        label.pack(side=side)

    def changePageButton(parent, controller, text, pageName, side=TOP):
        '''Adds a button that changes the page; needs a root, a reference to the main GUI object, some text for the button,
        the name of the page you want to display, and what side the button goes on.'''
        button = Button(parent, text=text, command=lambda: controller.showFrame(pageName))
        button.pack(side=side)


if __name__ == "__main__":
    app = GUI()
    app.mainloop()
