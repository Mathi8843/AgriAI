# Farmer Profile Management Module

This project contains the Backend and Frontend for the Farmer Profile Management system.

## Structure
- `backend/`: FastAPI application with SQLite database.
- `frontend/`: React Native Expo application.

## Setup & Running

### Backend
1. Navigate to `backend`:
   ```bash
   cd backend
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the server:
   ```bash
   uvicorn main:app --reload --host 0.0.0.0
   ```
   Server runs at `http://0.0.0.0:8000`.

### Frontend
1. Navigate to `frontend`:
   ```bash
   cd frontend
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Start the app:
   ```bash
   npx expo start
   ```
   - Press `a` for Android Emulator.
   - Press `w` for Web.

## Features
- **Farmer Registration**: Form to capture farmer details.
- **NLP Intent Classification**: Chat interface to route user queries (e.g. "recommended crops").
- **Data Persistence**: Postgres/SQLite (backend) and AsyncStorage (frontend for IDs).
