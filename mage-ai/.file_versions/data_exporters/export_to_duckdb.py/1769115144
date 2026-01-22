import duckdb
import os

@data_exporter
def export_data(df, *args, **kwargs):
    # 1. Path mapping: /home/src/ maps to your Mac project root
    db_path = '/home/src/data/processed/knowledge_base.duckdb'
    
    # Ensure directory exists
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    
    # 2. Connect to DuckDB
    # This creates the .duckdb file if it doesn't exist
    connection = duckdb.connect(db_path)
    
    # 3. Create the table and load the Dataframe
    # We use 'vector_store' as our primary table name
    connection.execute("CREATE TABLE IF NOT EXISTS vector_store AS SELECT * FROM df")
    
    # 4. Professional Verification
    res = connection.execute("SELECT COUNT(*) FROM vector_store").fetchone()
    print(f"✅ Successfully exported {len(df)} chunks.")
    print(f"📊 Total records in DuckDB: {res[0]}")

    connection.close()