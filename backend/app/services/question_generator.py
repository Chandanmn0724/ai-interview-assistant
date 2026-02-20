from dotenv import load_dotenv
from openai import OpenAI
import os

load_dotenv()

api_key = os.getenv("NVIDIA_API_KEY")

if not api_key:
    raise ValueError("NVIDIA_API_KEY not found in .env file")

client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=api_key
)

def generate_questions(role: str, difficulty: str):

    prompt = f"""
Generate 5 {difficulty} level technical interview questions for a {role}.

Do NOT include answers.
Keep them clear and professional.
"""

    completion = client.chat.completions.create(
        model="deepseek-ai/deepseek-v3.2",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=600
    )

    return completion.choices[0].message.content