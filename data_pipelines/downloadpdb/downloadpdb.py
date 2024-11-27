import concurrent.futures
import requests
import os
import sqlite3
import threading
from tqdm import tqdm  # Import tqdm for progress bar


def construct_alphafold_pdb_url(uniprot_id, model, version):
    base_url = "https://alphafold.ebi.ac.uk/files"
    pdb_url = f"{base_url}/AF-{uniprot_id}-{model}-model_v{version}.pdb"
    return pdb_url

# Function to download PDB files
def download_pdb(gene_uniprot_tuple, output_dir='pdb_files'):
    gene, uniprot_id = gene_uniprot_tuple

    if not uniprot_id:
        tqdm.write(f"Skipping download for gene '{gene}' due to missing UniProt ID.")
        return (gene, None)

    versions = ['4', '3', '2', '1']
    models = ['F1', 'F2', 'F3', 'F4', 'F5']

    os.makedirs(output_dir, exist_ok=True)

    for version in versions:
        for model in models:
            pdb_url = construct_alphafold_pdb_url(uniprot_id, model, version)
            filename = f"AF-{uniprot_id}-{model}-model_v{version}.pdb"
            save_path = os.path.join(output_dir, filename)

            try:
                response = requests.get(pdb_url, stream=True)
                if response.status_code == 200:
                    with open(save_path, 'wb') as file:
                        for data in response.iter_content(1024):
                            file.write(data)
                    return (gene, os.path.abspath(save_path))  # Return absolute path
                else:
                    continue
            except Exception as err:
                tqdm.write(f"Error downloading {filename} for UniProt ID '{uniprot_id}': {err}")
                continue

    tqdm.write(f"No PDB files found for UniProt ID '{uniprot_id}' for gene '{gene}'.")
    return (gene, None)