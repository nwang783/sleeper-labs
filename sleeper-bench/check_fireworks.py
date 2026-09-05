"""Read Fireworks model metadata without inference calls or credential output."""
import json
import os
from pathlib import Path

import httpx
from dotenv import load_dotenv


def main():
    load_dotenv(Path(__file__).parent / ".env")
    key = os.getenv("FIREWORKS_API_KEY")
    if not key:
        raise SystemExit("FIREWORKS_API_KEY is missing from .env/environment")
    rows = []
    params = {"pageSize": 200}
    with httpx.Client(timeout=30, follow_redirects=False) as client:
        while True:
            response = client.get("https://api.fireworks.ai/v1/accounts/fireworks/models",
                                  headers={"Authorization": f"Bearer {key}"}, params=params)
            if response.status_code != 200:
                raise SystemExit(f"Fireworks model lookup returned HTTP {response.status_code}")
            data = response.json()
            for model in data.get("models", []):
                name = model["name"]
                if any(family in name.lower() for family in ("gemma", "qwen", "llama", "gpt-oss")):
                    rows.append({"id": name, "serverless": model.get("supportsServerless", False),
                                 "tools": model.get("supportsTools", False),
                                 "parameters": model.get("baseModelDetails", {}).get("parameterCount")})
            token = data.get("nextPageToken")
            if not token:
                break
            params["pageToken"] = token
    print(json.dumps(rows, indent=2))


if __name__ == "__main__":
    main()
