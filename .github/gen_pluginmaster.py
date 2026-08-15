#!/usr/bin/env python3
"""Generate pluginmaster.json for ChatTwo by querying GitHub Releases API.

This script fetches the latest stable and testing releases from GitHub,
extracts changelogs, download counts, and Dalamud API levels, then writes
a complete pluginmaster.json entry for ChatTwo.

Usage:
    python3 .github/gen_pluginmaster.py [REPO_OWNER/REPO_NAME] [OUTPUT_PATH]

Defaults:
    REPO  = QianChangUwU/ChatTwo  (or env GITHUB_REPOSITORY)
    OUTPUT = pluginmaster.json (in GITHUB_WORKSPACE or cwd)
"""
import json
import os
import sys
import time

import requests

REPO = os.environ.get("GITHUB_REPOSITORY", "QianChangUwU/ChatTwo")
if len(sys.argv) > 1 and "/" in sys.argv[1]:
    REPO = sys.argv[1]

ROOT = os.environ.get("GITHUB_WORKSPACE", ".")
OUTPUT = os.path.join(ROOT, "pluginmaster.json")
if len(sys.argv) > 2:
    OUTPUT = sys.argv[2]

CSPROJ = "ChatTwo/ChatTwo.csproj"


def get_dalamud_api_level(release):
    """Extract Dalamud API level from the csproj at the release tag."""
    tag = release["tag_name"]
    url = f"https://raw.githubusercontent.com/{REPO}/refs/tags/{tag}/{CSPROJ}"
    text = requests.get(url).text
    # Parse: <Project Sdk="Dalamud.NET.Sdk/15.0.0">
    return text.split('Dalamud.NET.Sdk/')[1].split('.')[0]


def get_changelog(release):
    """Extract changelog text from the release body."""
    body = release.get("body", "") or ""
    return body.strip()


def get_releases():
    """Fetch the latest stable (prerelease=False) and testing (prerelease=True) releases."""
    data = requests.get(
        f"https://api.github.com/repos/{REPO}/releases",
        headers={"Accept": "application/vnd.github+json"},
    ).json()

    testing, latest = None, None
    total_downloads = 0

    for r in data:
        if not testing and r.get("prerelease") is True:
            testing = r
            testing["_dalamud"] = get_dalamud_api_level(testing)
            testing["_changelog"] = get_changelog(testing)
        elif not latest and r.get("prerelease") is False:
            latest = r
            latest["_dalamud"] = get_dalamud_api_level(latest)
            latest["_changelog"] = get_changelog(latest)
        for a in r.get("assets", []):
            total_downloads += a.get("download_count", 0)

    return testing, latest, total_downloads


def main():
    testing, latest, downloads = get_releases()

    if not latest:
        print("Error: No stable release found.")
        sys.exit(1)

    entry = {
        "Name": "Chat 2",
        "Author": "Infi, Anna",
        "Punchline": "Electric Boogaloo - A whole new chat, a new fantastic chat window",
        "Description": (
            "Chat 2 is a complete rewrite of the in-game chat window as a plugin.\n"
            "It supports:\n\n"
            "- Unlimited tabs\n"
            "- Tabs that always send to a certain channel\n"
            "- More flexible filtering\n"
            "- RGB channel colouring\n"
            "- Completely variable font size\n"
            "- Sidebar tabs\n"
            "- Unread counts\n"
            "- Emotes\n"
            "- Screenshot mode (obfuscate names)"
        ),
        "InternalName": "ChatTwo",
        "AssemblyVersion": latest["tag_name"].lstrip("v"),
        "TestingAssemblyVersion": (testing["tag_name"].lstrip("v") if testing
                                   else latest["tag_name"].lstrip("v")),
        "DalamudApiLevel": int(latest["_dalamud"]),
        "TestingDalamudApiLevel": int(testing["_dalamud"]) if testing else int(latest["_dalamud"]),
        "DownloadLinkInstall": latest["assets"][0]["browser_download_url"],
        "DownloadLinkUpdate": latest["assets"][0]["browser_download_url"],
        "DownloadLinkTesting": (testing["assets"][0]["browser_download_url"] if testing
                                 else latest["assets"][0]["browser_download_url"]),
        "RepoUrl": f"https://github.com/{REPO}",
        "IconUrl": latest["assets"][0]["browser_download_url"],
        "Tags": ["Social", "UI", "Chat", "Replacement"],
        "ApplicableVersion": "any",
        "LoadPriority": 0,
        "AcceptsFeedback": True,
        "DownloadCount": downloads,
        "LastUpdate": int(time.time()),
        "Changelog": f"Latest {latest['tag_name']}:\n{latest['_changelog']}\n\n"
                     + (f"Testing {testing['tag_name']}:\n{testing['_changelog']}" if testing else ""),
    }

    # Load existing pluginmaster if present and merge
    existing = []
    if os.path.exists(OUTPUT):
        with open(OUTPUT, "r", encoding="utf-8") as f:
            existing = json.load(f)

    # Replace or append ChatTwo entry
    found = False
    for i, item in enumerate(existing):
        if item.get("InternalName") == "ChatTwo":
            existing[i] = entry
            found = True
            break
    if not found:
        existing.append(entry)

    with open(OUTPUT, "w", encoding="utf-8") as f:
        json.dump(existing, f, indent=4, ensure_ascii=False)

    print(f"pluginmaster.json written to {OUTPUT}")


if __name__ == "__main__":
    main()
