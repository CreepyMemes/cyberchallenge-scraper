# sCCraper IT

<p align="center">
  <img src="assets/sCCraper-IT-logo.png" height="200px" alt="sCCraper-IT logo">
</p>

A Python-based scraper for downloading CTF challenges and files from the [CyberChallenge.IT](https://cyberchallenge.it) or [Olicyber.IT](https://training.olicyber.it) platforms using their API.

This tool logs in with your credentials, fetches all available challenges, downloads the metadata and attached files, and organizes everything into a clean folder structure.

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
python main.py
```

After execution, you’ll find:

- `challenges.json` — metadata of all challenges
- `challenges/` — subfolders with challenge JSON + files

## 📌 TODO

- [ ] CLI support (e.g. `--email`, `--save-to`)
- [ ] Caching to avoid re-downloading
- [ ] Automatic `.env` support
- [ ] Logging (instead of `print()`)
