import json
import os
import re
from pathlib import Path

import requests
import yaml

BOT_MARKER = "<!-- terraform-issue-bot -->"
BASE = "https://api.github.com"


def load_event():
    with open(os.environ["GITHUB_EVENT_PATH"], "r", encoding="utf-8") as f:
        return json.load(f)


def headers():
    return {
        "Authorization": f"Bearer {os.environ['GITHUB_TOKEN']}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api