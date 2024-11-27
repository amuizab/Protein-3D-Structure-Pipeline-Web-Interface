import concurrent.futures
import requests
import os
import sqlite3
import threading
from tqdm import tqdm  # Import tqdm for progress bar




# Function to map gene names to UniProt IDs
def map_gene_to_uniprot(gene_name, organism_id=9606):
    base_url = "https://rest.uniprot.org/uniprotkb/search"
    query = f"gene_exact:{gene_name} AND organism_id:{organism_id}"
    params = {
        "query": query,
        "format": "json",
        "fields": "accession",
        "size": 1  # Only top result
    }

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data = response.json()

        if data['results']:
            uniprot_id = data['results'][0]['primaryAccession']
            return (gene_name, uniprot_id)
        else:
            tqdm.write(f"No UniProt accession found for gene '{gene_name}'.")
            return (gene_name, None)

    except requests.exceptions.HTTPError as http_err:
        tqdm.write(f"HTTP error for gene '{gene_name}': {http_err}")
        return (gene_name, None)
    except Exception as err:
        tqdm.write(f"Error for gene '{gene_name}': {err}")
        return (gene_name, None)
    
