import os
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv

from src.database import (
    add_topic,
    get_dashboard_stats,
    init_db,
    list_topics,
    update_topic_status,
)
from src.file_loader import extract_text
from src.rag_pipeline import answer_question, ingest_document, make_study_plan


load_dotenv()

UPLOAD_DIR = Path("data/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


st.set_page_config(page_title="AI Syllabus Tracker", page_icon="📘", layout="wide")
init_db()

st.title("AI Syllabus Tracker")
st.caption("Upload syllabus files, ask AI questions, and track study progress with SQLite.")

with st.sidebar:
    st.header("Navigation")
    page = st.radio(
        "Choose a page",
        [
            "Dashboard",
            "Upload Syllabus",
            "Ask AI",
            "Study Plan",
            "Track Progress",
            "How SQLite Works",
        ],
    )


# def require_api_key():
#     if not os.getenv("OPENAI_API_KEY"):
#         st.warning("Add your OpenAI API key to a .env file before using AI features.")
#         st.code("OPENAI_API_KEY=your_api_key_here", language="text")
#         return False
#     return True
def require_api_key():
    api_key = os.getenv("GEMINI_API_KEY", "")
    if not api_key or api_key == "your_gemini_api_key_here":
        st.warning("Add your Gemini API key to a .env file before using AI features.")
        st.code("GEMINI_API_KEY=your_api_key_here", language="text")
        return False
    return True


if page == "Dashboard":
    stats = get_dashboard_stats()
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Topics", stats["total"])
    c2.metric("Completed", stats["completed"])
    c3.metric("In Progress", stats["in_progress"])
    c4.metric("Not Started", stats["not_started"])

    st.subheader("Topics")
    topics = list_topics()
    if not topics:
        st.info("No topics yet. Add topics on the Track Progress page.")
    else:
        st.dataframe(topics, use_container_width=True, hide_index=True)

elif page == "Upload Syllabus":
    st.subheader("Upload a syllabus file")
    st.write("Supported formats: PDF, DOCX, XLSX, CSV, TXT, MD")

    uploaded_file = st.file_uploader(
        "Choose file",
        type=["pdf", "docx", "xlsx", "csv", "txt", "md"],
    )

    subject = st.text_input("Subject name", placeholder="Example: Science")
    grade = st.text_input("Class/Grade", placeholder="Example: Class 10")

    if uploaded_file and st.button("Process file"):
        if not require_api_key():
            st.stop()

        save_path = UPLOAD_DIR / uploaded_file.name
        save_path.write_bytes(uploaded_file.getbuffer())

        with st.spinner("Extracting text..."):
            text = extract_text(save_path)

        if not text.strip():
            st.error("No readable text found in this file.")
            st.stop()

        with st.spinner("Chunking, embedding, and storing in ChromaDB..."):
            result = ingest_document(
                file_path=save_path,
                subject=subject or "Unknown",
                grade=grade or "Unknown",
            )

        st.success(f"File processed successfully. Stored {result['chunks']} chunks.")
        st.text_area("Preview extracted text", text[:3000], height=260)

elif page == "Ask AI":
    st.subheader("Ask questions from your uploaded syllabus")
    question = st.text_area(
        "Question",
        placeholder="Example: What are the main chapters in Class 10 Science?",
    )

    if st.button("Ask AI"):
        if not require_api_key():
            st.stop()
        if not question.strip():
            st.warning("Please enter a question.")
            st.stop()

        with st.spinner("Searching syllabus chunks and asking the LLM..."):
            result = answer_question(question)

        st.markdown("### Answer")
        st.write(result["answer"])

        st.markdown("### Retrieved Sources")
        for item in result["sources"]:
            with st.expander(f"{item['file_name']} | {item['subject']} | score: {item['score']:.4f}"):
                st.write(item["text"])

elif page == "Study Plan":
    st.subheader("Generate a study plan")
    days = st.number_input("Number of days", min_value=1, max_value=30, value=7)
    goal = st.text_area(
        "Study goal",
        placeholder="Example: Prepare for my Science exam using the pending chapters.",
    )

    if st.button("Generate Plan"):
        if not require_api_key():
            st.stop()
        if not goal.strip():
            st.warning("Please enter a study goal.")
            st.stop()

        with st.spinner("Creating a plan using syllabus data..."):
            plan = make_study_plan(goal=goal, days=int(days))
        st.markdown(plan)

elif page == "Track Progress":
    st.subheader("Add a syllabus topic")
    with st.form("add_topic_form"):
        c1, c2 = st.columns(2)
        subject = c1.text_input("Subject", placeholder="Science")
        chapter = c2.text_input("Chapter", placeholder="Life Processes")
        topic = st.text_input("Topic", placeholder="Nutrition in plants and animals")
        c3, c4 = st.columns(2)
        deadline = c3.date_input("Deadline", value=None)
        priority = c4.selectbox("Priority", ["Low", "Medium", "High"])
        notes = st.text_area("Notes", placeholder="Important diagrams, formulas, etc.")
        submitted = st.form_submit_button("Save Topic")

    if submitted:
        if not subject or not chapter or not topic:
            st.warning("Subject, chapter, and topic are required.")
        else:
            add_topic(
                subject=subject,
                chapter=chapter,
                topic=topic,
                deadline=str(deadline) if deadline else "",
                priority=priority,
                notes=notes,
            )
            st.success("Topic saved in SQLite.")

    st.subheader("Update progress")
    topics = list_topics()
    if topics:
        selected = st.selectbox(
            "Choose a topic",
            topics,
            format_func=lambda row: f"{row['id']} - {row['subject']} / {row['chapter']} / {row['topic']}",
        )
        new_status = st.selectbox("Status", ["Not Started", "In Progress", "Completed"])
        if st.button("Update Status"):
            update_topic_status(selected["id"], new_status)
            st.success("Status updated.")
            st.rerun()

        st.dataframe(topics, use_container_width=True, hide_index=True)
    else:
        st.info("No topics saved yet.")

elif page == "How SQLite Works":
    st.subheader("How SQLite is used in this project")
    st.write(
        "SQLite stores structured progress data: subjects, chapters, topics, deadlines, "
        "priorities, and completion status."
    )
    st.code(
        """
CREATE TABLE topics (
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
        """,
        language="sql",
    )
    st.write(
        "ChromaDB is different. It stores syllabus chunks and embeddings for AI search. "
        "SQLite stores the student's human-readable tracking data."
    )