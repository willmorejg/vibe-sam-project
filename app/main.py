from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.routers import components, systems
import os
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Service API",
    description="API for managing components and systems",
    version="0.1.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the routers
app.include_router(components.router)
app.include_router(systems.router)

# Check if frontend dist directory exists before mounting
frontend_dist_path = "frontend/.output/public"
if os.path.exists(frontend_dist_path) and os.path.isdir(frontend_dist_path):
    app.mount("/ui", StaticFiles(directory=frontend_dist_path, html=True), name="ui")
    logger.info(f"Frontend UI mounted at /ui from {frontend_dist_path}")
else:
    logger.warning(f"Frontend build directory '{frontend_dist_path}' not found. UI will not be available.")
    logger.info("Run 'cd frontend && npm run generate' to create the frontend build.")

@app.get("/")
async def root():
    frontend_status = "available at /ui" if os.path.exists(frontend_dist_path) else "not built yet"
    return {
        "message": "Welcome to the Service API",
        "api_docs": "Visit /docs for the API documentation",
        "frontend": frontend_status
    }

if __name__ == "__main__":
    import uvicorn
    host = "0.0.0.0"
    port = 8000
    logger.info(f"Starting API server on http://{host}:{port}")
    uvicorn.run(app, host=host, port=port)
