import os
import json

from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(
api_key=os.getenv("GEMINI_API_KEY")
)

def classify_persona(user_message: str):


    text = user_message.lower()

    technical_keywords = [
        "api",
        "token",
        "authentication",
        "database",
        "logs",
        "configuration",
        "endpoint",
        "server",
        "http",
        "401",
        "500",
        "integration",
        "bearer"
    ]

    frustrated_keywords = [
        "not working",
        "broken",
        "frustrated",
        "angry",
        "nothing works",
        "tried everything",
        "urgent",
        "failed",
        "issue",
        "problem",
        "still not working"
    ]

    business_keywords = [
        "operations",
        "timeline",
        "business",
        "revenue",
        "impact",
        "executive",
        "resolution",
        "uptime",
        "customer impact",
        "downtime"
    ]

    for keyword in technical_keywords:

        if keyword in text:

            return {
                "persona": "Technical Expert",
                "confidence": 0.95,
                "reasoning": f"Detected technical keyword: {keyword}"
            }

    for keyword in frustrated_keywords:

        if keyword in text:

            return {
                "persona": "Frustrated User",
                "confidence": 0.95,
                "reasoning": f"Detected frustration keyword: {keyword}"
            }

    for keyword in business_keywords:

        if keyword in text:

            return {
                "persona": "Business Executive",
                "confidence": 0.95,
                "reasoning": f"Detected business keyword: {keyword}"
            }

    prompt = f"""
    ```

    You are a customer persona classification engine.

    Classify the customer into EXACTLY ONE category:

    1. Technical Expert
    2. Frustrated User
    3. Business Executive

    Return ONLY valid JSON.

    Example:

    {{
    "persona": "Technical Expert",
    "confidence": 0.92,
    "reasoning": "Customer is discussing APIs and authentication."
    }}

    Customer Message:
    {user_message}
    """

    
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    output = response.text.strip()

    if output.startswith("```json"):
        output = output.replace("```json", "")
        output = output.replace("```", "")
        output = output.strip()

    return json.loads(output)
   

    if name == "main":

      test_message = (
        "How does this issue impact operations and when will it be resolved?"
      )

    result = classify_persona(
        test_message
    )

    print(
        json.dumps(
            result,
            indent=4
        )
    )
    
