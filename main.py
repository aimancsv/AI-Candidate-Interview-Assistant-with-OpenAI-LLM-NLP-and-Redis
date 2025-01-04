from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from company_routes import router as company_router
from interview_routes import router as interview_router
from audio_routes import router as audio_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(company_router)
app.include_router(interview_router)
app.include_router(audio_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
