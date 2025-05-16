from fastapi import FastAPI
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer
import faiss
import pickle
import os
from dotenv import load_dotenv
import google.generativeai as genai
from fastapi.middleware.cors import CORSMiddleware

# Load environment variables
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Configure Gemini (2.0 Flash if available)
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")  # Replace with "gemini-2.0-flash" if available in SDK

# Initialize FastAPI
app = FastAPI()

# CORS for frontend connection (e.g., from localhost:5173)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can replace "*" with ["http://localhost:5173"] for safety
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load FAISS index and metadata
index = faiss.read_index("faiss_index.index")
with open("index_metadata.pkl", "rb") as f:
    metadata = pickle.load(f)

# Load sentence transformer for semantic search
embed_model = SentenceTransformer("all-MiniLM-L6-v2")

# Input schema
class Query(BaseModel):
    question: str

# Main chatbot route
@app.post("/ask")
async def ask(query: Query):
    user_input = query.question

    # Encode the query and search FAISS index
    vector = embed_model.encode([user_input])
    D, I = index.search(vector, k=3)

    # Get top matching articles from metadata
    top_matches = [metadata[i] for i in I[0]]
    context = "\n\n".join(
        f"{m['article_number']} - {m['title']}:\n{m['content']}" for m in top_matches
    )

    # Gemini Prompt
    prompt = f"""
You are a legal assistant designed to answer only questions related to the **Indian Constitution** and **legal rights**.

Your tasks:
1. If the user asks about constitutional articles, fundamental rights, or describes a real-life situation involving legal protections — give a helpful, empathetic, and accurate answer based on the context provided.
2. If the user's question is outside your scope (e.g., unrelated topics like tech, cooking, finance, or politics), reply:  
   *"I’m designed to answer only questions related to the Indian Constitution and legal rights. Please consult a general chatbot or expert for other topics."*

Use the following context from the Constitution to guide your answer:

{context}

User's Question:
{user_input}
"""

    try:
        # Generate answer using Gemini model and prompt
        response = model.generate_content(prompt)
        answer = response.text
    except Exception as e:
        return {"error": str(e)}

    return {
        "answer": answer,
        "article_number": top_matches[0]["article_number"],
        "article_title": top_matches[0]["title"],
        "source": top_matches[0]["content"]
    }
