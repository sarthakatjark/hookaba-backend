# hookaba-backend

A production-ready Flask backend for OTP authentication via phone number, using MongoDB and best practices.

## Features
- Flask application factory pattern
- Blueprints for modularity
- Service-layer architecture
- Environment-based configuration
- OTP authentication via phone number (MongoDB)
- Marshmallow for validation
- Logging for OTP events
- Docker-ready

## Setup

1. **Clone the repository**
2. **Create a virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
4. **Create a `.env` file** in the project root with your environment variables (see `app/config.py` for required keys).
5. **(Optional) Add `instance/config.py`** for local sensitive config (not committed).

## Running the App

```bash
export FLASK_APP=run.py
export FLASK_ENV=development  # or production
flask run
```

## Testing

```bash
pytest
```

## Docker

```bash
docker build -t hookaba-backend .
docker run -p 5000:5000 hookaba-backend
```

## Twilio Integration

To enable Twilio for SMS, update `app/common/sms.py` (see comments in file). Do not hardcode secrets; use environment variables. 