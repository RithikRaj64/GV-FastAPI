from pyngrok import ngrok
import uvicorn

# Path to your FastAPI app file
app_path = "main:app"

# Start ngrok and create a tunnel to your FastAPI app
public_url = ngrok.connect(addr="8000")

print(public_url)

# Start FastAPI using Uvicorn with the ngrok tunnel as the host
uvicorn.run(app_path, host="localhost", port=8000)
