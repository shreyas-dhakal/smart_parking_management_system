
from google_drive_downloader import GoogleDriveDownloader as gdd

gdd.download_file_from_google_drive(file_id='1qYkURFNtmveo4lmEMQfJ1M6HYtt60gNk',
                                    dest_path='data/plate_detection.zip',
                                    unzip=True)