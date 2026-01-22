import os
import PyPDF2

@data_loader
def load_data_from_directory(*args, **kwargs):
    data_path = '/home/src/data/raw'
    docs = []

    if not os.path.exists(data_path):
        return []

    for filename in os.listdir(data_path):
        if filename.endswith('.pdf'):
            filepath = os.path.join(data_path, filename)
            try:
                with open(filepath, 'rb') as f:
                    reader = PyPDF2.PdfReader(f)
                    full_text = ""
                    for page in reader.pages:
                        extracted = page.extract_text()
                        if extracted:
                            full_text += extracted
                    
                    # CRITICAL: Ensure we are sending the actual variables
                    docs.append({
                        'filename': str(filename),
                        'text': str(full_text)
                    })
            except Exception as e:
                print(f"Error reading {filename}: {e}")
    
    return docs