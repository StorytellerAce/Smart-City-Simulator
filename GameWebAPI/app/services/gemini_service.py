import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import time

load_dotenv()

class GeminiService:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY is not set.")
        self.client = genai.Client(api_key=api_key)
        self.model = "gemini-2.5-flash"

    def generate_with_memory(
        self,
        prompt: str,
        previous_interaction_id: str | None = None
    ):
        retries = 3
        delay = 2

        for attempt in range(retries):
            try:
                if previous_interaction_id:
                    response = self.client.interactions.create(
                        model=self.model,
                        input=prompt,
                        previous_interaction_id=previous_interaction_id
                    )
                else:
                    response = self.client.interactions.create(
                        model=self.model,
                        input=prompt
                    )

                return {
                    "text": response.output_text,
                    "interaction_id": response.id
                }

            except Exception as e:
                print(f"[Gemini ERROR] attempt {attempt+1}: {e}")

                if attempt == retries - 1:
                    raise  # still fail then let caller handle fallback

                time.sleep(delay)
                delay *= 2  # exponential backoff