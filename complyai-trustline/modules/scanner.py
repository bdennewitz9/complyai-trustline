import uuid
import openai
import json

class ComplianceScanner:
    def __init__(self, api_key):
        openai.api_key = api_key
        with open("compliance_registry.json") as f:
            self.registry = json.load(f)

    def scan(self, text, doc_type, company_size):
        flags = []
        for rule in self.registry:
            if rule["module"] == "ADA" and company_size == "<15":
                continue  # ADA doesn’t apply under 15 employees

            prompt = f"""
Scan the following {doc_type} text for signs of {rule['description']}.
If any are found, return flagged text, a rewrite guidance, and a confidence score (0-100%).

Text:
{text}
"""

            try:
                response = openai.ChatCompletion.create(
                    model="gpt-4",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.3
                )
                content = response.choices[0].message.content
                result = {
                    "id": str(uuid.uuid4())[:8],
                    "module": rule["module"],
                    "flag_type": rule["flag_type"],
                    "citation": rule["citation"],
                    "original_text": text[:300],  # truncate for demo
                    "rewrite_guidance": content,
                    "confidence_score": 90  # static score for now
                }
                flags.append(result)
            except Exception as e:
                print("Scan error:", e)

        return {"flags": flags}
