def build_prompt(question, text_chunks, image_descriptions):
    context = "\n".join(
        [f"- {chunk}" for chunk in text_chunks]
    )

    images = "\n".join(
        [f"- Image evidence: {desc}" for desc in image_descriptions]
    )

    return f"""
You are an AI assistant answering questions STRICTLY using the provided context.

CONTEXT (Text):
{context}

CONTEXT (Images):
{images}

RULES:
- Use ONLY the given context
- If unsure, say "Insufficient information"
- Do NOT hallucinate

QUESTION:
{question}

ANSWER:
"""
