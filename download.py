import os
import logging
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Google Drive API configuration
API_KEY = os.getenv('GOOGLE_DRIVE_API_KEY')
drive_service = build('drive', 'v3', developerKey=API_KEY)

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def list_files_in_folder(folder_id):
    """List all files in a specified Google Drive folder."""
    try:
        query = f"'{folder_id}' in parents"
        results = drive_service.files().list(
            q=query,
            fields="files(id, name)"
        ).execute()
        items = results.get('files', [])
        if not items:
            logger.info(f"No files found in the folder with ID: {folder_id}")
        else:
            logger.info(f"Found {len(items)} files in the folder.")
        return items
    except Exception as e:
        logger.error(f"Error listing files in folder: {e}")
        return []


def download_file(file_id, file_name, output_dir='models'):
    """Download a file from Google Drive by file ID."""
    try:
        request = drive_service.files().get_media(fileId=file_id)
        output_path = os.path.join(output_dir, file_name)
        os.makedirs(output_dir, exist_ok=True)
        
        with open(output_path, 'wb') as file:
            downloader = MediaIoBaseDownload(file, request)
            done = False
            while not done:
                status, done = downloader.next_chunk()
                logger.info(f"Downloading {file_name}: {int(status.progress() * 100)}%")
        logger.info(f"Downloaded {file_name} to {output_path}")
    except Exception as e:
        logger.error(f"Error downloading file {file_name}: {e}")


def download_all_models_from_folder(folder_id, output_dir='models'):
    """Download all files in a Google Drive folder to the /models directory."""
    files = list_files_in_folder(folder_id)
    if not files:
        logger.warning("No files found in the folder.")
        return
    
    for file in files:
        file_id = file['id']
        file_name = file['name']
        logger.info(f"Starting download for {file_name} (ID: {file_id})")
        download_file(file_id, file_name, output_dir)
