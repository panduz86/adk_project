import requests
import subprocess
import time
import os
import signal
import sys
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Start uvicorn server in background
# Note: We redirect output to avoid cluttering the notebook
server_process = subprocess.Popen(
    [
        "uvicorn",
        "wine_cellar.a2a_agents.buy_wine_server:app",  # Module:app format with full path
        "--host",
        "localhost",
        "--port",
        "8001",
    ],
    cwd=os.path.join(os.path.dirname(__file__), "..", ".."),  # Project root
    env={**os.environ},  # Pass environment variables (including GOOGLE_API_KEY)
)

print("🚀 Starting Buy Wine Agent server...")
print("   Waiting for server to be ready...")

# Wait for server to start (poll until it responds)
max_attempts = 30
for attempt in range(max_attempts):
    try:
        response = requests.get(
            "http://localhost:8001/.well-known/agent-card.json", timeout=1
        )
        if response.status_code == 200:
            print(f"\n✅ Buy Wine Agent server is running!")
            print(f"   Server URL: http://localhost:8001")
            print(f"   Agent card: http://localhost:8001/.well-known/agent-card.json")
            break
    except requests.exceptions.RequestException:
        time.sleep(5)
        print(".", end="", flush=True)
else:
    print("\n⚠️  Server may not be ready yet. Check manually if needed.")

# Store the process so we can stop it later
globals()["buy_wine_server_process"] = server_process

# Signal handler to cleanup on Ctrl+C
def cleanup(signum, frame):
    print("\n🛑 Shutting down Buy Wine Agent server...")
    server_process.terminate()
    try:
        server_process.wait(timeout=5)
    except subprocess.TimeoutExpired:
        server_process.kill()
    print("✅ Server stopped.")
    sys.exit(0)

signal.signal(signal.SIGINT, cleanup)
signal.signal(signal.SIGTERM, cleanup)

print("\n💡 Press Ctrl+C to stop the server")

# Keep the script running
try:
    server_process.wait()
except KeyboardInterrupt:
    cleanup(None, None)
