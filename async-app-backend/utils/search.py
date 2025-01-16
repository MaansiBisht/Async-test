from typing import List
from pinecone import Pinecone, ServerlessSpec
import torch
from transformers import AutoTokenizer, AutoModel
import os , sys

# Initialize transformers tokenizer and model (e.g., for BERT embeddings)
tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
model = AutoModel.from_pretrained("bert-base-uncased")

# Pinecone initialization
pc = Pinecone(api_key="YOUR_API_KEY",environment="us-west1-gcp")
index_name = "html-index"

# Check if the index exists and initialize it
if index_name not in pc.list_indexes().names():
    print(f"Creating index: {index_name}")
    pc.create_index(index_name, dimension=768, metric="cosine", 
    spec=ServerlessSpec(
        cloud="aws",
        region="us-east-1"
    ))
index = pc.Index(index_name)

# Function to convert text to embeddings (using BERT)
def text_to_embedding(text: str):
    inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True)
    with torch.no_grad():
        embeddings = model(**inputs).last_hidden_state.mean(dim=1).squeeze().cpu().numpy()
    return embeddings.tolist()

# Function to index chunks into Pinecone (along with HTML content as metadata)
def index_chunks(chunks: List[dict], url_path:str):
    vectors = []
    for chunk in chunks:
        embedding = text_to_embedding(chunk["text"]) 
        chunk_id = str(hash(chunk["text"]))

        # Store both chunk text and HTML in the metadata
        vectors.append((
            chunk_id, 
            embedding, 
            {"content": chunk["text"], "html": chunk["html"], "url": url_path}
        ))

    if vectors:
        index.upsert(vectors)

def search_chunks(query: str, url_path:str ,top_k=10):
    try:
        # Convert query to embedding
        query_embedding = text_to_embedding(query)
        
        # Perform the semantic search using Pinecone
        query_result = index.query(
            vector=query_embedding,
            top_k=top_k,
            include_metadata=True  # Retrieve metadata including HTML content
        )

        results = []
        for match in query_result['matches']:
            if match.metadata.get('url') == url_path:
                match_percentage = round(match.score * 100, 2) 
                results.append({
                    "chunk_id": match.id,
                    "score": match_percentage,  # Percentage score
                    "content": match.metadata.get('content', ""),  # Chunk text
                    "html": match.metadata.get('html', ""),  # HTML content
                    "match_percentage": f"{match_percentage:.2f}%",
                    "path": match.metadata.get('url', "")  
                })

        return results


    except Exception as e:
        exc_type, exc_value, exc_tb = sys.exc_info()
        line_number = exc_tb.tb_lineno
        print(f"Error at line {line_number}: {e}")
