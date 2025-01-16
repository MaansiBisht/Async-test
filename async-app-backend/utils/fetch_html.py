import httpx
from bs4 import BeautifulSoup

async def fetch_html_content(url: str) -> dict:
    async with httpx.AsyncClient() as client:
        print(f"Fetching URL: {url}")
        try:
            response = await client.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")

            # Clean HTML by removing unnecessary tags (e.g., <script>, <style>)
            for tag in soup(["script", "style"]):
                tag.decompose()

            # Get cleaned HTML content
            cleaned_html_content = str(soup)

            # Extract plain text from the cleaned HTML
            plain_text_content = soup.get_text()

            # Return both HTML and text content
            return {
                "html": cleaned_html_content,
                "text": plain_text_content
            }
        except httpx.RequestError as e:
            print(f"Error during request: {e}")
            return {"error": f"Request failed: {str(e)}"}

        except Exception as e:
            print(f"An error occurred: {e}")
            return {"error": f"An error occurred: {str(e)}"}
