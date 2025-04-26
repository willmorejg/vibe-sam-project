# VIBE-SAM Project

A comprehensive management system for components and systems using FastAPI and Nuxt.js.

## Project Structure

- `/app` - FastAPI backend
- `/frontend` - Nuxt.js frontend with TypeScript

## Setup Instructions

### Backend

1. Install dependencies:
   ```
   pip install fastapi uvicorn pydantic python-multipart
   ```

2. Run the backend server:
   ```
   python -m app.main
   ```

### Frontend

1. Navigate to the frontend directory:
   ```
   cd frontend
   ```

2. Install dependencies:
   ```
   npm install
   ```

3. For development:
   ```
   npm run dev
   ```

4. For production build:
   ```
   npm run build
   npm run generate
   ```

## Complete Setup Sequence

For a full setup from scratch:

```bash
# Install backend dependencies
pip install fastapi uvicorn pydantic python-multipart

# Build the frontend
cd frontend
npm install
npm run generate
cd ..

# Run the backend (which will serve the frontend)
python -m app.main
```

## Accessing the Application

- API documentation: http://localhost:8000/docs
- Web Interface: http://localhost:8000/ui/
  - Important: Always include the trailing slash in the UI URL!
  - If you see a "Not Found" error, try accessing http://localhost:8000/ui/ (with trailing slash)
- API root: http://localhost:8000/

## Troubleshooting

### "Not Found" Error in Frontend

If you see a "Not Found" error when accessing the frontend:

1. Make sure you're accessing the UI with a trailing slash: http://localhost:8000/ui/
2. Verify the frontend was built correctly with `npm run generate`
3. Check that the FastAPI server is properly serving the frontend directory
4. Clear your browser cache or try in a private/incognito window

### Routing Issues

Client-side routing may not work properly on direct page access. This is because:

1. The SPA (Single Page Application) needs to handle routes on the client side
2. Direct access to routes like `/ui/systems` needs server configuration

Fix this by adding a catch-all route in the FastAPI application or configuring proper redirects.

## Features

- Create, read, update, and delete systems
- Create, read, update, and delete components
- Associate components with systems
- Manage dynamic properties for both systems and components
- Modern responsive UI built with Nuxt.js and Bootstrap

## Development Notes

- The API provides full RESTful endpoints for managing systems and components
- The frontend handles dynamic properties (0 to many) for both systems and components
- When no data is available, appropriate messages are displayed
- Create buttons are always available for adding new items
