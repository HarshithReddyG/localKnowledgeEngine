import duckdb
from sentence_transformers import SentenceTransformer
import requests
import json

@custom
def rag_search(*args, **kwargs):
    # 1. Pull the variable from the Global Variables (kwargs)
    # If the variable isn't found, it defaults to a generic question
    user_query = kwargs.get('user_query', "Summarize the documents")
    
    print(f"🚀 Processing Query: {user_query}")
    
    # 2. Setup paths and models
    db_path = '/home/src/data/processed/knowledge_base.duckdb'
    model = SentenceTransformer('all-MiniLM-L6-v2')
    
    # 3. Convert User Query into a Vector
    query_vector = model.encode(user_query).tolist()
    
    # 4. Connect to DuckDB
    conn = duckdb.connect(db_path)
    
    # Check if the DuckDB 'vss' extension is needed for similarity
    # Note: list_cosine_similarity is built-in for recent DuckDB versions
    search_query = f"""
        SELECT content, document_id, 
               list_cosine_similarity(vector, {query_vector}::FLOAT[]) as similarity
        FROM vector_store
        ORDER BY similarity DESC
        LIMIT 3
    """
    
    results = conn.execute(search_query).df()
    conn.close()
    
    # 5. Context Preparation
    context = "\n".join(results['content'].tolist())
    
    # 6. Send to Ollama (RAG Step)
    ollama_url = "http://host.docker.internal:11434/api/generate"
    
    prompt = f"""
    You are a professional research assistant. Use the following pieces of retrieved context 
    to answer the user's question. If you don't know the answer, say you don't know.
    
    Context: {context}
    Question: {user_query}
    Answer:
    """
    
    try:
        response = requests.post(ollama_url, json={
            "model": "llama3.2:3b",
            "prompt": prompt,
            "stream": False
        }, timeout=30)
        
        answer = response.json().get('response', 'No response from AI.')
    except Exception as e:
        answer = f"Error connecting to Ollama: {str(e)}. Make sure Ollama is running on your Mac!"

    return {
        "answer": answer,
        "sources": results['document_id'].unique().tolist()
    }