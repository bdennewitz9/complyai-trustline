import json
import uuid
import openai
import os
import re

class ComplianceScanner:
    def __init__(self, api_key):
        registry_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "compliance_registry.json")
        )
        try:
            with open(registry_path, "r", encoding="utf-8") as f:
                self.registry = json.load(f)
        except FileNotFoundError:
            self.registry = {}
            print("⚠️ compliance_registry.json not found. Scanner may have limited functionality.")

        self.api_key = api_key
        openai.api_key = api_key

    def scan(self, doc_text, doc_type, company_size):
        results = {
            "flags": [],
            "document_type": doc_type,
            "company_size": company_size,
            "scan_id": str(uuid.uuid4())
        }

        sentences = re.split(r"(?<=[.!?])\s+", doc_text)

        for module_name, rules in self.registry.items():
            if module_name == "registry_version":
                continue  # skip metadata
            for rule in rules:
                trigger = rule["trigger"].lower()
                for sentence in sentences:
                    if trigger in sentence.lower():
                        suggested_rewrite = sentence.replace(
                            rule["trigger"], rule["guidance"].split("Use '")[-1].split("'")[0]
                        )

                        results["flags"].append({
                            "id": str(uuid.uuid4()),
                            "module": module_name,
                            "flag_type": rule["type"],
                            "original_text": rule["trigger"],
                            "flagged_sentence": sentence.strip(),
                            "rewrite_guidance": rule["guidance"],
                            "suggested_rewrite": suggested_rewrite.strip(),
                            "citation": rule["citation"],
                            "confidence_score": rule.get("confidence", 95)
                        })
                        break  # only flag one match per rule per scan

        return results
