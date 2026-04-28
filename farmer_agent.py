import os
import openai
from typing import Optional

class AgentError(Exception):
    pass

class FarmerAgent:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if self.api_key:
            openai.api_key = self.api_key
            self.use_api = True
        else:
            self.use_api = False

        self.system_prompt = (
            "You are AgriGPT, an AI assistant for farmers. "
            "Provide clear, practical advice for crop selection, soil care, pest management, and weather-aware farming. "
            "If you cannot answer, say so politely and suggest practical general guidelines."
        )

    def ask(self, question: str) -> str:
        question = question.strip()
        if not question:
            raise AgentError("Empty question provided.")

        if self.use_api:
            try:
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": self.system_prompt},
                        {"role": "user", "content": question},
                    ],
                    max_tokens=250,
                    temperature=0.7,
                )
                return response.choices[0].message.content.strip()
            except openai.error.OpenAIError as error:
                raise AgentError(f"OpenAI API error: {error}") from error
            except Exception as error:
                raise AgentError(f"Unexpected response error: {error}") from error
        else:
            return self._local_answer(question)

    def _local_answer(self, question: str) -> str:
        text = question.lower()
        if "dry" in text or "drought" in text:
            return (
                "For dry climates, choose drought-tolerant crops such as millet, sorghum, chickpeas, or sesame. "
                "Use mulch, drip irrigation, and conserve soil moisture."
            )
        if "pest" in text or "insect" in text or "disease" in text:
            return (
                "Monitor fields regularly, remove infected plants, and use integrated pest management. "
                "Encourage beneficial insects and avoid overusing chemical sprays."
            )
        if "soil" in text or "fertility" in text or "nutrition" in text:
            return (
                "Test the soil first. Add compost or organic matter, maintain pH balance, and rotate crops to keep soil healthy."
            )
        if "weather" in text or "rain" in text or "temperature" in text:
            return (
                "Plan planting around the local forecast. Protect young plants from late frost and use shade or irrigation during heat waves."
            )
        return (
            "AgriGPT local fallback: choose resilient crops, maintain soil health, and keep good field records. "
            "For more precise advice, set OPENAI_API_KEY and run again."
        )
