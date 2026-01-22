from sentence_transformers import SentenceTransformer
import pandas as pd

@transformer
def transform(data, *args, **kwargs):
    model = SentenceTransformer('all-MiniLM-L6-v2')
    chunked_data = []
    
    # 1. Ensure 'data' is a list so we can iterate
    if not isinstance(data, list):
        data = [data]

    for doc in data:
        # 2. Check if the item is a dictionary (what we expect)
        if isinstance(doc, dict):
            text = doc.get('text', '')
            source_name = doc.get('filename', 'unknown_source')
        else:
            # 3. If it's a string, we treat the whole string as text
            # This prevents the 'AttributeError'
            text = str(doc)
            source_name = 'unknown_source'

        # Skip empty strings
        if not text or len(text.strip()) == 0:
            continue

        # 4. Chunking (500 chars)
        chunks = [text[i:i+500] for i in range(0, len(text), 500)]
        
        for i, chunk in enumerate(chunks):
            # 5. Embedding math
            embedding = model.encode(chunk).tolist()
            
            chunked_data.append({
                'document_id': source_name,
                'chunk_id': f"{source_name}_{i}",
                'content': chunk,
                'vector': embedding
            })
    
    return pd.DataFrame(chunked_data)