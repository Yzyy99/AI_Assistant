import os
import re
import openai
from openai import OpenAI

client = OpenAI(
  api_key="sk-xxx",
  base_url = "http://localhost:8080/v1"
)

def generate_text(prompt):
    """
    TODO
    """
    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        stream=True,

    )
    return response

def generate_answer(current_file_text: str, content: str):
    """
    TODO
    """
    question = f"Answer the questions {content} based on these {current_file_text}?"
    return question


def generate_summary(current_file_text: str):
    """
    TODO
    """
    summary_prompt = f"Summarize the following text: \"{current_file_text}"
    return summary_prompt


if __name__ == "__main__":
    prompt = generate_answer("Hello", "Who is Sun Wukong?")
    generate_text(prompt)