from nltk.tokenize import word_tokenize
from bs4 import BeautifulSoup

def tokenize_html(content: str, chunk_size: int = 500) -> list[str]:    
    soup = BeautifulSoup(content, "html.parser")
    visible_text = soup.get_text(separator=" ", strip=True)

    # Tokenize text
    words = word_tokenize(visible_text)

    # Chunk text and associate corresponding HTML
    chunks = []
    for i in range(0, len(words), chunk_size):
        chunk_text = " ".join(words[i:i + chunk_size])
        chunk_html = soup.prettify()[i:i + chunk_size]  # Adjust slicing logic if needed
        chunks.append({
            "text": chunk_text,
            "html": chunk_html
        })
    return chunks
   
