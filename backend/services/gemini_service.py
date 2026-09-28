import os

from dotenv import load_dotenv
from google import genai


load_dotenv()


GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


client = None

if GEMINI_API_KEY:
    client = genai.Client(
        api_key=GEMINI_API_KEY
    )


def generate_recommendation(prompt: str) -> str:
    """
    Generate an AI recommendation using Gemini Interactions API.
    """

    if not GEMINI_API_KEY:
        return (
            "AI service is not configured. "
            "Please configure GEMINI_API_KEY."
        )

    if client is None:
        return "AI client could not be initialized."

    try:

        interaction = client.interactions.create(
            model="gemini-3.8-flash",
            input=prompt
        )

        if interaction.output_text:
            return interaction.output_text

        return "No recommendation was generated."

    except Exception as error:

        error_text = str(error)

        if "429" in error_text or "Rate limit exceeded" in error_text:

            return (
                "AI_LIMIT_REACHED"
            )

        return (
            f"AI generation error: {error_text}"
        )