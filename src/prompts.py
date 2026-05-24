SYSTEM_PROMPT = """
You are an AI syllabus assistant for school students.
Use only the provided syllabus context and progress data.
If the answer is not available in the context, say that the uploaded syllabus does not contain enough information.
Explain in simple language.
Be practical and organized.
"""


def build_rag_prompt(question, context, progress_summary=""):
    return f"""
Syllabus context:
{context}

Progress data:
{progress_summary}

Student question:
{question}

Answer:
"""


def build_study_plan_prompt(goal, days, context, progress_summary):
    return f"""
Create a {days}-day study plan for this goal:
{goal}

Use this syllabus context:
{context}

Use this progress data:
{progress_summary}

Rules:
- Prefer pending and in-progress topics.
- Keep the plan realistic for school students.
- Include revision and practice.
- Mention which syllabus parts were used.
"""