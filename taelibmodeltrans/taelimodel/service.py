from google.oauth2 import service_account
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
# from gdstorage.storage import GoogleDriveStorage, GoogleDrivePermissionType, GoogleDrivePermissionRole, GoogleDriveFilePermission
from django.conf import settings
from django.contrib import messages
import logging
import os
logger = logging.getLogger('taelimodel')

class DriveFileUploadService:
    def __init__(self):
        """ 
        initing google credintial  fiel and fiel id 
        """
        credentials = service_account.Credentials.from_service_account_file(
            settings.GOOGLE_SERVICE_CREDINTIAL_JSON,
            scopes=['https://www.googleapis.com/auth/drive.file']
        )
        
        self.folder_id=settings.GOOGLE_DRIVE_FOLDER_ID
        self.drive_service = build('drive','v3',credentials=credentials)

    def upload(self,filepath,pk,bookname):
        """ 
        Uploads the file to Google Drive and returns the file ID.
        """
        # if not os.path.isfile(filepath):
        #     logger.error(f"File does not exist: {filepath}")
        #     return None 
        if not filepath:
            print("No file to upload.")
            return None
        print(f"to upload. {filepath}")

        file_metada= {
            'name':f'{pk}_{bookname}',
            'parents':[self.folder_id]
        }

        media = MediaFileUpload(filepath,resumable=True)
        try:
        # upload_file = drive_service.files().create(body=file_metada, media)
            upload_file =  self.drive_service.files().create(body=file_metada, media_body=media).execute()
            permission = {
            'type':'anyone',
            'role':'reader',
            'allowFileDiscovery':False,    
            'copyContent': False,
            'viewersCanCopyContent': False, 
            'canShare': False
             }
            self.drive_service.permissions().create(fileId=upload_file.get('id'), body=permission).execute()
            print(f"File uploaded: {upload_file.get('id')}")  # Print the ID of the uploaded file
            return upload_file.get('id')  # Return the Google Drive file ID

        except Exception as e:
            # print(f"An error occurred: {e}")
            logger.error(f"An error occurred during file upload: {e}")
            # messages.error(request, "An error occurred during file upload. Please try again.") 
            return None
