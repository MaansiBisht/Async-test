# Website Content Search Application

This application allows users to search for specific content within a webpage by entering the URL and a search query. It splits the webpage content into manageable chunks and performs a semantic search to find the most relevant results.

## Features

### Frontend
- **Framework**: Next.js
- **Key Features**:
  - A form with two input fields:
    1. **Website URL**: Text input for the target URL.
    2. **Search Query**: Text input for the query string.
  - A submit button to trigger the search.
  - Display the top 10 matches in a structured format, such as a card or table layout.
  - Each result displays:
    - HTML content chunks (up to 500 tokens each).
    - Relevance score for the match.

### Backend
- **Framework**: FastAPI
- **Key Functionalities**:
  - Fetch HTML content from the provided URL (JavaScript rendering is not required).
  - Tokenize the HTML content and split it into chunks of up to 500 tokens each.
  - Perform a semantic search for the query string across these chunks.
  - Return the top 10 matching chunks based on relevance.

### Vector Database
- **Database Used**: Pinecone
- **Purpose**:
  - Index HTML chunks for efficient retrieval.
  - Perform semantic searches to find the most relevant matches for the user query.

## Installation and Setup

### Prerequisites
- **Frontend**:
  - Next.js
  - Node.js (version 16 or above recommended)
  - npm or yarn
- **Backend**:
  - Python 3.9 or above
  - pip
- **Database**:
  - Pinecone account and API key

### Steps

#### Clone the Repository
```bash
git clone https://github.com/your-repo/website-content-search.git
cd aync-app-frontend
npm install
npm start
```

#### Setting up backend
```bash
    python3 -m venv venv
    pip3 install -r requirements.txt
```

#### Setting up Pinecone Account and API Key

Pinecone is used as the vector database to index and search the HTML content. To integrate Pinecone with your application, follow the steps below:

##### 1. Create a Pinecone Account
1. Go to the [Pinecone website](https://www.pinecone.io/) and sign up for an account if you don't already have one.
2. Once you've signed up and logged in, navigate to the Pinecone dashboard.

##### 2. Generate an API Key
1. In the Pinecone dashboard, go to the **API Keys** section (found under your account settings).
2. Click on the **Create New API Key** button.
3. Copy the generated API key; you'll need it to integrate Pinecone with your backend in Search.py file.

##### 3. Set up Pinecone in the Backend

In your backend, you'll need to use the Pinecone API key to connect to Pinecone services. Follow these steps:

###### Install the Pinecone Python Client
If you haven't installed the Pinecone client yet, install it by running the following command in your backend directory:

```bash
pip install pinecone-client
```
### Running backend
```bash
uvicorn main:app --reload
```



