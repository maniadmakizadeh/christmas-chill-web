#!/usr/bin/env python3
"""
CHRISTMAS CHILL IP updater.
Keeps the public IP in server-ip.json in your GitHub Pages repository.
Run this on the PC that hosts HLDS. Keep your GitHub token private.
"""
import base64, json, os, time, urllib.request, urllib.error
from datetime import datetime, timezone

GITHUB_OWNER = os.environ.get("GITHUB_OWNER", "YOUR_GITHUB_USERNAME")
GITHUB_REPO = os.environ.get("GITHUB_REPO", "YOUR_REPOSITORY")
GITHUB_BRANCH = os.environ.get("GITHUB_BRANCH", "main")
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "")
PORT = int(os.environ.get("CS_PORT", "27015"))
MAP = os.environ.get("CS_MAP", "de_dust2_2x2_xmas")
POLL_SECONDS = int(os.environ.get("POLL_SECONDS", "300"))
FILE_PATH = "server-ip.json"

def request_json(url, method="GET", payload=None, token=None):
    data = None if payload is None else json.dumps(payload).encode()
    headers = {"Accept": "application/vnd.github+json", "User-Agent": "ChristmasChill-IP-Updater"}
    if token: headers["Authorization"] = "Bearer " + token
    if data is not None: headers["Content-Type"] = "application/json"
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    with urllib.request.urlopen(req, timeout=20) as response:
        body = response.read()
        return json.loads(body.decode()) if body else {}

def get_public_ip():
    with urllib.request.urlopen("https://api.ipify.org", timeout=15) as r:
        ip = r.read().decode().strip()
    parts = ip.split(".")
    if len(parts) != 4 or any(not p.isdigit() or not 0 <= int(p) <= 255 for p in parts):
        raise RuntimeError("Public IP service returned an invalid IPv4 address")
    return ip

def publish(ip):
    api = f"https://api.github.com/repos/{GITHUB_OWNER}/{GITHUB_REPO}/contents/{FILE_PATH}"
    try:
        existing = request_json(api + f"?ref={GITHUB_BRANCH}", token=GITHUB_TOKEN)
        sha = existing.get("sha")
    except urllib.error.HTTPError as e:
        if e.code != 404: raise
        sha = None

    payload_obj = {
        "ip": ip,
        "port": PORT,
        "map": MAP,
        "updated_at": datetime.now(timezone.utc).isoformat()
    }
    content = base64.b64encode((json.dumps(payload_obj, indent=2) + "\n").encode()).decode()
    payload = {"message": "Update CS 1.6 server public IP", "content": content, "branch": GITHUB_BRANCH}
    if sha: payload["sha"] = sha
    request_json(api, method="PUT", payload=payload, token=GITHUB_TOKEN)

def main():
    if not GITHUB_TOKEN or GITHUB_OWNER == "YOUR_GITHUB_USERNAME" or GITHUB_REPO == "YOUR_REPOSITORY":
        raise SystemExit("Set GITHUB_TOKEN, GITHUB_OWNER and GITHUB_REPO environment variables first.")
    last_ip = None
    print("CHRISTMAS CHILL IP updater started; checking every", POLL_SECONDS, "seconds.")
    while True:
        try:
            ip = get_public_ip()
            if ip != last_ip:
                publish(ip)
                print(f"Published public IP {ip}:{PORT}")
                last_ip = ip
        except Exception as exc:
            print("Update failed:", exc)
        time.sleep(POLL_SECONDS)

if __name__ == "__main__":
    main()
