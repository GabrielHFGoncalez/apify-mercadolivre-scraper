"""
Apify & GitHub Deployment Automation Script
Author: GabrielHFGoncalez
Repo: GabrielHFGoncalez/apify-mercadolivre-scraper
Actor: mercadolivre-price-intel
"""

import base64
import os
import pathlib
import sys
from typing import Dict, Optional

from dotenv import load_dotenv
import httpx

# Load credentials from .env in parent or current dir
load_dotenv()
load_dotenv(pathlib.Path(__file__).resolve().parent.parent.parent / ".env")

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
APIFY_TOKEN = os.getenv("APIFY_TOKEN")
REPO_NAME = "apify-mercadolivre-scraper"
REPO_OWNER = "GabrielHFGoncalez"
REPO_FULL_NAME = f"{REPO_OWNER}/{REPO_NAME}"
ACTOR_NAME = "mercadolivre-price-intel"


def get_github_headers() -> Dict[str, str]:
    if not GITHUB_TOKEN:
        raise ValueError("GITHUB_TOKEN not found in environment or .env file.")
    return {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }


def ensure_github_repo(client: httpx.Client) -> Dict[str, str]:
    """Check if repository exists; if not, create it publicly."""
    headers = get_github_headers()
    check_url = f"https://api.github.com/repos/{REPO_FULL_NAME}"
    res = client.get(check_url, headers=headers)

    if res.status_code == 200:
        print(f"[*] GitHub repository '{REPO_FULL_NAME}' already exists.")
        return res.json()
    elif res.status_code == 404:
        print(f"[*] Creating new public repository '{REPO_FULL_NAME}' on GitHub...")
        create_payload = {
            "name": REPO_NAME,
            "description": "Apify Actor: Mercado Livre Price & Product Intelligence Scraper (LATAM) for Apify Store monetization.",
            "private": False,
            "has_issues": True,
            "has_projects": True,
            "has_wiki": False,
            "auto_init": False,
        }
        create_res = client.post("https://api.github.com/user/repos", headers=headers, json=create_payload)
        if create_res.status_code not in (200, 201):
            raise RuntimeError(f"Failed to create GitHub repo: {create_res.status_code} - {create_res.text}")
        print(f"[+] Repository '{REPO_FULL_NAME}' created successfully.")
        return create_res.json()
    else:
        raise RuntimeError(f"Error checking repo status: {res.status_code} - {res.text}")


def push_file_to_github(client: httpx.Client, file_rel_path: str, file_full_path: pathlib.Path):
    """Create or update a file in the GitHub repo via API."""
    headers = get_github_headers()
    content_bytes = file_full_path.read_bytes()
    content_b64 = base64.b64encode(content_bytes).decode("utf-8")

    api_path = file_rel_path.replace("\\", "/")
    content_url = f"https://api.github.com/repos/{REPO_FULL_NAME}/contents/{api_path}"

    # Check if file exists to get sha
    sha: Optional[str] = None
    res = client.get(content_url, headers=headers)
    if res.status_code == 200:
        sha = res.json().get("sha")

    payload = {
        "message": f"Sync {api_path} for Apify Actor deployment",
        "content": content_b64,
        "branch": "main",
    }
    if sha:
        payload["sha"] = sha

    put_res = client.put(content_url, headers=headers, json=payload)
    if put_res.status_code in (200, 201):
        status_action = "updated" if sha else "created"
        print(f"[+] File '{api_path}' {status_action} in repository.")
    else:
        print(f"[!] Failed to upload '{api_path}': {put_res.status_code} - {put_res.text}")


def sync_all_actor_files(actor_dir: pathlib.Path):
    """Walk through all files in actor directory and push to GitHub."""
    print(f"[*] Syncing actor directory '{actor_dir}' with GitHub...")
    with httpx.Client(timeout=30.0) as client:
        ensure_github_repo(client)

        ignored_dirs = {".venv", "__pycache__", "storage", ".git"}
        for root, dirs, files in os.walk(actor_dir):
            dirs[:] = [d for d in dirs if d not in ignored_dirs]
            for file in files:
                if file.endswith(".pyc") or file == ".env":
                    continue
                full_path = pathlib.Path(root) / file
                rel_path = full_path.relative_to(actor_dir)
                push_file_to_github(client, str(rel_path), full_path)

    print(f"\n[✓] All files synced to: https://github.com/{REPO_FULL_NAME}")


def link_apify_actor(client: httpx.Client):
    """Optional Apify API connector when APIFY_TOKEN is supplied."""
    if not APIFY_TOKEN:
        print("\n[i] APIFY_TOKEN not found in environment.")
        print("    To link directly to your Apify Account via API, set APIFY_TOKEN in .env.")
        print(f"    Alternatively, link your GitHub repository in Apify Console:")
        print(f"    -> https://console.apify.com/actors/new (Select 'Git repository' and paste 'https://github.com/{REPO_FULL_NAME}')")
        return

    print("\n[*] Connecting to Apify API with APIFY_TOKEN...")
    apify_headers = {
        "Authorization": f"Bearer {APIFY_TOKEN}",
        "Content-Type": "application/json",
    }
    actor_payload = {
        "name": ACTOR_NAME,
        "title": "Mercado Livre Price & Product Intelligence Scraper (LATAM)",
        "description": "High-speed product and price intelligence for Mercado Livre (Brazil & LATAM).",
        "versions": [
            {
                "versionNumber": "1.0",
                "sourceType": "GIT_REPO",
                "gitRepoUrl": f"https://github.com/{REPO_FULL_NAME}.git",
                "buildTag": "latest",
            }
        ],
    }

    res = client.post("https://api.apify.com/v2/acts", headers=apify_headers, json=actor_payload)
    if res.status_code in (200, 201):
        actor_data = res.json().get("data", {})
        print(f"[✓] Apify Actor created/linked successfully: ID {actor_data.get('id')}")
        print(f"    Console URL: https://console.apify.com/actors/{actor_data.get('id')}")
    else:
        print(f"[!] Apify API response ({res.status_code}): {res.text}")


def main():
    print("=" * 65)
    print(" Apify Actor Deployment & GitHub Sync Tool")
    print(f" Target Repository: {REPO_FULL_NAME}")
    print("=" * 65)

    actor_dir = pathlib.Path(__file__).resolve().parent
    sync_all_actor_files(actor_dir)

    with httpx.Client(timeout=30.0) as client:
        link_apify_actor(client)


if __name__ == "__main__":
    main()
