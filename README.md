# Protein-3D-Structure-Pipeline-Web-Interface

## Overview
This project consists of a comprehensive data pipeline for protein structure data collection and a web interface for visualization. The system processes gene names to retrieve their corresponding PDB files and provides an interactive interface for protein structure exploration using Mol* viewer.

## Project Structure

### Data Pipeline (`/data`)
The pipeline performs the following sequential operations:
1. Gene name collection and processing
2. UniProt ID extraction
3. URL generation and validation
4. PDB file download and storage
5. SQLite database creation (`.db`) for metadata storage
6. uploadtoGCS.py to upload pdb files into Google Cloud Storage

**Note:** Not all gene names in the input set have available 3D structural models. Currently, the system has successfully processed approximately 17,300 PDB files.

### Web Server (`/web_server`)
The web interface provides:
- Search functionality for protein genes
- Integration with Mol* viewer for 3D structure visualization
- Detailed gene descriptions and metadata display
- Deployed on Google Cloud Run

## Storage
- PDB files are stored in Google Cloud Storage for efficient access and scalability
- Metadata and relationships are managed through SQLite database

## Usage
The entire data pipeline can be executed through the provided Jupyter notebook (`.ipynb`). The notebook orchestrates all pipeline steps sequentially, ensuring proper data processing and storage.

### Prerequisites
- Python 3.x
- Jupyter Notebook
- Google Cloud Storage access credentials
- Required Python packages (requirements.txt)

### Running the Pipeline
1. Configure your Google Cloud credentials
2. Open the Jupyter notebook
3. Execute all cells sequentially
4. Monitor the pipeline progress through provided logging

### Accessing the Web Interface
Web can be access via (https://projectwikicrow-2-ckpruviikq-uc.a.run.app/)
Detailed chosen gene is on the bottom of the page

## Limitations
- Not all gene names have corresponding 3D structural models available
- Total PDB files processed: ~17,300
