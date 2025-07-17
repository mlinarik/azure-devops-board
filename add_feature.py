import os
import requests
import base64
from datetime import datetime

# Set these values
AZURE_ORG = os.getenv('AZURE_ORG', 'ORG_NAME')
AZURE_PROJECT = os.getenv('AZURE_PROJECT', 'PROJECT_NAME')
AZURE_TEAM = os.getenv('AZURE_TEAM', 'TEAM_NAME')
AZURE_PAT = 'xxx'  # Replace with your Personal Access Token

API_URL = f"https://dev.azure.com/{AZURE_ORG}/{AZURE_PROJECT}/_apis/wit/workitems/$Epic?api-version=7.0"

# Encode PAT for Basic Auth
pat_bytes = f":{AZURE_PAT}".encode("utf-8")
pat_base64 = base64.b64encode(pat_bytes).decode("utf-8")

headers = {
    'Content-Type': 'application/json-patch+json',
    'Authorization': f'Basic {pat_base64}'
}

def create_epic(title, description):
    today = datetime.now().strftime('%Y-%m-%d')
    title_with_date = f"{title} [{today}]"
    data = [
        {"op": "add", "path": "/fields/System.Title", "value": title_with_date},
        {"op": "add", "path": "/fields/System.Description", "value": description},
        {"op": "add", "path": "/fields/System.TeamProject", "value": AZURE_PROJECT},
        {"op": "add", "path": "/fields/System.AreaPath", "value": "Pied-Piper\\pied_piper"},
        {"op": "add", "path": "/fields/System.WorkItemType", "value": "Epic"}
    ]
    response = requests.post(API_URL, json=data, headers=headers)
    if response.status_code == 200 or response.status_code == 201:
        print(f"Epic '{title_with_date}' created successfully and added to the backlog.")
    else:
        print(f"Failed to create epic: {response.text}")

def create_feature(title, description=None):
    today = datetime.now().strftime('%Y-%m-%d')
    title_with_date = f"{title} [{today}]"
    # Use the requested description format
    user_story = "User Story: As a blank, I need black, because of blank."
    acceptance_criteria = "Acceptance Criteria:\n- The feature is visible on the Pied-Piper board.\n- The feature includes tags: 2025Q4, SEC, RTB.\n- The feature is created with today's date in the title."
    full_description = f"{user_story}\n\n{acceptance_criteria}"
    data = [
        {"op": "add", "path": "/fields/System.Title", "value": title_with_date},
        {"op": "add", "path": "/fields/System.Description", "value": full_description},
        {"op": "add", "path": "/fields/System.TeamProject", "value": AZURE_PROJECT},
        {"op": "add", "path": "/fields/System.AreaPath", "value": "Pied-Piper\\pied_piper"},
        {"op": "add", "path": "/fields/System.WorkItemType", "value": "Feature"},
        {"op": "add", "path": "/fields/System.Tags", "value": "2025Q4; SEC; RTB"}
    ]
    url = f"https://dev.azure.com/{AZURE_ORG}/{AZURE_PROJECT}/_apis/wit/workitems/$Feature?api-version=7.0"
    response = requests.post(url, json=data, headers=headers)
    if response.status_code in [200, 201]:
        feature_id = response.json()['id']
        print(f"Feature '{title_with_date}' created successfully. Feature ID: {feature_id}")
        return feature_id
    else:
        print(f"Failed to create feature: {response.text}")
        return None


def create_pbi(title, description):
    today = datetime.now().strftime('%Y-%m-%d')
    title_with_date = f"{title} [{today}]"
    data = [
        {"op": "add", "path": "/fields/System.Title", "value": title_with_date},
        {"op": "add", "path": "/fields/System.Description", "value": description},
        {"op": "add", "path": "/fields/System.TeamProject", "value": AZURE_PROJECT},
        {"op": "add", "path": "/fields/System.AreaPath", "value": "Pied-Piper\\pied_piper"},
        {"op": "add", "path": "/fields/System.WorkItemType", "value": "Product Backlog Item"}
    ]
    url = f"https://dev.azure.com/{AZURE_ORG}/{AZURE_PROJECT}/_apis/wit/workitems/$Product%20Backlog%20Item?api-version=7.0"
    response = requests.post(url, json=data, headers=headers)
    if response.status_code in [200, 201]:
        pbi_id = response.json()['id']
        print(f"Product Backlog Item '{title_with_date}' created successfully.")
        return pbi_id
    else:
        print(f"Failed to create product backlog item: {response.text}")
        return None

if __name__ == "__main__":
    # Create Feature only (not Epic or PBI)
    create_feature("Sample Feature", "Feature without parent or child relationship")
