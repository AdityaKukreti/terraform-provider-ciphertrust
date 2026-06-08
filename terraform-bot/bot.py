import json, os, requests


e = json.load(open(os.environ["GITHUB_EVENT_PATH"], encoding="utf-8"))
r = e["repository"]["full_name"]
i = e.get("issue")
if not i or "pull_request" in i:
    raise SystemExit(0)

t = (i.get("title", "") + " " + (i.get("body") or "")).lower()
rules = {
    "bug": ["bug", "error", "fail", "crash"],
    "enhancement": ["feature