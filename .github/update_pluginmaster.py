#!/usr/bin/env python3
"""Update pluginmaster.json entry for ChatTwo after a release.

Called from release.yml with:
    python3 .github/update_pluginmaster.py <repo_path> <version> <repo_full_name>
"""
import json
import os
import sys
import time

repo_path = sys.argv[1]
version = sys.argv[2]
repo_full_name = sys.argv[3]

json_path = os.path.join(repo_path, 'pluginmaster.json')

# Read existing pluginmaster.json (or start fresh)
if os.path.exists(json_path):
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
else:
    data = []

# Find existing ChatTwo entry or create new one
entry = None
for item in data:
    if item.get('InternalName') == 'ChatTwo':
        entry = item
        break

if entry is None:
    entry = {}
    data.append(entry)

download_url = f"https://github.com/{repo_full_name}/releases/download/v{version}/latest.zip"

entry.update({
    'Name': 'Chat 2',
    'Author': 'Infi, Anna',
    'Punchline': 'Electric Boogaloo - A whole new chat, a new fantastic chat window',
    'Description': (
        'Chat 2 is a complete rewrite of the in-game chat window as a plugin.\n'
        'It supports:\n\n'
        '- Unlimited tabs\n'
        '- Tabs that always send to a certain channel\n'
        '- More flexible filtering\n'
        '- RGB channel colouring\n'
        '- Completely variable font size\n'
        '- Sidebar tabs\n'
        '- Unread counts\n'
        '- Emotes\n'
        '- Screenshot mode (obfuscate names)'
    ),
    'InternalName': 'ChatTwo',
    'AssemblyVersion': version,
    'TestingAssemblyVersion': version,
    'DalamudApiLevel': 15,
    'TestingDalamudApiLevel': 15,
    'DownloadLinkInstall': download_url,
    'DownloadLinkUpdate': download_url,
    'DownloadLinkTesting': download_url,
    'RepoUrl': f'https://github.com/{repo_full_name}',
    'IconUrl': download_url,
    'Tags': ['Social', 'UI', 'Chat', 'Replacement'],
    'ApplicableVersion': 'any',
    'LoadPriority': 0,
    'AcceptsFeedback': True,
    'LastUpdate': int(time.time()),
})

with open(json_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=4, ensure_ascii=False)
