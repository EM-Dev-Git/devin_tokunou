# devin_tokunou

A FastAPI application with basic API endpoints.

## Features

- RESTful API with FastAPI
- Health check endpoint
- Items management endpoints
- CORS support
- Auto-generated API documentation

## Requirements

- Python 3.12+
- FastAPI
- Uvicorn

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/EM-Dev-Git/devin_tokunou.git
   cd devin_tokunou
   ```

2. Install dependencies:
   ```bash
   pip install fastapi uvicorn
   ```

## Running the Application

Start the FastAPI server:

```bash
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

The API will be available at http://localhost:8000

## API Documentation

FastAPI automatically generates interactive API documentation:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## API Endpoints

- `GET /`: Welcome message
- `GET /health`: Health check
- `GET /items`: List all items
- `GET /items/{item_id}`: Get a specific item
- `POST /items/`: Create a new item
