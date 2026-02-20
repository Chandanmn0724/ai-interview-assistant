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

def evaluate_answer(question: str, answer: str):

    prompt = f"""
You are a technical interview evaluator.

Evaluate the following:

Question:
{question}

Candidate Answer:
{answer}

Provide:
1. Score out of 10
2. Strengths
3. Areas for improvement
4. Final feedback summary

Be constructive and professional.
"""

    completion = client.chat.completions.create(
        model="deepseek-ai/deepseek-v3.2",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.5,
        max_tokens=500
    )

    return completion.choices[0].message.content