 #AI Syllabus Tracker

A beginner-friendly LLM project that uses RAG to answer questions from uploaded school syllabus files and SQLite to track study progress.

## What This Project Does

- Upload syllabus files: PDF, DOCX, XLSX, CSV, TXT, MD
- Extract text from the file
- Split text into chunks
- Create embeddings with `text-embedding-3-small`
- Store chunks in ChromaDB
- Ask questions using a RAG pipeline
- Track syllabus progress in SQLite
- Generate study plans with an OpenAI LLM

## Architecture

```text
File upload
-> text extraction
-> chunking
-> embeddings
-> ChromaDB vector storage
-> question embedding
-> retrieve similar chunks
-> OpenAI LLM answer
-> Streamlit UI
```

SQLite is used for structured progress tracking:

```text
subject, chapter, topic, status, deadline, priority, notes
```

ChromaDB is used for AI search:

```text
syllabus chunks + embedding vectors + file metadata
```

## Folder Structure

```text
ai-syllabus-tracker/
  app.py
  requirements.txt
  .env.example
  README.md
  data/
    uploads/
    chroma/
  samples/
  src/
    chunker.py
    config.py
    database.py
    embedder.py
    file_loader.py
    prompts.py
    rag_pipeline.py
    vector_store.py
```
## STEP BY STEP GUIDANCE TO BUILD THIS PROJECT:
# 1 First open a fresh folder, 
# 2 Create project folder
# 3 under project create ai_syllabus_tracker folder
# 4 open it in any code editor platform (I have used VS Code here)
# 5 install all libraries first here main we are using python so install python libraries 

## Setup

Create a virtual environment:

```bash
python -m venv venv
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt

#install every requirements without fail
```

Create a `.env` file by copying `.env.example`:

```text
OPENAI_API_KEY=your_openai_api_key_here
LLM_MODEL=gpt-5.5
EMBEDDING_MODEL=text-embedding-3-small
CHROMA_PATH=data/chroma
SQLITE_DB_PATH=data/syllabus_tracker.db

Sometimes whithout free tier the API may not work so use other relevent API Platforms
```
# If you have OpenAi subscription use it else i have used gemini ai studio api keys here
GEMINI_API_KEY=your_gemini_api_key - paste the key here that you generated
LLM_MODEL=gemini-2.5-flash
EMBEDDING_MODEL=gemini-embedding-001
CHROMA_PATH=data/chroma
SQLITE_DB_PATH=data/syllabus_tracker.db
``` 
Run the app:

```bash
streamlit run app.py
```

## How SQLite Is Built

The SQLite database is created automatically at:

```text
data/syllabus_tracker.db
```

The table is created in `src/database.py`:

```sql
CREATE TABLE IF NOT EXISTS topics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    subject TEXT NOT NULL,
    chapter TEXT NOT NULL,
    topic TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'Not Started',
    deadline TEXT,
    priority TEXT,
    notes TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);
```

You do not need to manually create the database. When the app starts, `init_db()` creates it.

## Example Upload Files

Use these samples: (these are external files create from word, excel, pdf and upload when the code is executed)

- `samples/science_syllabus.txt`
- `samples/math_syllabus.csv`
- `samples/word_file_content_example.md`
- `samples/excel_file_content_example.md`

For Word files, paste the example content into Word or Google Docs and export as `.docx`.

For Excel files, create the columns shown in the example and save as `.xlsx`.

## RAG Process

1. User uploads a syllabus file.
2. `file_loader.py` extracts text.
3. `chunker.py` splits text into chunks of about 700 tokens with 120 token overlap.
4. `embedder.py` creates embeddings using `text-embedding-3-small`.
5. `vector_store.py` stores chunks in ChromaDB.
6. User asks a question.
7. The question is embedded.
8. Similar chunks are retrieved from ChromaDB.
9. The retrieved chunks are sent to the LLM.
10. The LLM answers using only the syllabus context.

## Good Questions To Test

```text
What chapters are included in Science?
Explain Life Processes in simple words.
Create a 7-day plan for my Science exam.
Which topics are high priority?
What should I revise before the unit test?


```

## Beginner Presentation Line

This project uses Retrieval-Augmented Generation. Uploaded syllabus files are parsed, cleaned, chunked, embedded using `text-embedding-3-small`, stored in ChromaDB, retrieved based on the user's question, and passed to an OpenAI LLM to generate grounded answers and study plans. SQLite stores the student's progress data separately.