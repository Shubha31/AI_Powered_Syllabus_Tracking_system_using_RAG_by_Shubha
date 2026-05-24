from google import genai
from google.genai import types

from src.config import EMBEDDING_MODEL, GEMINI_API_KEY


client = genai.Client(api_key=GEMINI_API_KEY)


def create_embedding(text):
    response = client.models.embed_content(
        model=EMBEDDING_MODEL,
        contents=text,
        config=types.EmbedContentConfig(
            task_type="RETRIEVAL_QUERY"
        ),
    )
    return response.embeddings[0].values


def create_embeddings(texts):
    embeddings = []

    for text in texts:
        response = client.models.embed_content(
            model=EMBEDDING_MODEL,
            contents=text,
            config=types.EmbedContentConfig(
                task_type="RETRIEVAL_DOCUMENT"
            ),
        )
        embeddings.append(response.embeddings[0].values)

    return embeddings


# from google import genai
# from google.genai import types

# from src.config import EMBEDDING_MODEL, GEMINI_API_KEY


# def get_client():
#     return genai.Client(api_key=GEMINI_API_KEY)


# def create_embedding(text):
#     response = get_client().models.embed_content(
#         model=EMBEDDING_MODEL,
#         contents=text,
#         config=types.EmbedContentConfig(
#             task_type="RETRIEVAL_QUERY"
#         ),
#     )
#     return response.embeddings[0].values


# def create_embeddings(texts):
#     response = get_client().models.embed_content(
#         model=EMBEDDING_MODEL,
#         contents=texts,
#         config=types.EmbedContentConfig(
#             task_type="RETRIEVAL_DOCUMENT"
#         ),
#     )
#     return [embedding.values for embedding in response.embeddings]


# #Openai-text
# #from openai import OpenAI

# #from src.config import EMBEDDING_MODEL


# #client = OpenAI()


# # def create_embedding(text):
# #     response = client.embeddings.create(
# #         model=EMBEDDING_MODEL,
# #         input=text,
# #     )
# #     return response.data[0].embedding


# # def create_embeddings(texts):
# #     response = client.embeddings.create(
# #         model=EMBEDDING_MODEL,
# #         input=texts,
# #     )
# #     return [item.embedding for item in response.data]