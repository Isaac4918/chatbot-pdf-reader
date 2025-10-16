import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

async def stream_response(user_message: str, pdf_context: str):
    """
    Generates a streaming response from the OpenAI model based on the provided PDF context.
    Compatible with the OpenAI SDK v1.x (handles ContentDeltaEvent correctly).
    """
    prompt = f"""
    You are an assistant that answers questions **only** based on the following PDF content.

    PDF CONTEXT:
    {pdf_context}

    USER QUESTION:
    {user_message}

    Please provide a clear and concise answer using only the information found in the PDF.
    """

    # Streaming responses are synchronous (no await)
    with client.chat.completions.stream(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
    ) as stream:
        for event in stream:
            # Partial text chunks are in ContentDeltaEvent
            if event.type == "content.delta" and event.delta:
                yield f'{{"type": "content", "content": "{event.delta}"}}'
            elif event.type == "message.stop":
                break

    # Signal that streaming is complete
    yield '{"type": "done"}'
