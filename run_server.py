from server import app
from fastapi.middleware.cors import CORSMiddleware
#uvicorn run_server:app --reload
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)