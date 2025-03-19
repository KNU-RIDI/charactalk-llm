import os
from langchain_google_vertexai import VertexAI

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "./gcp-key.json"

llm = VertexAI(
    model_name="gemini-2.0-flash-lite",
    temperature=0.7,
    max_output_tokens=256
)