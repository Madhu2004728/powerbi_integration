import sys
import os
import requests
from dotenv import load_dotenv

# Explicitly load .env from the root directory
load_dotenv(os.path.join(os.getcwd(), ".env"), override=True)

# Add the backend directory to sys.path so we can import from app
sys.path.append(os.path.join(os.getcwd(), "backend"))

from app.services.powerbi.auth import get_access_token

def test_full_embedding():
    # Import settings INSIDE the function to ensure it loads after load_dotenv(override=True)
    from app.core.config import settings
    
    print("--- Power BI Full Embedding Test ---")

    # 1. Get Access Token
    try:
        print("\n1. Attempting to get Access Token...")
        access_token = get_access_token()
        print("SUCCESS! Access Token retrieved.")
        print("-" * 30 + " ACCESS TOKEN " + "-" * 30)
        print(access_token)
        print("-" * 74)
    except Exception as e:
        print(f"FAILED to get Access Token: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Response Body: {e.response.text}")
        return

    # 2. Workspace and Report IDs
    workspace_id = settings.POWERBI_WORKSPACE_ID
    report_id = settings.POWERBI_REPORT_ID

    # 3. Get Report Metadata
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    report_api = f"https://api.powerbi.com/v1.0/myorg/groups/{workspace_id}/reports/{report_id}"

    try:
        print("\n2. Fetching Report Metadata (to get Embed URL)...")
        response = requests.get(report_api, headers=headers)
        response.raise_for_status()
        report_data = response.json()
        embed_url = report_data["embedUrl"]
        dataset_id = report_data["datasetId"]
        print(f"SUCCESS! Embed URL found.")
    except Exception as e:
        print(f"FAILED to get Report Metadata: {e}")
        print("\nNOTE: Ensure your Azure App is added as a 'Member' to the Power BI Workspace.")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Response Body: {e.response.text}")
        return

    # 4. Generate Embed Token
    token_api = "https://api.powerbi.com/v1.0/myorg/GenerateToken"
    token_payload = {
        "datasets": [{"id": dataset_id}],
        "reports": [{"id": report_id}]
    }

    try:
        print("\n3. Generating Embed Token...")
        token_response = requests.post(token_api, headers=headers, json=token_payload)
        token_response.raise_for_status()
        embed_token = token_response.json()["token"]
        print("SUCCESS! Embed Token generated.")
        
        print(f"\n" + "=" * 25 + " FINAL RESULTS " + "=" * 25)
        print(f"Embed URL: {embed_url}")
        print("\n" + "-" * 30 + " EMBED TOKEN " + "-" * 30)
        print(embed_token)
        print("-" * 73)
        print(f"\nTest Complete.")
    except Exception as e:
        print(f"FAILED to generate Embed Token: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Response Body: {e.response.text}")

if __name__ == "__main__":
    test_full_embedding()
