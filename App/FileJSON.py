import json

def isValidJSON(data):
    """
    Checks whether a string is valid JSON.
    Code borrowed from Eric Leschinski on Stack Overflow
    https://stackoverflow.com/questions/5508509/how-do-i-check-if-a-string-is-valid-json-in-python
    :param data:
    :return:
    """
    try:
        object = json.loads(data)
    except ValueError as e:
        return False
    return True

class FileJSON:
    """
    A general purpose class to interact with JSON files.
    """
    def __init__(self, path):
        """
        Requires the path to the JSON file. If the file does not exist, it will be created.
        :param path:
        """
        # Save path to JSON
        self.path = path
        # Open file, read only
        self.file = open(self.path, "r")
        # Save plaintext
        self.text = self.file.read()
        # Initialize data
        self.data = {}
        # If valid JSON, convert to dictionary and save as self.data
        if isValidJSON(self.text):
            self.data = json.loads(self.text)
            self.file.close()
    def print(self):
        """
        Prints the JSON data
        """
        print(self.data)
    def write(self, new):
        """
        Overwrites the file with new data.
        :param new:
        :return:
        """
        with open(self.path, 'w+', newline='\r\n') as json_file:
            # Clear file
            json_file.truncate(0)
            # Write new data
            json.dump(new, json_file, separators=(',', ':'))
            # Update text to new file content
            self.text = json_file.read()
            # Update data to new file content
            self.data = new
            # Close file
            json_file.close()