from fastapi import FastAPI
from app.api.routes import router
from app.dependencies.database import initialize_database

app = FastAPI(title="ATM System")

# Initialize the database on startup asynchronously
@app.on_event("startup")
async def on_startup():
    await initialize_database()

# Include API routes
app.include_router(router, prefix="/api", tags=["ATM"])

@app.get("/")
def root():
    return {"message": "Welcome to the ATM System"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000)
