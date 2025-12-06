# Environment Configuration

## Overview
Environment configuration has been set up for both backend and frontend to manage sensitive data and environment-specific settings.

## Backend Configuration

### Files Created
- **`.env`** - Contains actual environment variables (not committed to git)
- **`.env.example`** - Template file with example values
- **`.gitignore`** - Updated to exclude `.env` files

### Environment Variables

```bash
# MongoDB Configuration
MONGO_URL=mongodb://localhost:27017
DB_NAME=kevin_assignment_db

# Server Configuration
PORT=8000
API_PREFIX=/rent-easy/api

# Environment
ENVIRONMENT=development
```

### Installation Required

**Install python-dotenv package:**
```bash
pip3 install python-dotenv
```

Or add to `requirements.txt`:
```
python-dotenv==1.0.0
```

### Usage
The `src/config/config.py` file now loads environment variables automatically:
```python
from dotenv import load_dotenv
load_dotenv()

mongo_url = os.getenv("MONGO_URL", "mongodb://localhost:27017")
db_name = os.getenv("DB_NAME", "kevin_assignment_db")
```

---

## Frontend Configuration

### Files Created
- **`frontend/.env`** - Contains actual environment variables (not committed to git)
- **`frontend/.env.example`** - Template file with example values
- **`frontend/.gitignore`** - Updated to exclude `.env` files

### Environment Variables

```bash
# API Configuration
VITE_API_BASE_URL=http://localhost:8000/rent-easy/api

# Application Configuration
VITE_APP_TITLE=Student-Teacher Management System
```

> **Note:** Vite requires environment variables to be prefixed with `VITE_` to be exposed to the client.

### Usage
The `frontend/src/services/api.js` file now reads from environment variables:
```javascript
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/rent-easy/api';
```

---

## Setup Instructions

### For New Developers

1. **Backend Setup:**
   ```bash
   # Copy the example file
   cp .env.example .env
   
   # Edit .env with your actual values
   nano .env
   
   # Install python-dotenv
   pip3 install python-dotenv
   ```

2. **Frontend Setup:**
   ```bash
   cd frontend
   
   # Copy the example file
   cp .env.example .env
   
   # Edit .env with your actual values (if different from defaults)
   nano .env
   ```

3. **Restart Services:**
   ```bash
   # Backend
   fastapi dev main.py
   
   # Frontend
   cd frontend && npm run dev
   ```

---

## Security Notes

- ✅ `.env` files are excluded from git via `.gitignore`
- ✅ `.env.example` files are committed to provide templates
- ⚠️ Never commit actual `.env` files with sensitive data
- ⚠️ Update `.env.example` when adding new environment variables

---

## Environment-Specific Configuration

### Development
Use the default `.env` file with localhost settings.

### Production
Update `.env` with production values:
```bash
MONGO_URL=mongodb://production-server:27017
DB_NAME=production_db
ENVIRONMENT=production
VITE_API_BASE_URL=https://api.yourdomain.com/rent-easy/api
```

### Staging
Create a separate `.env.staging` file if needed.
