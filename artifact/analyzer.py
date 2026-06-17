import os
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("GEMINI_API_KEY")
)

def analyze_ingredients(ingredients_text: str) -> dict:
    prompt = f"""You are a cosmetic safety expert. Analyze the following personal care product ingredient list and return ONLY a JSON object, no explanation, no markdown.

The JSON must have exactly this structure:
{{
  "summary": "2-3 sentence plain language summary of the product safety",
  "flagged": [
    {{
      "name": "ingredient name",
      "reason": "why it is concerning",
      "severity": "high" or "medium" or "low"
    }}
  ],
  "safe_highlights": ["beneficial ingredient 1", "beneficial ingredient 2"],
  "score": a number between 0 and 100
}}

Scoring rules:
- Start at 100
- Subtract 20 for each high severity ingredient
- Subtract 10 for each medium severity ingredient
- Subtract 3 for each low severity ingredient
- Add 2 for each beneficial ingredient
- Minimum score is 0, maximum is 100

Ingredient list:
{ingredients_text}"""

    response = client.chat.completions.create(
        model="google/gemini-2.0-flash-exp:free",
        messages=[{"role": "user", "content": prompt}]
    )

    raw = response.choices[0].message.content
    clean = raw.replace("```json", "").replace("```", "").strip()
    return json.loads(clean)