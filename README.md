<div align="center"><img src="assets/sCCraper-IT-logo.png" height="100px" alt="sCCraper-IT logo"></div>

<h2 align="center">sCCraper IT</h2>

## ✨ Introduction

**sCCraper IT** is a Python-based tool designed to automate the download of all the available **CTF challenges**, including their metadata and attached files, via the platform APIs. It organizes the retrieved content into a structured, easy-to-navigate folder hierarchy.

## 🌐 Supported Platforms

This tool was designed to work with these platforms:

- <img src="assets/cyberchallenge-logo.png" height="20px" alt="CyberChallenge.IT logo"> [CyberChallenge.IT](https://cyberchallenge.it)
- <img src="assets/olicyber-logo.png" height="20px" alt="Olicyber.IT logo"> [Olicyber.IT](https://training.olicyber.it)

> [!NOTE]  
> Access to the above platforms is required. **sCCraper IT** uses your platform **credentials** to authenticate and retrieve challenge data.

## 🚀 Features

- Login with API token via email/password
- Fetches all challenges in the selected platform
- Downloads all attached files
- Automatically downloads hints (if user is a `SUPERVISOR`)
- Saves everything in a clean folder structure

## ⚙️ Configuration

Update your login credentials and desired base URL in `config.py`:

```python
# Switch Platform
BASE_URL = "https://ctf.cyberchallenge.it"
# BASE_URL = "https://training.olicyber.it"

EMAIL = "your@email.com"
PASSWORD = "your_password"
```

## ✅ Usage

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the script:

```bash
python -m src.main
```

After execution, you’ll find:

- `challenges.json` — metadata of all challenges
- `challenges/` — subfolders with challenge JSON + files

## 📌 TODO

- [ ] CLI support (e.g. `--email`, `--save-to`)
- [ ] Caching to avoid re-downloading
- [ ] Automatic `.env` support
- [ ] Logging (instead of `print()`)
