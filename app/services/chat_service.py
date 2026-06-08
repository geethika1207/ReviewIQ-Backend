import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.getenv("API_KEY"))


def get_prompt(code, reviews_bugs, question):
    prompt = f"""
You are a code review assistant. A user has submitted code and received an AI-generated review with bugs and suggestions. 
The user is now asking a follow-up question about their code or the review. Answer the user's question clearly and concisely based only on the provided code and review context. 
Do not re-review the code from scratch.

Code :
{code}

Reviews and bugs :
{reviews_bugs}

Question : {question}

Answer : your answer here

"""
    return prompt

def ask_groq(prompt: str) -> str:
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    raw = response.choices[0].message.content
    return raw    # returns string directly