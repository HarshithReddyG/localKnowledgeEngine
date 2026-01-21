FROM mageai/mageai:latest

WORKDIR /home/src

# Install PDF and ML libraries
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Pre-cache the model for M1
RUN python3 -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('all-MiniLM-L6-v2')"
