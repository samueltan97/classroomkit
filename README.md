# Classroom Kit
## A tool developed by Samuel Tan, Joseph Gentile, and Isaac Wasserman
Final Presentation: https://docs.google.com/presentation/d/1Y20Ut0iORKRF5RvxIgfKKal15aO16YJvYNLWwW4gGBo/edit?usp=sharing
## Running
To run Classroom Kit from the command line, run: `python App/GUI.py` or `python3 App/GUI.py` if using MacOS. If you're
not running the program on a Raspberry Pi with the required peripherals, all RFID scans will be simulated. This means that when you click the "Scan" button, you will be prompted in the command line to enter a simulated tag ID.
## How to use the application:

To use this application, you must first make a class, in the editClasses menu, which you could archive or delete.
To add students, you have to go into enrollment mode under attendance options; there, you pick the class, then enter
 student’s name and press scan. If you are running the Raspberry Pi, simply scan the required identification card,
 which will then be linked to their name. If you are not, enter in an id in the command line which will be used to sign
 them in.

To sign them in, go into sign in mode (also under attendance options), pick a class, then scan for the card or enter
the aforementioned id in the command line to add them to today’s class for that class.


As for piazza, you need to have a piazza page for that class, and enter that URL into the program; to do that, go to
the Set Class URL button under participationOptions next to the class of your choice. To update the data, go into the
Update Participation menu and enter in a piazza username/password for an account that has access to that piazza class,
then pick the class to update.