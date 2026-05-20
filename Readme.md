# schulmanager-api

A simple REST API that scrapes your timetable from [Schulmanager Online](https://schulmanager-online.de) and returns it as structured JSON.

## How it works

1. Authenticates via JWT stored in `localStorage`
2. Uses Playwright to load the timetable page and trigger Angular rendering
3. Parses the HTML with BeautifulSoup
4. Returns the timetable as JSON via a Flask endpoint

## Requirements

- Python 3.10+
- Google Chrome / Chromium

## Installation

```bash
git clone https://github.com/yourname/schulmanager-api
cd schulmanager-api

python3 -m venv venv
source venv/bin/activate

pip install flask playwright beautifulsoup4 python-dotenv
playwright install chromium
```

## Configuration

Create a `.env` file in the project root:

```env
SECRET_KEY=your_flask_secret_key
```

You get your `jwt` and `user` values from Schulmanager's `localStorage`. Open DevTools in your browser on the Schulmanager page, go to **Application → Local Storage** and copy the `jwt` and `user` values.

## Usage

Start the server:

```bash
python3 app.py
```

Then send a POST request to `/api/table` with your credentials:

```bash
curl -X POST http://localhost:5000/api/table \
  -H "Content-Type: application/json" \
  -d '{"jwt": "your_jwt_token", "user": "your_user_value"}'
```

## Response

```json
{
  "1": {
    "Mo": [{ "subject": "MUS", "teacher": "Sta", "room": "0.04", "cancelled": false }],
    "Di": [],
    "Mi": [{ "subject": "D",   "teacher": "Be",  "room": "0.11", "cancelled": false }]
  },
  "4": {
    "Di": [{ "subject": "PH",  "teacher": "Fi",  "room": "0.09", "cancelled": true }]
  }
}
```

Each period (1–7) contains an entry for each day (Mo–Fr) with a list of lessons. An empty list means a free period. `cancelled: true` means the lesson is cancelled.

## Project Structure

```
schulmanager-api/
├── app.py            # Flask API
├── schulmanager.py   # Scraper + parser
├── .env              # Secrets (not committed)
└── README.md
```

## Notes

- The JWT token expires periodically — you'll need to refresh it from your browser
- `headless=False` is recommended if the timetable fails to load (Angular rendering issue)
- This project is unofficial and not affiliated with Schulmanager Online
