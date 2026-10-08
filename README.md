# SupplySense AI

AI-powered demand forecasting and inventory risk monitoring for supply-chain teams.

## Stack
- Backend: Python + FastAPI
- ML: scikit-learn RandomForestRegressor
- Database: PostgreSQL (Docker)
- Dashboard: React + Vite
- Charts: Recharts

## Features
- SKU-level demand forecasting
- Stockout and overstock alerts
- Inventory health dashboard
- Forecast vs actual visualization
- PostgreSQL persistence
- Demo seed data
- REST API
- Docker Compose for easy startup

## Run
Prerequisites: Docker Desktop and Node.js 18+.

```bash
docker compose up --build
```

Then open:
- Dashboard: http://localhost:5173
- API docs: http://localhost:8000/docs
- Health: http://localhost:8000/health

The backend automatically creates tables and seeds realistic demo data on first start.

## Local development without Docker
Create PostgreSQL yourself, then:

```bash
cd backend
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
set DATABASE_URL=postgresql+psycopg2://postgres:postgres@localhost:5432/supplysense
uvicorn app.main:app --reload
```

For frontend:
```bash
cd frontend
npm install
npm run dev
```
