# 🤖 RAG Chatbot - "Chat with your files"

A full-stack AI system that allows users to upload documents and images, store them securely, and interact with an AI assistant. The chatbot answers questions **grounded strictly** in the user's uploaded content using **Retrieval Augmented Generation (RAG)**.


---

## ✨ Features

### 🔐 Authentication
* **Token-based Auth**: Secure email/password login via Django REST Framework.
* **Data Isolation**: Strict per-user isolation—users can only access and query their own files and chat history.

### 📂 File & Image Upload
* **Supported Formats**: PDF, TXT, DOCX, PNG, JPG, JPEG.
* **Storage**: Files are securely stored in **MinIO** (S3-compatible object storage).
* **Management**: View file metadata (size, type, timestamp) and delete assets (automatically removing their embeddings).

### 🧠 RAG Pipeline (The Brain)
| Step | Description |
| :--- | :--- |
| **Extraction** | Text is parsed from PDF, DOCX, TXT, and Images (OCR). |
| **Chunking** | Documents are split into overlapping segments for better context. |
| **Embedding** | Uses `sentence-transformers/all-MiniLM-L6-v2`. |
| **Vector Store** | **FAISS** (Facebook AI Similarity Search) for fast retrieval. |
| **Retrieval** | Top-K similarity search finds relevant chunks. |
| **Generation** | **Google Gemini** LLM generates answers strictly from retrieved context. |

### 💬 Chat Interface
* Ask questions across *all* uploaded assets simultaneously.
* **Grounded Answers**: The AI cites sources when content exists.
* **Anti-Hallucination**: Gracefully declines to answer if the information is not found in your files.

---

## 🏗 Tech Stack

| Layer | Technology |
| :--- | :--- |
| **Frontend** | React + TypeScript |
| **Backend** | Django + Django REST Framework |
| **Auth** | DRF Token Authentication |
| **Vector DB** | FAISS |
| **Embeddings** | Sentence-Transformers |
| **LLM** | Google Gemini (Free Tier Friendly) |
| **Storage** | MinIO (Docker) |

---

## 📁 Project Structure

```bash
backend/
 ├─ accounts/        # Auth serializers & views
 ├─ assets/          # Upload / delete / metadata logic
 ├─ rag/             # Chunking, embeddings, FAISS indexing
 ├─ chat/            # Chat API + LLM grounding logic
 ├─ data/faiss/      # User-isolated Vector index files
 └─ manage.py

frontend/
 ├─ pages/           # Login, Register, Chat views
 ├─ api/             # Axios client configuration
 ├─ context/         # AuthContext provider
 └─ styles/          # CSS/Tailwind styles
# ⚙️ Setup Instructions
```
Follow these steps to get the RAG Chatbot running locally.

Backend Setup
```bash
cd backend

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Start server
python manage.py runserver
```
MinIO Setup (Object Storage)
Run MinIO using Docker:

```Bash
docker compose up -d
```

Frontend Setup
```Bash
cd frontend
npm install
npm run dev
```
