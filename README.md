![ScamHunt banner](assets/scamhunt/logo-banner.jpeg)

# ScamHunt

Bot name: [@ScamHunt_bot](https://t.me/@ScamHunt_bot)

## Tools

Supabase: https://supabase.com/dashboard/project/iyaldvefunvxxmlrerte
Fly\.io: https://fly.io/apps/scamhunt

## Install

1. Create `.env` file with these values
    ```
    TELEGRAM_BOT_TOKEN=<token>
    OPENAI_API_KEY=<token>
    SUPABASE_KEY=<token>
    ```

2. `python -m venv .venv`

3. `source .venv/bin/activate`

4. `pip install -r requirements.txt`

5. `python run.py`


## Run with Docker

`docker build -t scamhunt .`

`docker run -d -p 8080:8080 scamhunt`

## Deploy

`fly deploy`
