from dotenv import load_dotenv
import os
import cohere
from app.llm.base import LLMClient

load_dotenv()

class CohereClient(LLMClient):

    def __init__(self):
        self.client = cohere.ClientV2(
            api_key=os.getenv("COHERE_API_KEY")
        )

    def generate(self, prompt: str, temperature: float = 0.2) -> str:
        """Genera texto con Cohere.

        Se permite configurar la temperatura para que tareas como la
        clasificación de intención sean totalmente deterministas
        (temperature=0.0), mientras que las respuestas conversacionales
        pueden seguir usando un valor ligeramente creativo.
        """

        response = self.client.chat(
            model="command-r-plus-08-2024",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=temperature
        )

        return response.message.content[0].text.strip()
