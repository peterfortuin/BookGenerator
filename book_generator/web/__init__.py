from fastapi import FastAPI
from fastapi.responses import HTMLResponse

fast_api = FastAPI()


@fast_api.get("/", response_class=HTMLResponse)
async def read_root():
    return """
    <html>
        <body>
            <img src="/image" alt="Generated Image"><br>
            <button onclick="location.reload()">Refresh</button>
        </body>
    </html>
    """
