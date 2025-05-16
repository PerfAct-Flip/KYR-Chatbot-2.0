# KYR Chatbot 2.0

A conversational AI assistant that answers questions about the **Indian Constitution** and **legal rights** using semantic search and Google Gemini LLM. Built with FastAPI (Python backend), FAISS for vector search, and a React + Vite frontend.

---

## Features

- **Semantic Search:** Uses [FAISS](https://github.com/facebookresearch/faiss) and [sentence-transformers](https://www.sbert.net/) to find relevant constitutional articles.
- **LLM-Powered Answers:** Integrates Google Gemini to generate empathetic, accurate responses.
- **Legal Domain Focus:** Only answers questions related to the Indian Constitution and legal rights.
- **Modern Frontend:** React + TypeScript + Vite with Tailwind CSS.

---

## Project Structure

```
.
├── chatbot_api.py           # FastAPI backend with Gemini integration
├── build_faiss_index.py     # Script to build FAISS index from data
├── flatten_constitution.py  # Script to preprocess constitution data
├── COI.json                 # Raw constitution data
├── faiss_index.index        # FAISS index file
├── index_metadata.pkl       # Metadata for indexed articles
├── flattened_constitution.jsonl # Preprocessed data
├── .env                     # API keys and environment variables
├── frontend/                # React + Vite frontend
└── requirements.txt         # Python dependencies
```

---

## Setup

### 1. Backend (Python/FastAPI)

#### Prerequisites

- Python 3.10+
- [Google Gemini API access](https://ai.google.dev/)
- [FAISS](https://github.com/facebookresearch/faiss)

#### Installation

```sh
python -m venv chatbot-env
source chatbot-env/bin/activate  # or Scripts\activate on Windows
pip install -r requirements.txt
```

#### Environment Variables

Create a `.env` file in the root directory:

```
GEMINI_API_KEY="your-gemini-api-key"
```

#### Build the FAISS Index

If not already present, run:

```sh
python build_faiss_index.py
```

#### Start the API

```sh
uvicorn chatbot_api:app --reload
```

---

### 2. Frontend (React + Vite)

#### Prerequisites

- Node.js 18+

#### Installation

```sh
cd frontend
npm install
```

#### Development Server

```sh
npm run dev
```

The frontend will be available at [http://localhost:5173](http://localhost:5173).

---

## Usage

- Ask questions about the Indian Constitution or legal rights in the frontend UI.
- The backend will retrieve relevant articles and generate an answer using Gemini.

---

## License

MIT

---

## Acknowledgements

- [FAISS](https://github.com/facebookresearch/faiss)
- [sentence-transformers](https://www.sbert.net/)
- [Google Gemini](https://ai.google.dev/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [React](https://react.dev/)
