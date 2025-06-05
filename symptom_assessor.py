"""
symptom_assessor.py
-------------------
Gemini-powered helper for Symptom Assessment using LangChain.
This version can be executed directly for testing purposes.
Place this file in the same folder as main.py and secret_key.py
"""

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage

# Attempt to import the API key from secret_key.py
try:
    from secret_key import geminiai_key
except ImportError:
    print("Warning: 'secret_key.py' not found or 'geminiai_key' not defined.")
    print("Please create 'secret_key.py' in the same directory and set geminiai_key = 'YOUR_API_KEY_HERE'.")
    print("Using a placeholder API key. Symptom assessment will likely fail without a valid key.")
    geminiai_key = "YOUR_PLACEHOLDER_GEMINI_API_KEY" # Placeholder for direct execution if key is missing

# ────────────────────────────────────────────────────────────────────────────────
# Gemini via LangChain setup
# ────────────────────────────────────────────────────────────────────────────────
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",  # or "gemini-1.5-pro"
    temperature=0.6,
    google_api_key=geminiai_key
)

# ────────────────────────────────────────────────────────────────────────────────
# Public helper function for symptom assessment
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

    print(f"\n--- Sending prompt to Gemini ---\nPrompt: {prompt}\n------------------------------") # For debugging

    try:
        response = llm.invoke([HumanMessage(content=prompt)])
        return response.content.strip()
    except Exception as exc:
        return f"❌ Error generating response: {exc}"

# ────────────────────────────────────────────────────────────────────────────────
# Example usage when symptom_assessor.py is run directly
# ────────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("--- Running symptom_assessor.py directly for testing ---")

    # Example 1: Basic symptom assessment
    print("\nScenario 1: Basic symptoms")
    basic_symptoms = "Fever, sore throat, and body aches"
    basic_duration = "2 days"
    result_basic = assess_symptoms(basic_symptoms, basic_duration)
    print("\nAI Assessment (Basic):")
    print(result_basic)
    print("-" * 50)

    # Example 2: Symptoms with additional file content
    print("\nScenario 2: Symptoms with additional info")
    complex_symptoms = "Persistent headache, blurred vision, and dizziness"
    complex_duration = "1 week"
    # Simulate file content
    simulated_file_content = (
        "Patient is a 45-year-old male with a history of migraines. "
        "Recent blood pressure reading was 140/90 mmHg. "
        "No recent injuries reported. Family history of hypertension."
    )
    result_complex = assess_symptoms(complex_symptoms, complex_duration, simulated_file_content)
    print("\nAI Assessment (with file content):")
    print(result_complex)
    print("-" * 50)

    # Example 3: Edge case - missing symptoms
    print("\nScenario 3: Missing symptoms (should return an error/warning from the function itself)")
    missing_symptoms = ""
    missing_duration = "1 day"
    result_missing = assess_symptoms(missing_symptoms, missing_duration)
    print("\nAI Assessment (Missing Symptoms):")
    print(result_missing)
    print("-" * 50)

    print("\n--- Testing complete ---")
