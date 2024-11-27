import os
from google.cloud import storage
from concurrent.futures import ThreadPoolExecutor, as_completed


def download_file(file_name, bucket, download_dir, data_files):
    """
    Downloads a single file from the bucket to the local directory.

    Args:
        file_name (str): The name/path of the file in the bucket.

    Returns:
        str: The name of the downloaded file.
    """
    try:
        blob = bucket.blob(file_name)
        local_path = os.path.join(download_dir, os.path.basename(file_name))

        # Download the file
        blob.download_to_filename(local_path)
        print(f"Downloaded {file_name} to {local_path}")
        return file_name
    except Exception as e:
        print(f"Failed to download {file_name}: {e}")
        return None

