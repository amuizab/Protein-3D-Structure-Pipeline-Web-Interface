import os
import apache_beam as beam
from google.cloud import storage

class UploadToGCS(beam.DoFn):
    def __init__(self, bucket_name, destination_path):
        self.bucket_name = bucket_name
        self.destination_path = destination_path
        self.client = None

    def setup(self):
        # Initialize the GCS client once per worker
        self.client = storage.Client()

    def process(self, file_path):
        # Extract the file name
        file_name = os.path.basename(file_path)
        # Build the GCS destination path
        gcs_blob_path = f"{self.destination_path}/{file_name}"
        # Upload the file to GCS
        bucket = self.client.bucket(self.bucket_name)
        blob = bucket.blob(gcs_blob_path)
        blob.upload_from_filename(file_path)
        yield f"Uploaded {file_path} to gs://{self.bucket_name}/{gcs_blob_path}"


# Configuration
bucket_name = "xxxx"  # Replace with your GCS bucket name
destination_path = "pdb_files"  # The target folder in GCS
local_folder = "/content/pdb_files"  # Folder containing your .pdb files

# List all files in the local folder
def list_files(folder):
    for root, _, files in os.walk(folder):
        for file in files:
            yield os.path.join(root, file)


# Apache Beam Pipeline
with beam.Pipeline() as pipeline:
    (
        pipeline
        | "List Files" >> beam.Create(list_files(local_folder))  # Step 1: List all files
        | "Upload Files" >> beam.ParDo(UploadToGCS(bucket_name, destination_path))  # Step 2: Upload files
        | "Print Results" >> beam.Map(print)  # Step 3: Print results
    )
