from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from utils.fetch_html import fetch_html_content
from utils.tokenize import tokenize_html
from utils.search import search_chunks , index_chunks
from fastapi.middleware.cors import CORSMiddleware
import traceback ,sys

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can specify allowed origins here
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)
class SearchRequest(BaseModel):
    url: str
    query: str

@app.get("/")
def read_root():
    return {"message": "Welcome to Website Content Search API"}

@app.post("/search/")
async def search_website(request: SearchRequest):
    try:
        #Fetch HTML content
        html_content = await fetch_html_content(request.url)

        # Tokenize into chunks of 500 tokens
        chunks = tokenize_html(html_content.get('html'))

         # Step 3: Index the chunks into Pinecone (only once, then reuse)
        index_chunks(chunks, url_path=request.url)
    
        # Step 4: Perform a semantic search using the query
        search_results = search_chunks(request.query,url_path=request.url)
    
        return {"url": request.url, "query": request.query, "results": search_results}

    except Exception as e:
        exc_type, exc_value, exc_tb = sys.exc_info()
        line_number = exc_tb.tb_lineno
        print(f"Error at line :{line_number} {e}")
        raise HTTPException(status_code=500, detail=str(e))
