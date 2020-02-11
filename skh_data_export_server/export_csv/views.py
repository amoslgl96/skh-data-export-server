# import csv
# import boto3
# import io
# import logging
import sys
import os

# from botocore.exceptions import ClientError

from django.shortcuts import render, HttpResponse
from django.core.mail import EmailMessage

# from .models import SensorReading

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

from django.http import JsonResponse

# Create your views here.
def hello_world(request):
    return render(request, 'hello_world.html', {})

# for s3 bucket
# def export_csv(request):

#     sensor_readings = SensorReading.objects.all()


#     buff =  io.StringIO()

#     writer = csv.writer(buff, delimiter=',')

#     # write headers
#     writer.writerow(['day','steps_taken','heart_rate','medication_taken'])

#     for reading_obj in sensor_readings:
#         writer.writerow([reading_obj.day,reading_obj.steps_taken,reading_obj.heart_rate,reading_obj.medication_taken])
    
#     buff = io.BytesIO(buff.getvalue().encode())

#     s3_client = boto3.client('s3')
#     s3_client.upload_fileobj(buff, 'skh-data-test','skh-data-test.csv')

#     try:
#         response = s3_client.generate_presigned_url('get_object',
#                                                     Params={'Bucket': 'skh-data-test',
#                                                             'Key': 'skh-data-test.csv'},
#                                                     ExpiresIn=3600)
#     except ClientError as e:
#         logging.error(e)
#         return None

#     return HttpResponse(response)


# FOR GOOGLE - DRIVE
# def export_csv(request):

#     GoogleAuth.DEFAULT_SETTINGS['client_config_file'] = os.path.join(os.path.abspath("export_csv/client_secrets.json")) 

#     gauth = GoogleAuth()
#     gauth.LocalWebserverAuth()

#     drive = GoogleDrive(gauth)

#     # file1 = drive.CreateFile({'title': 'Hello.txt'})  # Create GoogleDriveFile instance with title 'Hello.txt'.
#     # file1.SetContentString('Hello World!') # Set content of the file from given string.
#     # file1.Upload()
#     file1 = drive.CreateFile({"mimeType": "text/csv", "title": 'table.csv'})
#     file1.SetContentFile(os.path.join(os.path.abspath("export_csv/table.csv")))
#     file1.Upload()
    
#     gauth.SaveCredentialsFile("mycreds.txt")

#     return JsonResponse({'foo':'bar'})

# Using service account:

def export_csv(request):

    import tempfile
    from apiclient import discovery
    from apiclient.http import MediaFileUpload

    def credentials_from_file():
        """Load credentials from a service account file
        Args:
            None
        Returns: service account credential object
        
        https://developers.google.com/identity/protocols/OAuth2ServiceAccount
        """
        
        from google.oauth2 import service_account
        import googleapiclient.discovery

        # https://developers.google.com/identity/protocols/googlescopes#drivev3
        SCOPES = [
            'https://www.googleapis.com/auth/drive'
        ]
        SERVICE_ACCOUNT_FILE = os.path.join(os.path.abspath("export_csv/skh-hams-gdrive-ad23b147b8a7.json"))
        
        credentials = service_account.Credentials.from_service_account_file(
                SERVICE_ACCOUNT_FILE, scopes=SCOPES)
                
        return credentials

    # Set your Google email address here
    userEmail = 'baolgl96@gmail.com'

    credentials = credentials_from_file()
    service = discovery.build('drive', 'v3', credentials=credentials)

    # Create a folder
    # https://developers.google.com/drive/v3/web/folder

    folder_metadata = {
        'name': 'My Test Folder',
        'mimeType': 'application/vnd.google-apps.folder'
    }
    cloudFolder = service.files().create(body=folder_metadata).execute()

    # Upload a file in the folder
    # https://developers.google.com/api-client-library/python/guide/media_upload
    # https://developers.google.com/drive/v3/reference/files/create

    file_metadata = {
        'name': 'A Test File',
        'parents': [cloudFolder['id']]
    }

    with tempfile.NamedTemporaryFile(mode='w') as tf:
        tf.write("This is some test data")

        # https://developers.google.com/api-client-library/python/guide/media_upload
        media = MediaFileUpload(tf.name, mimetype='text/plain')
        # https://developers.google.com/drive/v3/web/manage-uploads
        cloudFile = service.files().create(body=file_metadata).execute()

    # Share file with a human user
    # https://developers.google.com/drive/v3/web/manage-sharing
    # https://developers.google.com/drive/v3/reference/permissions/create

    cloudPermissions = service.permissions().create(fileId=cloudFile['id'], 
        body={'type': 'user', 'role': 'reader', 'emailAddress': userEmail}).execute()

    cp = service.permissions().list(fileId=cloudFile['id']).execute()
    print(cp)

    # List files in our folder
    # https://developers.google.com/drive/v3/web/search-parameters
    # https://developers.google.com/drive/v3/reference/files/list

    query = "'{}' in parents".format(cloudFolder['id'])
    filesInFolder = service.files().list(q=query, orderBy='folder', pageSize=10).execute()
    items = filesInFolder.get('files', [])

    # Print the paged results
    if not items:
        print('No files found.')
    else:
        print('Files:')
        for item in items:
            print('{0} ({1})'.format(item['name'], item['id']))
            # service.files().delete(fileId=item['id']).execute()  # Optional cleanup