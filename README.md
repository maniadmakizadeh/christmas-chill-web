# CHRISTMAS CHILL website

A customizable, responsive single-page site inspired by the supplied mockup.

## Files
- `index.html`: website UI and styles.
- `server-ip.json`: public IP data consumed by the website.
- `updater.py`: runs on the PC hosting HLDS and updates `server-ip.json` in your GitHub repository when your public IPv4 changes.

## Publish the website with GitHub Pages
1. Create a public GitHub repository (for example `christmas-chill`).
2. Upload `index.html` and `server-ip.json` to the repository root.
3. In repository Settings → Pages, enable deployment from the `main` branch and `/ (root)`.
4. Your site will appear at `https://YOURNAME.github.io/christmas-chill/`.

## Configure automatic IP updates
1. In GitHub, create a fine-grained personal access token limited to this repository, with **Contents: Read and write** permission. Do not put the token in `index.html` or any public file.
2. Install Python 3 on the HLDS host PC.
3. Open PowerShell in this folder and set environment variables for the current terminal session (replace the example values):

```powershell
$env:GITHUB_OWNER="YOUR_GITHUB_USERNAME"
$env:GITHUB_REPO="christmas-chill"
$env:GITHUB_BRANCH="main"
$env:GITHUB_TOKEN="YOUR_PRIVATE_TOKEN"
$env:CS_PORT="27015"
$env:CS_MAP="de_dust2_2x2_xmas"
python .\updater.py
```

The script checks every 5 minutes and only commits when the public IP changes. Keep the updater running on the host PC. Use Windows Task Scheduler to start it when you log in or boot.

## Important
- This updates the displayed **public IPv4 address**, not a private LAN address such as `192.168.x.x`.
- Your router must forward the selected UDP port to the HLDS PC, and your ISP must allow inbound connections. If the ISP uses CGNAT, port forwarding may not work.
- The website currently displays the IP and map from `server-ip.json`. Player count / real online status need a separate server query/API.
- The email form is a styled front-end placeholder only. Do not collect email addresses until you connect a real email backend/provider. For notifications, use a backend/email service; never expose provider API keys in browser JavaScript.
- “Connect Now” copies the `connect IP:PORT` command; it cannot reliably launch every player's local CS 1.6 client directly from a browser.
- Change the port and map in `updater.py` environment variables or edit the website `CONFIG` section.
