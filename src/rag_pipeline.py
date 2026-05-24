from pathlib import Path

from google import genai
#from openai import OpenAI

from src.chunker import chunk_text
from src.config import GEMINI_API_KEY, LLM_MODEL
#from src.config import LLM_MODEL
from src.database import list_topics
from src.embedder import create_embedding, create_embeddings
from src.file_loader import extract_text
from src.prompts import SYSTEM_PROMPT, build_rag_prompt, build_study_plan_prompt
from src.vector_store import add_chunks, search_chunks


#client = OpenAI()
# def get_client():
#     return genai.Client(api_key=GEMINI_API_KEY)
client = genai.Client(api_key=GEMINI_API_KEY)


def ingest_document(file_path, subject="Unknown", grade="Unknown"):
    text = extract_text(file_path)
    chunks = chunk_text(text)
    embeddings = create_embeddings(chunks)

    add_chunks(
        chunks=chunks,
        embeddings=embeddings,
        metadata={
            "file_name": Path(file_path).name,
            "subject": subject,
            "grade": grade,
        },
    )

    return {"chunks": len(chunks)}


def answer_question(question):
    query_embedding = create_embedding(question)
    matches = search_chunks(query_embedding, top_k=5)
    context = format_matches(matches)
    progress_summary = format_progress()

    prompt = build_rag_prompt(
        question=question,
        context=context,
        progress_summary=progress_summary,
    )

    # response = client.responses.create(
    #     model=LLM_MODEL,
    #     instructions=SYSTEM_PROMPT,
    #     input=prompt,
    # )

    # return {
    #     "answer": response.output_text,
    
    #response = get_client().models.generate_content(
    response = client.models.generate_content(
    model=LLM_MODEL,
    contents=f"{SYSTEM_PROMPT}\n\n{prompt}",
)

    return {
    "answer": response.text,
        "sources": [
            {
                "text": match["text"],
                "score": match["score"],
                "file_name": match["metadata"].get("file_name", "Unknown"),
                "subject": match["metadata"].get("subject", "Unknown"),
            }
            for match in matches
        ],
    }


def make_study_plan(goal, days):
    query = f"Study plan for: {goal}"
    query_embedding = create_embedding(query)
    matches = search_chunks(query_embedding, top_k=8)

    prompt = build_study_plan_prompt(
        goal=goal,
        days=days,
        context=format_matches(matches),
        progress_summary=format_progress(),
    )

    # response = client.responses.create(
    #     model=LLM_MODEL,
    #     instructions=SYSTEM_PROMPT,
    #     input=prompt,
    # )
    # return response.output_text
    #response = get_client().models.generate_content(
    response = client.models.generate_content(
    model=LLM_MODEL,
    contents=f"{SYSTEM_PROMPT}\n\n{prompt}",
)
    return response.text


def format_matches(matches):
    if not matches:
        return "No syllabus chunks found."

    parts = []
    for index, match in enumerate(matches, start=1):
        metadata = match["metadata"]
        parts.append(
            f"""
[Source {index}]
File: {metadata.get("file_name", "Unknown")}
Subject: {metadata.get("subject", "Unknown")}
Grade: {metadata.get("grade", "Unknown")}
Text:
{match["text"]}
"""
        )
    return "\n".join(parts)


def format_progress():
    topics = list_topics()
    if not topics:
        return "No progress topics have been added yet."

    lines = []
    for topic in topics:
        lines.append(
            f"- {topic['subject']} | {topic['chapter']} | {topic['topic']} | "
            f"Status: {topic['status']} | Deadline: {topic['deadline']} | Priority: {topic['priority']}"
        )
    return "\n".join(lines)