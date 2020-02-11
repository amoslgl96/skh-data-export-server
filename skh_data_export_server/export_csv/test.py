from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive



gauth = GoogleAuth()

"""
LocalWebserverAuth() is a built-in method of GoogleAuth which sets up local webserver to automatically receive authentication code from user and authorizes by itself. You can also use CommandLineAuth() which manually takes code from user at command line.
"""
gauth.LocalWebserverAuth()

drive = GoogleDrive(gauth)

# file1 = drive.CreateFile({'title': 'Hello.txt'})  # Create GoogleDriveFile instance with title 'Hello.txt'.
# file1.SetContentString('Hello World!') # Set content of the file from given string.
# file1.Upload()

file1 = drive.CreateFile({"mimeType": "text/csv"})
file1.SetContentFile("table.csv")
file1.Upload()

