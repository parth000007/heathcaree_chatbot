"""
symptom_assessor.py
-------------------
Gemini-powered helper for Symptom Assessment using LangChain.
Place this file in the same folder as main.py
"""

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
from secret_key import geminiai_key  # Your Gemini API key

# ────────────────────────────────────────────────────────────────────────────────
# Gemini via LangChain setup
# ────────────────────────────────────────────────────────────────────────────────
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",  # or "gemini-1.5-pro"
    temperature=0.6,
    google_api_key=geminiai_key
)

# ────────────────────────────────────────────────────────────────────────────────
# Public helper
# ────────────────────────────────────────────────────────────────────────────────
def assess_symptoms(symptoms: str,
                    duration: str,
                    file_content: str | None = None) -> str:
    """
    Generate a preliminary AI assessment using Gemini via LangChain.
    """
    prompt_parts = [
        f"I have the following symptoms: {symptoms}.",
        f"These symptoms have been present for {duration}.",
    ]
    if file_content:
        # Limiting file_content to 4000 characters to stay within token limits and avoid excessive processing
        prompt_parts.append(f"Attached is additional medical information: {file_content[:4000]}.")
    prompt_parts.append(
        "Give a preliminary health insight (not a diagnosis), list possible causes, "
        "and general self-care advice in short bullet points."
    )

    prompt = " ".join(prompt_parts)

    try:
        response = llm.invoke([HumanMessage(content=prompt)])
        return response.content.strip()
    except Exception as exc:
        return f"❌ Error generating response: {exc}"