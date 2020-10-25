import threading
from random import randint

# Default to running on Raspberry Pi
RunningOnPi = True

# Check whether RPi and mfrc522 installed.
# If not, program acts like not running on Pi and scans are simulated
try:
    import RPi.GPIO as GPIO
    import sys
    sys.path.append('~/home/pi/MFRC522-python')
    from mfrc522 import SimpleMFRC522
except:
    RunningOnPi = False
    print("Not running on Raspberry Pi. Scans will be simulated.")


class FakeReader:
    """
    A class that copies the behavior of SimpleMFRC522, but asks for command line input rather than scans
    """
    def __init__(self):
        pass
    def read(self):
        toPass = str(input("Enter simulated tag ID:"))
        return (toPass,"")

# If not running on Pi, use fake reader
if RunningOnPi:
    reader = SimpleMFRC522()
else:
    reader = FakeReader()


def log(id):
    """
    A function that mirrors print() without using reserved names
    :param id:
    :return:
    """
    print(id)

class RFID:
    """
    RFID is the scanning interface.
    """
    def __init__(self, callback=log):
        """
        When initializing RFID, you should pass it a callback function that it will call when an RFID tag is scanned.
        The callback function is passed the id of the tag.
        :param callback:
        """
        self.keepScanning = True
        self.callback = callback
        self.lastScanned = None

    def singleScan():
        """
        Scans once on main thread. Halts the rest of the program.
        :return:
        """
        return str(reader.read()[0])

    def scanIndefinitely(self):
        """
        scanIndefinitely() listens for RFID scans FOREVER.
        It should not be called directly in the main thread.
        Instead, use RFID.start().
        :return:
        """
        try:
            # While stop() method has not been called
            while self.keepScanning:
                # Listen for scans
                id, text = reader.read()
                # If scan not identical to previous scan
                if id != self.lastScanned:
                    # Save id as lastScanned
                    self.lastScanned = id
                    # Pass id to callback
                    self.callback(id)
        except:
            raise
            if RunningOnPi:
                GPIO.cleanup()

    def start(self):
        """
        This is the recommended way to begin listening for RFID scans.
        Use stop() when you wish to stop listening.
        :return:
        """
        print("Hold a tag near the reader")
        # Initialized and runs new thread solely for scan listening
        ScanThread = threading.Thread(target=self.scanIndefinitely)
        ScanThread.start()

    def stop(self):
        """
        This tells the scanner to stop listening for scans.
        :return:
        """
        # Stop scanning
        self.keepScanning = False

    def simulateScan(self, id=None):
        """
        This simulates the behavior of scanning a tag.
        By default, it calls the callback function using a random integer as the tag id.
        You can also specify a tag id with the 'id' parameter.
        Use this for debugging purposes or when you don't have physical access to the scanner.
        :param id:
        :return:
        """
        # If no ID param
        if id is None:
            # Create random id
            id = randint(1000000000,9999999999)
        # Run callback with fake ID
        self.callback(id)