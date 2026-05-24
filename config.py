import os

from dotenv import load_dotenv


load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
LLM_MODEL = os.getenv("LLM_MODEL", "gemini-2.5-flash")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "gemini-embedding-001")
CHROMA_PATH = os.getenv("CHROMA_PATH", "data/chroma")
SQLITE_DB_PATH = os.getenv("SQLITE_DB_PATH", "data/syllabus_tracker.db")
COLLECTION_NAME = "syllabus_chunks"


#OpenAI-Text
#import os

#from dotenv import load_dotenv


#load_dotenv()

#LLM_MODEL = os.getenv("LLM_MODEL", "gpt-5.5")
#EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")
#CHROMA_PATH = os.getenv("CHROMA_PATH", "data/chroma")
#SQLITE_DB_PATH = os.getenv("SQLITE_DB_PATH", "data/syllabus_tracker.db")
#COLLECTION_NAME = "syllabus_chunks"