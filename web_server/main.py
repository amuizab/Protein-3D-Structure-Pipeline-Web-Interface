from flask import Flask, send_from_directory, jsonify, request
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('genes.db')  # Changed to your db filename
    conn.row_factory = sqlite3.Row
    return conn

def get_table_name():
    conn = get_db_connection()
    cur = conn.cursor()
    
    # Get list of tables in the database
    cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cur.fetchall()
    
    print("Available tables:", tables)  # This will show tables in console
    conn.close()
    return tables

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/check_tables')
def check_tables():
    tables = get_table_name()
    print(tables)
    return jsonify({'tables': [table[0] for table in tables]})

@app.route('/search_proteins')
def search_proteins():
    query = request.args.get('query', '').lower()
    
    if not query:
        return jsonify([])
    
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        # First, let's get the actual table name
        cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cur.fetchall()
        table_name = tables[0][0]  # Get the first table name
        
        # Search for partial matches in gene_names using the correct table
        search_query = f"%{query}%"
        cur.execute(f"""
            SELECT gene_name, uniprot_id, description, pdb_file 
            FROM {table_name} 
            WHERE LOWER(gene_name) LIKE ?
        """, (search_query,))
        
        # Fetch all matching rows
        rows = cur.fetchall()
        
        # Convert rows to list of dictionaries
        results = []
        for row in rows:
            results.append({
                'gene_name': row['gene_name'],
                'uniprot_id': row['uniprot_id'],
                'code': row['uniprot_id'],
                'description': row['description']
            })
        
        conn.close()
        return jsonify(results)
        
    except Exception as e:
        print(f"Error searching proteins: {e}")
        return jsonify([])

if __name__ == '__main__':
    app.run(debug=True)