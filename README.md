# 🚀 SupplySense AI

## AI-Powered Demand Forecasting & Inventory Risk Management System

SupplySense AI is a machine-learning-powered supply-chain management system designed to help companies **predict future product demand, identify stockout and overstock risks, and make better inventory decisions**.

The system combines:

- 🐍 Python
- 🤖 Machine Learning
- ⚡ FastAPI
- 🐘 PostgreSQL
- ⚛️ React
- 📊 Recharts
- 🐳 Docker

The goal is simple:

> **Predict what customers will need before inventory problems happen.**

---

# 📌 1. Problem Statement

Supply-chain companies frequently face two major inventory problems:

### 🔴 Stockout

A company does not have enough inventory to satisfy future demand.

This can result in:

- Lost sales
- Customer dissatisfaction
- Delayed orders
- Emergency purchasing
- Loss of customer trust

### 🟠 Overstock

A company purchases or stores more inventory than it actually needs.

This can result in:

- Capital being locked in inventory
- Higher warehouse costs
- Increased storage requirements
- Product obsolescence
- Reduced cash flow

Traditional inventory management often depends on:

- Manual calculations
- Fixed reorder levels
- Historical averages
- Human intuition
- Spreadsheet-based analysis

These approaches may not react quickly enough to changing demand.

---

# 💡 2. Our Solution

SupplySense AI uses historical sales data and machine learning to estimate future demand.

The system analyzes:

- Previous sales
- Day of the week
- Recent demand
- Weekly demand patterns
- Short-term trends
- Medium-term trends

It then generates a future demand forecast.

The forecast is compared with the company's current inventory and supplier lead time.

SupplySense AI can then identify whether a product is:

### 🟢 HEALTHY

Inventory is currently within a reasonable operating range.

### 🟡 LOW STOCK

Inventory is approaching a critical level.

### 🔴 STOCKOUT RISK

Predicted demand may exceed available inventory before the next replenishment arrives.

### 🟠 OVERSTOCK RISK

Inventory is significantly higher than expected demand.

---

# 🎯 3. Main Objectives

SupplySense AI aims to:

1. Predict future product demand.
2. Reduce stockout situations.
3. Identify unnecessary excess inventory.
4. Provide inventory risk alerts.
5. Recommend approximate reorder quantities.
6. Give supply-chain managers a centralized dashboard.
7. Store inventory and sales data in PostgreSQL.
8. Provide APIs for future integration with ERP/e-commerce systems.
9. Make inventory decisions data-driven rather than completely manual.

---

# 🧠 4. Machine Learning

## ML Model

SupplySense AI currently uses:

```text
Random Forest Regressor
```

from:

```text
scikit-learn
```

Random Forest is useful for this type of prototype because it can model nonlinear relationships between historical demand patterns and future demand.

---

# 📊 5. Features Used by the Model

The forecasting model creates several features from historical sales.

### Day of Week

```text
Monday
Tuesday
Wednesday
...
Sunday
```

This helps the model learn weekly demand patterns.

---

### Lag 1

Previous day's sales.

Example:

```text
Yesterday = 20 units
```

The model can use this information when predicting today/tomorrow.

---

### Lag 7

Sales from seven days ago.

This helps identify weekly patterns.

Example:

```text
Last Monday = 35
Current Monday forecast can use this information.
```

---

### Lag 14

Sales from fourteen days ago.

This provides additional historical context.

---

### Rolling 7-Day Average

Average demand over the previous seven days.

Example:

```text
10 + 12 + 15 + 11 + 14 + 13 + 16
```

The model calculates the average to understand recent demand.

---

### Rolling 14-Day Average

Average demand over the previous fourteen days.

This helps smooth short-term fluctuations.

---

### Trend

The system also includes a time-based feature that allows the model to learn gradual changes in demand.

---

# 🔮 6. Forecasting Process

The forecasting process works approximately like this:

```text
Historical Sales
       ↓
Data Cleaning
       ↓
Feature Engineering
       ↓
Lag Features
       ↓
Rolling Averages
       ↓
Random Forest Model
       ↓
Future Demand Prediction
       ↓
Inventory Risk Analysis
       ↓
Dashboard Alert
```

---

# 📅 7. Forecast Horizon

The dashboard currently generates a:

```text
14-Day Forecast
```

The API supports forecasts from:

```text
1 → 60 days
```

Example:

```text
GET /api/forecast/SKU-1001?horizon=14
```

---

# 📦 8. Inventory Risk Detection

After demand is predicted, SupplySense AI compares forecasted demand with available inventory.

For example:

```text
Current Inventory = 50 units

Expected demand during supplier lead time = 65 units
```

The system identifies:

```text
Potential Stockout
```

because:

```text
50 - 65 = -15
```

The company could potentially be short by approximately:

```text
15 units
```

---

# 🚨 9. Stockout Detection

Stockout risk occurs when predicted demand during supplier lead time exceeds current inventory.

Conceptually:

```text
Projected Inventory =
Current Stock - Expected Lead-Time Demand
```

If:

```text
Projected Inventory < 0
```

then:

```text
STOCKOUT RISK
```

---

# 📦 10. Overstock Detection

The system also looks for unusually high inventory.

If projected inventory is substantially higher than the product's reorder threshold, SupplySense AI can classify the product as:

```text
OVERSTOCK
```

This helps identify inventory that may be tying up unnecessary capital.

---

# 🛒 11. Reorder Recommendation

SupplySense AI calculates an approximate reorder quantity based on:

- Future demand
- Current inventory
- Reorder point

The goal is to provide a useful starting recommendation for inventory managers.

Example:

```text
Current stock:
20

Expected future demand:
70

Safety/reorder requirement:
15
```

The system may recommend ordering approximately:

```text
65 units
```

The recommendation should be treated as a decision-support estimate rather than an automatic purchase order.

---

# 🗄️ 12. PostgreSQL Database

SupplySense AI uses PostgreSQL to store application data.

The main database tables are:

```text
products
sales_history
forecasts
```

---

## Products Table

Stores information about products.

Example:

```text
SKU
Product Name
Category
Current Stock
Reorder Point
Lead Time
Unit Cost
```

Example:

```text
SKU-1001
Wireless Mouse
Electronics
48 units
35 reorder point
5 days lead time
$18.50
```

---

## Sales History Table

Stores historical product sales.

Example:

```text
Date          SKU          Units Sold

2026-01-01    SKU-1001     12
2026-01-02    SKU-1001     15
2026-01-03    SKU-1001     11
```

This historical data becomes the input for the ML model.

---

## Forecasts Table

Stores generated demand forecasts.

Example:

```text
SKU
Forecast Date
Predicted Demand
```

---

# 🏗️ 13. System Architecture

The overall architecture is:

```text
                    ┌─────────────────────┐
                    │      User           │
                    │ Supply Chain Team   │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   React Dashboard   │
                    │                     │
                    │ Charts              │
                    │ Alerts              │
                    │ Inventory Health     │
                    └──────────┬──────────┘
                               │
                         REST API
                               │
                               ▼
                    ┌─────────────────────┐
                    │       FastAPI       │
                    │                     │
                    │ Products API        │
                    │ Forecast API        │
                    │ Dashboard API       │
                    └──────────┬──────────┘
                               │
              ┌────────────────┴────────────────┐
              │                                 │
              ▼                                 ▼
     ┌─────────────────┐              ┌─────────────────┐
     │ Machine Learning│              │   PostgreSQL    │
     │                 │              │                 │
     │ Random Forest   │              │ Products        │
     │ Forecasting     │              │ Sales History   │
     └─────────────────┘              │ Forecasts       │
                                      └─────────────────┘
```

---

# 📁 14. Project Structure

```text
SupplySense_AI/
│
├── backend/
│   │
│   ├── app/
│   │   ├── __init__.py
│   │   └── main.py
│   │
│   ├── Dockerfile
│   └── requirements.txt
│
├── frontend/
│   │
│   ├── src/
│   │   ├── main.jsx
│   │   └── styles.css
│   │
│   ├── index.html
│   ├── package.json
│   └── vite.config.js
│
├── data/
│   └── sample_sales.csv
│
├── docker-compose.yml
│
└── README.md
```

---

# 🐍 15. Backend

The backend is built using:

```text
Python
FastAPI
SQLAlchemy
PostgreSQL
Pandas
NumPy
Scikit-learn
```

The backend is responsible for:

- Database communication
- Machine-learning forecasting
- Inventory analysis
- Risk calculation
- API endpoints
- Product management
- Dashboard data

---

# ⚡ 16. FastAPI

FastAPI provides the REST API layer.

Important endpoints include:

### Health Check

```http
GET /health
```

Returns:

```json
{
  "status": "ok",
  "service": "SupplySense AI"
}
```

---

### Get Products

```http
GET /api/products
```

Returns all tracked products.

---

### Dashboard

```http
GET /api/dashboard
```

Returns:

- Total SKUs
- Stockout risks
- Overstock risks
- Healthy inventory
- Inventory value
- Inventory alerts

---

### Forecast

```http
GET /api/forecast/{sku}
```

Example:

```http
GET /api/forecast/SKU-1001?horizon=14
```

Returns the future demand prediction.

---

### Retrain / Refresh

```http
POST /api/retrain
```

Refreshes the forecasting process for all products.

---

# 📊 17. Dashboard

The React dashboard provides a visual interface for supply-chain managers.

The dashboard contains:

### KPI Cards

```text
Total SKUs
Stockout Risk
Overstock Risk
Inventory Value
```

---

### Demand Forecast Chart

The user can select a SKU and see the predicted demand for the next 14 days.

Example:

```text
Demand
  │
20│       ╭──╮
  │   ╭───╯  ╰──╮
10│───╯         ╰───
  │
  └──────────────────
       Future Days
```

---

### Inventory Alerts

The dashboard highlights products requiring attention.

Example:

```text
🔴 SKU-1003
USB-C Hub

STOCKOUT

Projected shortage of 20 units.
Recommended order: 75 units.
```

---

### Inventory Health Table

The table provides:

```text
SKU
Product
Current Stock
Average Daily Demand
Lead-Time Projection
Status
Recommended Order
```

---

# 🎨 18. Frontend Technologies

The dashboard uses:

```text
React
Vite
Recharts
CSS
```

React handles the user interface.

Vite provides the development environment.

Recharts displays the forecasting graphs.

---

# 🐳 19. Docker

The project includes Docker Compose so the entire application can run without manually configuring PostgreSQL.

The system contains three containers:

```text
PostgreSQL
     │
     ▼
FastAPI Backend
     │
     ▼
React Frontend
```

---

# ⚙️ 20. Requirements

Before running the project, install:

### Required

- Docker Desktop
- VS Code

Docker Desktop includes:

```text
Docker
Docker Compose
```

For optional local frontend development:

```text
Node.js 18+
```

---

# 🚀 21. Running the Project

## Step 1 — Extract the Project

Extract:

```text
SupplySense_AI.zip
```

Open the extracted folder in VS Code.

---

## Step 2 — Open Terminal

In VS Code:

```text
Terminal → New Terminal
```

---

## Step 3 — Start the Application

Run:

```bash
docker compose up --build
```

The first startup may take several minutes because Docker needs to download images and install dependencies.

---

# 🌐 22. Open the Application

After the containers start successfully:

### Dashboard

```text
http://localhost:5173
```

### Backend

```text
http://localhost:8000
```

### API Documentation

```text
http://localhost:8000/docs
```

The `/docs` page provides an interactive Swagger interface where you can test the APIs.

---

# 🧪 23. Demo Data

The application automatically generates realistic demo sales data when the database is empty.

The generated data contains:

```text
8 Products
181 Days of Sales History
Multiple Categories
Different Demand Patterns
Different Inventory Levels
Different Supplier Lead Times
```

This allows the project to work immediately without requiring a real company database.

---

# 🔄 24. Application Workflow

When the application starts:

```text
1. PostgreSQL starts
        ↓
2. FastAPI connects to PostgreSQL
        ↓
3. Database tables are created
        ↓
4. Demo products are inserted
        ↓
5. Historical sales are generated
        ↓
6. Dashboard requests inventory data
        ↓
7. ML model analyzes sales history
        ↓
8. Future demand is predicted
        ↓
9. Inventory risk is calculated
        ↓
10. Dashboard displays results
```

---

# 🧠 25. Example Business Scenario

Suppose a company sells wireless mice.

Historical sales:

```text
Monday       15
Tuesday      18
Wednesday    16
Thursday     20
Friday       23
Saturday     12
Sunday       10
```

Current inventory:

```text
48 units
```

Supplier lead time:

```text
5 days
```

The ML model predicts:

```text
Next 5 days:

21
22
24
20
23
```

Total expected demand:

```text
110 units
```

Current stock:

```text
48 units
```

Therefore:

```text
48 - 110 = -62
```

The system identifies:

```text
🔴 STOCKOUT RISK
```

The dashboard alerts the supply-chain manager before the shortage happens.

---

# 📈 26. Why Machine Learning?

A simple average might calculate:

```text
Average demand = 15 units/day
```

But demand can change because of:

- Weekly patterns
- Growth
- Recent demand spikes
- Seasonal behavior
- Promotions
- Customer behavior

Machine learning allows the system to consider multiple historical signals instead of relying only on a single average.

---

# ⚠️ 27. Important Limitation

This is a functional **MVP / prototype**, not a production-grade enterprise forecasting platform.

Real-world demand forecasting can also require:

- Promotions
- Holidays
- Pricing
- Weather
- Marketing campaigns
- Supplier delays
- Competitor pricing
- Economic conditions
- Regional demand
- Product lifecycle
- External events

These can be added later.

The current model should therefore be presented as:

> **An AI-powered decision-support system for demand forecasting and inventory risk detection.**

Not as a system that guarantees exact future demand.

---

# 🔐 28. Security Considerations

For production deployment, add:

- Authentication
- Role-based access control
- HTTPS
- Environment variables for secrets
- Database encryption
- API rate limiting
- Audit logs
- Input validation
- Secure CORS configuration

The current Docker configuration uses demo credentials:

```text
Username: postgres
Password: postgres
```

These credentials are intended only for local development.

---

# 🚀 29. Future Improvements

SupplySense AI can be extended significantly.

## Advanced ML

Possible models:

```text
XGBoost
LightGBM
Prophet
LSTM
Temporal Fusion Transformer
```

---

## External Factors

Add:

```text
Weather
Holidays
Promotions
Marketing Campaigns
Price Changes
Regional Demand
Economic Indicators
```

---

## Advanced Inventory Optimization

Add:

```text
Safety Stock Optimization
Economic Order Quantity
Service Level Optimization
Supplier Performance
Purchase Order Generation
```

---

## Real-Time Data

Integrate with:

```text
ERP
Warehouse Management System
E-commerce Platform
POS System
Supplier APIs
```

---

# 🏆 30. Competition / Hackathon Value

SupplySense AI is designed around a clear business problem:

```text
Demand Uncertainty
        ↓
Inventory Risk
        ↓
Financial Loss
```

The system attempts to break this cycle using:

```text
Historical Data
      +
Machine Learning
      +
Inventory Intelligence
      +
Actionable Alerts
```

Instead of only showing a forecast, SupplySense AI converts the prediction into an operational decision:

```text
"What will demand be?"
          ↓
"Will inventory be sufficient?"
          ↓
"Is there a stockout/overstock risk?"
          ↓
"How much should we consider ordering?"
```

This makes the project more useful than a simple ML prediction demo.

---

# 📋 31. Technology Stack

| Layer | Technology |
|---|---|
| Frontend | React |
| Build Tool | Vite |
| Charts | Recharts |
| Backend | FastAPI |
| Language | Python |
| ML | Scikit-learn |
| Data Processing | Pandas |
| Numerical Computing | NumPy |
| ORM | SQLAlchemy |
| Database | PostgreSQL |
| Containerization | Docker |
| API Documentation | Swagger / OpenAPI |

---

# 🧩 32. Quick Commands

Start:

```bash
docker compose up --build
```

Start in background:

```bash
docker compose up --build -d
```

Stop:

```bash
docker compose down
```

Stop and delete database volume:

```bash
docker compose down -v
```

View logs:

```bash
docker compose logs
```

Backend logs:

```bash
docker compose logs backend
```

Frontend logs:

```bash
docker compose logs frontend
```

---

# 🛠️ 33. Troubleshooting

## Port 5432 already in use

Another PostgreSQL installation may already be running.

Stop the existing PostgreSQL service or change the port mapping in:

```text
docker-compose.yml
```

---

## Port 8000 already in use

Change:

```yaml
ports:
  - "8000:8000"
```

to something like:

```yaml
ports:
  - "8001:8000"
```

Then update the frontend API URL if necessary.

---

## Port 5173 already in use

Change:

```yaml
ports:
  - "5173:5173"
```

to another available port.

---

## Rebuild Everything

If something becomes inconsistent:

```bash
docker compose down -v
docker compose up --build
```

⚠️ The `-v` option deletes the PostgreSQL Docker volume and therefore resets the demo database.

---

# 📌 34. API Summary

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/health` | Check application status |
| GET | `/api/products` | Get products |
| GET | `/api/dashboard` | Get dashboard data |
| GET | `/api/forecast/{sku}` | Generate demand forecast |
| POST | `/api/retrain` | Refresh forecasting models |

---

# 🔭 35. Project Vision

SupplySense AI can eventually become a complete supply-chain intelligence platform.

The long-term vision is:

```text
                   SUPPLYSENSE AI
                         │
        ┌────────────────┼────────────────┐
        │                │                │
        ▼                ▼                ▼
 Demand Forecast    Inventory Risk    Supplier Risk
        │                │                │
        └────────────────┼────────────────┘
                         ▼
                Inventory Optimization
                         │
                         ▼
                 Purchase Recommendation
                         │
                         ▼
                  Business Decision
```

The ultimate goal is to help organizations move from:

```text
Reactive Inventory Management
```

to:

```text
Predictive Inventory Management
```

---

# 👨‍💻 36. Developer Notes

This project is structured so that additional modules can be added without replacing the existing architecture.

Potential future modules:

```text
authentication/
analytics/
forecasting/
inventory/
suppliers/
notifications/
reports/
```

Possible notification integrations:

```text
Email
SMS
Slack
WhatsApp
Microsoft Teams
```

---

# 📜 37. License

This project is intended as an educational, prototype, and hackathon project.

Modify and extend it according to your project requirements.

---

# ⭐ SupplySense AI

### Predict demand. Prevent stockouts. Reduce overstock. Make smarter inventory decisions.

```text
Historical Data
       ↓
Machine Learning
       ↓
Demand Forecast
       ↓
Inventory Risk
       ↓
Actionable Recommendation
```

**SupplySense AI — Turning supply-chain data into decisions.**
