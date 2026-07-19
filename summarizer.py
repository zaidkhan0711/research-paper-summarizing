import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def chunk_text(text, chunk_size=3000):
    """Split text into smaller chunks."""
    return [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]


def summarize_text(text):
    chunks = chunk_text(text)

    summaries = []

    # Summarize each chunk
    for chunk in chunks:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert research paper summarizer."
                },
                {
                    "role": "user",
                    "content": f"Summarize the following part of a research paper:\n\n{chunk}"
                }
            ],
            max_tokens=200,
        )

        summaries.append(response.choices[0].message.content)

    # If there was only one chunk, return it
    if len(summaries) == 1:
        return summaries[0]

    # Combine all summaries
    combined_summary = "\n\n".join(summaries)

    # Summarize the summaries into one final summary
    final_response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "system",
                "content": "You are an expert research paper summarizer."
            },
            {
                "role": "user",
                "content": f"Create one concise summary from these summaries:\n\n{combined_summary}"
            }
        ],
        max_tokens=300,
    )

    return final_response.choices[0].message.content