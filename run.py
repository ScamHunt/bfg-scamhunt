from bot.bot import main
from api import app
import logging
import uvicorn
import threading

logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO
)

# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

def run_api():
    """Run the FastAPI server in a separate thread"""
    uvicorn.run(app, host="0.0.0.0", port=8000)

def run_bot():
    """Run the Telegram bot in the main thread"""
    main()

if __name__ == "__main__":
    # Start API server in a separate thread
    api_thread = threading.Thread(target=run_api, daemon=True)
    api_thread.start()
    
    # Run bot in main thread
    run_bot()
