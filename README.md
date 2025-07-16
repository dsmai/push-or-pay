<div align="center">
  <h1>PushOrPay</h1>
  <p><strong>Automated daily coding accountability with LeetCode, GitHub, and Discord notifications.</strong></p>
  <img src="https://img.shields.io/badge/python-3.13-blue" alt="Python 3.13">
  <img src="https://img.shields.io/badge/fastapi-0.116.1-green" alt="FastAPI">
  <img src="https://img.shields.io/badge/supabase-cloud-orange" alt="Supabase">
</div>

---

## 🚀 Overview

PushOrPay is a FastAPI web application that helps you and your team stay accountable for daily coding practice. Register your GitHub and LeetCode usernames, set a daily fine, and let the app track your progress. Miss a day? The app records it and updates the leaderboard. Daily results and fines are posted to Discord automatically.

## Features

- **User Registration:** Sign up with your name, GitHub, and LeetCode usernames, and set your daily fine amount.
- **Automated Daily Checks:** Scheduler verifies your GitHub commits and LeetCode submissions every midnight (PST).
- **Leaderboard:** See who’s keeping up and who’s paying the most fines.
- **Discord Notifications:** Daily summary and leaderboard sent to your Discord channel.
- **Supabase Integration:** All data stored securely in Supabase.

## 🛠️ Tech Stack

- Python 3.13
- FastAPI
- Supabase (PostgreSQL)
- APScheduler
- Jinja2 & Tailwind CSS (for frontend)
- Discord Webhook

## 📦 Setup & Installation

1. **Clone the repo:**
   ```bash
   git clone https://github.com/dsmai/push-or-pay.git
   cd push-or-pay
   ```
2. **Install dependencies:**
   ```bash
   poetry install
   ```
3. **Configure environment:**
   - Copy `.env.example` to `.env` and fill in your Supabase and Discord credentials.
4. **Run the app:**
   ```bash
   PYTHONPATH=src poetry run uvicorn pushorpay.main:app --reload
   # Or use: make dev
   ```
5. **Access the frontend:**
   - Registration: [http://localhost:8000/](http://localhost:8000/)
   - Leaderboard: [http://localhost:8000/leaderboard](http://localhost:8000/leaderboard)

## 📝 Usage

1. Register yourself and your teammates.
2. The scheduler will check your coding activity every day at midnight PST.
3. View the leaderboard to see fines and rankings.
4. Check Discord for daily summaries.

## 🗄️ Project Structure

```
pushorpay/
├── src/
│   └── pushorpay/
│       ├── main.py           # FastAPI entry point
│       ├── db.py             # Supabase client setup
│       ├── checker.py        # GitHub/LeetCode activity checkers
│       ├── scheduler.py      # Daily job logic
│       ├── notifier.py       # Discord notifications
│       ├── utils/            # Shared utilities
│       └── templates/        # Jinja2 HTML templates
├── .env                      # Secrets (not committed)
├── pyproject.toml            # Poetry config
├── Makefile                  # Dev commands
└── README.md                 # Project info
```

## 🤝 Contributing

Pull requests and issues are welcome! Please open an issue to discuss major changes before submitting a PR.

## 📄 License

MIT License. See [LICENSE](LICENSE) for details.

---

<div align="center">
  <sub>Made with ❤️ by dsmai</sub>
</div>
