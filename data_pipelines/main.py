

from datagenes import download_file
from map2uniprot import map_gene_to_uniprot
from downloadpdb import download_pdb

import concurrent.futures
import requests
import os
import sqlite3
import threading
from tqdm import tqdm  # Import tqdm for progress bar

from google.cloud import storage
from concurrent.futures import ThreadPoolExecutor, as_completed


def main():
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'credentials.json' #Specify your Credentials

    #Connect to gs://fh-public/wikicrow2
    bucket_name = 'fh-public'  # Replace with your bucket name
    prefix = 'wikicrow2/'

    client = storage.Client()
    bucket = client.bucket(bucket_name)

    #get all the files with concurrent exectuion
    blobs = client.list_blobs(bucket, prefix=prefix)
    data_files = [blob.name for blob in blobs ]


    # Define a local directory to store downloaded data
    download_dir = 'wikicrow2'
    os.makedirs(download_dir, exist_ok=True)


    # Specify the number of threads.
    # You can adjust this number based on your system's capabilities and network bandwidth.
    MAX_WORKERS = 10

    # Use ThreadPoolExecutor to manage concurrent downloads
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        # Submit all download tasks to the executor
        future_to_file = {executor.submit(download_file, file_name): file_name for file_name in data_files}

        # As each task completes, handle the result
        for future in as_completed(future_to_file):
            file_name = future_to_file[future]
            try:
                result = future.result()
                if result:
                    # Optional: Additional processing can be done here
                    pass
            except Exception as exc:
                print(f"{file_name} generated an exception: {exc}")

    file_keys = [file.replace('.txt', '') for file in data_files if file.endswith('.txt')]
    file_keys = [file.replace('wikicrow2/', '') for file in file_keys]

    db_lock = threading.Lock()

    def process_gene(x_and_y):
        x, y = x_and_y
        try:
            with open(y, "r") as f:
                description = f.read()
        except Exception as e:
            tqdm.write(f"Error reading file {y}: {e}")
            description = ""

        gene_name = x
        gene_uniprot_tuple = map_gene_to_uniprot(gene_name)
        download_pdb(gene_uniprot_tuple)
        gene, uniprot_id = gene_uniprot_tuple
        gene_pdb_tuple = (gene_uniprot_tuple)
        gene, pdb_file_path = gene_pdb_tuple

        # Insert into SQL database
        with db_lock:
            cursor.execute('''
                INSERT INTO genes (gene_name, description, uniprot_id, pdb_file)
                VALUES (?, ?, ?, ?)
            ''', (gene_name, description, uniprot_id, pdb_file_path))
            conn.commit()

        return (gene_name, description, uniprot_id, pdb_file_path)

    # Create the database connection
    conn = sqlite3.connect('genes.db', check_same_thread=False)
    cursor = conn.cursor()

    # Create the table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS genes (
            gene_name TEXT,
            description TEXT,
            uniprot_id TEXT,
            pdb_file TEXT
        )
    ''')
    conn.commit()

    # Use ThreadPoolExecutor for concurrency
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Wrap the executor.map call with tqdm for progress bar
        results = list(tqdm(
            executor.map(process_gene, zip(file_keys, data_files)),
            total=len(file_keys),
            desc="Processing Genes",
            unit="gene"
        ))

    # Close the database connection
    conn.close()

    print("Processing complete. Data stored in 'genes.db' database.")



if __name__ == '__main__':
    main()