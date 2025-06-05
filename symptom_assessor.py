import os
import google.generativeai as genai
from secret_key import GeminiAi_key

# --- Configure Gemini API ---
if not GeminiAi_key :
    raise ValueError("❌ API_KEY is missing! Please check your secret_key.py file.")

genai.configure(api_key=GeminiAi_key)

# --- Initialize Gemini Model (Text Only) ---
try:
    model = genai.GenerativeModel("gemini-pro")
except Exception as e:
    raise RuntimeError(f"❌ Failed to initialize Gemini model: {e}")

# --- Main Function to Assess Symptoms ---
def assess_symptoms(symptoms: str, duration: str) -> str:
    """
    Analyze patient symptoms using Gemini and return an assessment.
    
    Parameters:
        symptoms (str): Description of symptoms from the user.
        duration (str): How long the symptoms have persisted.
    
    Returns:
        str: AI-generated assessment or user-friendly error.
    """
    if not symptoms.strip() or not duration.strip():
        return "⚠️ Please provide both symptoms and their duration."

    prompt = (
        f"Patient describes the following symptoms: {symptoms}.\n"
        f"Duration: {duration}.\n\n"
        "As an AI healthcare assistant (not a licensed doctor), analyze the symptoms and provide:\n"
        "1. Possible causes or related conditions.\n"
        "2. Severity level (mild, moderate, critical).\n"
        "3. If urgent attention is needed.\n"
        "4. Suggestions for next steps or medical departments to consult.\n"
        "Please respond clearly, concisely, and in bullet points."
    )

    try:
        response = model.generate_content(prompt)
        return response.text.strip() if response and hasattr(response, 'text') else "⚠️ No response received from the model."
    except Exception as e:
        return f"❌ Error during symptom assessment: {str(e)}"