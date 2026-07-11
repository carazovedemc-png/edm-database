<div align="center">
<table style="border-collapse: collapse; border: none; margin-bottom: 20px;">
<tr style="border: none;">
<td style="background-color: #0056b3; border: none; border-radius: 6px 0 0 6px; padding: 10px 20px;">
<a href="README.md" style="color: #ffffff; text-decoration: none; font-weight: bold; font-family: -apple-system,BlinkMacSystemFont,Segoe UI,Helvetica,Arial,sans-serif; font-size: 14px;">🇬🇧 English</a>
</td>
<td style="background-color: #2c2c2c; border: none; padding: 10px 20px;">
<a href="README_ru.md" style="color: #ffffff; text-decoration: none; font-weight: bold; font-family: -apple-system,BlinkMacSystemFont,Segoe UI,Helvetica,Arial,sans-serif; font-size: 14px;">🇷🇺 Русский</a>
</td>
<td style="background-color: #2c2c2c; border: none; border-radius: 0 6px 6px 0; padding: 10px 20px;">
<a href="README_zh.md" style="color: #ffffff; text-decoration: none; font-weight: bold; font-family: -apple-system,BlinkMacSystemFont,Segoe UI,Helvetica,Arial,sans-serif; font-size: 14px;">🇨🇳 中文</a>
</td>
</tr>
</table>
```text
┌────────────────────────────────────────────────────────┐
│  ███████╗██████╗ ███╗   ███╗    ██████╗  █████╗ ███████╗│
│  ██╔════╝██╔══██╗████╗ ████║    ██╔══██╗██╔══██╗██╔════╝│
│  █████╗  ██║  ██║██╔████╔██║    ██████╔╝███████║███████╗│
│  ██╔══╝  ██║  ██║██║╚██╔╝██║    ██╔══██╗██╔══██║╚════██║│
│  ███████╗██████╔╝██║ ╚═╝ ██║    ██████╔╝██║  ██║███████║│
│  ╚══════╝╚═════╝ ╚═╝     ╚═╝    ╚═════╝ ╚═╝  ╚═╝╚══════╝│
└────────────────────────────────────────────────────────┘

```
# 🪐 EDM Data Base // SECRET FILES
**A high-performance, fully offline, self-hosted file vault with an immersive Brutalist/Hacker Web UI & CLI Console.**
License: MIT

Python 3.8+

Flask

</div>
<p align="center">
<img src="assets/web_preview.png" alt="EDM Database Web Interface" width="100%" style="border-radius: 8px; border: 2px solid #222; box-shadow: 0 4px 20px rgba(0,0,0,0.15);">
</p>
## ⚡ Key Highlights
 * **📴 Zero-Dependency Frontend** — Completely independent of external CDNs, Google Fonts, or cloud-hosted scripts. The entire frontend resides within a single, optimized offline-friendly HTML document.
 * **🕹️ Tactical CLI Console** — Manage user authentication, specify file vault paths, monitor server runtime statuses, and initiate the Flask environment inside a highly customized terminal shell.
 * **🪐 Brutalist & Cyberpunk Aesthetic** — Immersive cyber-style layouts with Light, Dark, and Hacker (Matrix-green) theme configurations. Supports custom accents, adjustable borders, custom radius sizes, and haptic feedback.
 * **🎬 Native Media Processing** — Real-time media streaming with built-in multi-format video/audio players, image pinch-zoom overlays, and an interactive markdown/text log editing pane.
 * **👁️ Dynamic Path Camouflage** — Seamlessly hide or unhide your storage folder from native Android/Linux file systems (using instant dot-prefixing .) at the touch of a button.
## 📸 Console Layout
<p align="center">
<img src="assets/terminal_preview.png" alt="Terminal UI Console Panel" width="80%" style="border-radius: 8px; border: 2px solid #222; box-shadow: 0 4px 20px rgba(0,0,0,0.15);">
</p>
## 🚀 Installation & Setup
### 📦 1. Clone the repository
Clone the repository recursively to fetch all assets and configurations:
```bash
git clone [https://github.com/YOUR_USERNAME/edm-database.git](https://github.com/YOUR_USERNAME/edm-database.git)
cd edm-database

```
### 📦 2. Configure Environment
Install Python's lightweight micro-framework (Flask is the only runtime dependency):
```bash
pip install flask

```
### 📦 3. Fire up the Console
Execute the integrated terminal manager to configure your secure environment:
```bash
python server.py

```
## 🕹️ CLI Console Guide
Upon launching server.py, the administrative console provides a visual control frame:
```text
/------------------------------------------------------------\
|   _____  _____  __  __      /---------------------------\  |
|  |  ___||  _  \|  \/  |     | СТАТУС : [ОФФЛАЙН  ]      |  |
|  | |__  | | | || \  / |     | ПОРТ   : 5000             |  |
|  |  __| | | | || |\/| |     | АДМИНЫ : 1                |  |
|  | |___ | |_| || |  | |     | ПАПКА  : /storage/emul... |  |
|  |_____||_____/|_|  |_|     \---------------------------/  |
\------------------------------------------------------------/
|~ /_> MAIN MENU
--------------------------------------------------------------
|_ [ 1 ] START SERVER
|_ [ 2 ] USER ACCOUNTS
|_ [ 3 ] VAULT CONFIGURATION
|_ [ 4 ] STATS & LOGS
|_ [ 0 ] TERMINATE

```
### Operations Map:
 1. **Start Server:** Triggers a synchronized daemon thread that launches Flask, keeping the CLI shell active.
 2. **User Accounts:** Easily modify access credentials, remove administrator nodes, and register new accounts.
 3. **Vault Configuration:** Define the exact folder path used to read and write your secure data structures.
 4. **Stats & Logs:** View real-time folder footprint metrics, file counts, and overall storage weight.
## 🛠️ Interface Controls
 * **Uploading:** Seamlessly drag-and-drop media elements or tap standard upload interfaces.
 * **Context Interaction:** Perform a **long-press** or tap the triple-dot ⋮ button on any folder index to trigger administrative parameters (Rename, Edit Tags, Delete, Toggle Favorites).
 * **Automatic Preservation:** Activate Autosave in the Settings panel to preserve textual edits locally on a debounced timeline.
## 📝 License
This project is licensed under the MIT License.
