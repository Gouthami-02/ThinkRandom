import os
import json

from google import genai


client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def analyze_answer(answer, topic):

    prompt = f"""
You are a communication coach.

Analyze the user's answer to this practice topic.

Topic:
{topic}

User answer:
{answer}

Evaluate these communication factors:

1. Clarity
2. Structure
3. Vocabulary
4. Fluency
5. Filler words

Give each score from 0 to 100.

Return ONLY valid JSON in this exact format:

{{
    "clarity_score": 0,
    "structure_score": 0,
    "vocabulary_score": 0,
    "fluency_score": 0,
    "filler_word_count": 0,
    "feedback": "Short, actionable feedback"
}}
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    text = response.text.strip()

    if text.startswith("```"):
        text = text.replace("```json", "")
        text = text.replace("```", "")
        text = text.strip()

    try:
        result = json.loads(text)
    except json.JSONDecodeError:
        raise ValueError(
            "Gemini returned an invalid JSON response."
        )

    required_fields = [
        "clarity_score",
        "structure_score",
        "vocabulary_score",
        "fluency_score",
        "filler_word_count",
        "feedback",
    ]

    for field in required_fields:
        if field not in result:
            raise ValueError(
                f"Gemini response is missing required field: {field}"
            )

    score_fields = [
        "clarity_score",
        "structure_score",
        "vocabulary_score",
        "fluency_score",
    ]

    for field in score_fields:
        score = result[field]

        if not isinstance(score, (int, float)):
            raise ValueError(
                f"{field} must be a number."
            )

        if not 0 <= score <= 100:
            raise ValueError(
                f"{field} must be between 0 and 100."
            )

    if not isinstance(
        result["filler_word_count"],
        int
    ):
        raise ValueError(
            "filler_word_count must be an integer."
        )

    if result["filler_word_count"] < 0:
        raise ValueError(
            "filler_word_count cannot be negative."
        )

    if not isinstance(result["feedback"], str):
        raise ValueError(
            "feedback must be a string."
        )

    return result