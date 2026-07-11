<table align="center">
  <tr>
    <td bgcolor="#444444" align="center"><a href="README.md" style="color: #ffffff; text-decoration: none; font-weight: bold; padding: 4px 8px;">&nbsp;LANG: 🇬🇧 English&nbsp;</a></td>
    <td bgcolor="#0056b3" align="center"><a href="README_ru.md" style="color: #ffffff; text-decoration: none; font-weight: bold; padding: 4px 8px;">&nbsp;LANG: 🇷🇺 Русский&nbsp;</a></td>
    <td bgcolor="#cc0000" align="center"><a href="README_zh.md" style="color: #ffffff; text-decoration: none; font-weight: bold; padding: 4px 8px;">&nbsp;LANG: 🇨🇳 中文&nbsp;</a></td>
  </tr>
</table>

<br>

# EDM Data Base // SECRET FILES
**A fully offline, self-hosted file vault with a Brutalist/Hacker UI.**
License: MIT

Python 3.8+

Flask

</div>
<div align="center">
</div>
## 🪐 About The Project
**EDM Data Base** is a lightweight, zero-dependency (frontend-wise) secret file server and vault. It allows you to host your files locally (e.g., on an Android device via Termux, a Raspberry Pi, or any PC) and access them securely through a sleek, customizable Web UI.
All settings, accounts, and server operations are managed through an integrated **CLI Admin Console** right in your terminal.
### ✨ Features
 * **Completely Offline Frontend:** No external CDNs, Google Fonts, or external assets. Everything is bundled.
 * **Integrated CLI Console:** Start the server, manage accounts, and monitor stats directly from a beautifully crafted terminal UI.
 * **Adaptive Web UI:** Brutalist/Hacker design, themes (Light, Dark, Matrix), customizable shapes, colors, and haptics.
 * **Media Support:** Built-in viewer for images, video player, and a text/code editor directly in the browser.
 * **Hide/Unhide Vault:** Instantly prepend a dot (.) to your vault folder to hide it from native file managers, controlled via the UI or CLI.
 * **Mobile First:** Perfect for running on Termux (Android) and accessing via your phone's browser.
<div align="center">
</div>
## 🚀 Getting Started (Installation)
### Prerequisites
 * **Python 3.8+** installed on your system.
 * (Optional) **Termux** if you are running this on Android.
### 1. Clone the repository
Open your terminal and run the following commands:
```bash
git clone [https://github.com/YOUR_USERNAME/edm-database.git](https://github.com/YOUR_USERNAME/edm-database.git)
cd edm-database

```
### 2. Install dependencies
Install the required Python packages (only Flask is required):
```bash
pip install -r requirements.txt

```
*(If you don't have a requirements.txt, simply run: pip install flask)*
### 3. Run the Server / Admin Console
Start the integrated management console:
```bash
python server.py

```
From the terminal menu, you can:
 1. Create a secure vault path.
 2. Setup your login ID and KEY.
 3. Press [1] to boot the Flask server.
 4. Open the provided Local IP in your browser (e.g., http://192.168.1.X:5000).
## 🛠️ Usage
 * **Upload:** Drag & drop or use the + FILE / UPLOAD buttons.
 * **Context Menu:** Tap the ⋮ icon or long-press any folder card to Rename, Tag, or Delete files.
 * **Settings:** Access the settings panel to change themes (Dark/Light/Hacker), toggle Autosave, or adjust border radius.
## 🤝 Contributing
Contributions, issues, and feature requests are welcome!
Feel free to check the issues page.
## 📝 License
This project is MIT licensed.
