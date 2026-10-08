import os
from datetime import date, timedelta
from math import ceil
import numpy as np
import pandas as pd
from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, Integer, String, Float, Date, ForeignKey, text
from sqlalchemy.orm import declarative_base, sessionmaker, Session, relationship
from sklearn.ensemble import RandomForestRegressor
from pydantic import BaseModel

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg2://postgres:postgres@localhost:5432/supplysense"
)
engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True)
    sku = Column(String(50), unique=True, nullable=False)
    name = Column(String(150), nullable=False)
    category = Column(String(80), nullable=False)
    current_stock = Column(Integer, nullable=False)
    reorder_point = Column(Integer, nullable=False)
    lead_time_days = Column(Integer, nullable=False)
    unit_cost = Column(Float, nullable=False)
    history = relationship("SalesHistory", back_populates="product", cascade="all, delete-orphan")

class SalesHistory(Base):
    __tablename__ = "sales_history"
    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    sales_date = Column(Date, nullable=False)
    units_sold = Column(Integer, nullable=False)
    product = relationship("Product", back_populates="history")

class Forecast(Base):
    __tablename__ = "forecasts"
    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    forecast_date = Column(Date, nullable=False)
    predicted_demand = Column(Float, nullable=False)

class ProductOut(BaseModel):
    sku: str
    name: str
    category: str
    current_stock: int
    reorder_point: int
    lead_time_days: int
    unit_cost: float

app = FastAPI(title="SupplySense AI", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def seed_database(db: Session):
    if db.query(Product).count() > 0:
        return
    products = [
        ("SKU-1001","Wireless Mouse","Electronics",48,35,5,18.5),
        ("SKU-1002","Mechanical Keyboard","Electronics",92,45,7,54.0),
        ("SKU-1003","USB-C Hub","Electronics",14,28,6,31.0),
        ("SKU-1004","Laptop Stand","Accessories",160,55,8,42.0),
        ("SKU-1005","Noise Cancelling Headphones","Electronics",22,30,10,89.0),
        ("SKU-1006","Webcam 1080p","Electronics",67,40,6,49.0),
        ("SKU-1007","Desk Mat","Accessories",210,70,4,15.0),
        ("SKU-1008","Power Bank","Electronics",19,34,8,36.0),
    ]
    rng = np.random.default_rng(42)
    start = date.today() - timedelta(days=180)
    for i, p in enumerate(products):
        product = Product(
            sku=p[0], name=p[1], category=p[2], current_stock=p[3],
            reorder_point=p[4], lead_time_days=p[5], unit_cost=p[6]
        )
        db.add(product)
        db.flush()
        base = [11, 8, 7, 5, 9, 7, 6, 10][i]
        trend = [0.015,0.01,0.02,-0.005,0.018,0.01,-0.002,0.02][i]
        weekly = [2,3,2,1,4,2,1,3][i]
        for d in range(181):
            dt = start + timedelta(days=d)
            dow = dt.weekday()
            season = weekly if dow in (0,1,2) else -1
            noise = rng.normal(0, max(1, base*0.18))
            units = max(0, int(round(base + base*trend*d + season + noise)))
            db.add(SalesHistory(product_id=product.id, sales_date=dt, units_sold=units))
    db.commit()

def train_forecast(db: Session, product: Product, horizon: int = 14):
    rows = db.query(SalesHistory).filter(
        SalesHistory.product_id == product.id
    ).order_by(SalesHistory.sales_date).all()
    if len(rows) < 30:
        return []
    df = pd.DataFrame([{"date": r.sales_date, "sales": r.units_sold} for r in rows])
    df["dow"] = pd.to_datetime(df["date"]).dt.dayofweek
    df["day_num"] = np.arange(len(df))
    for lag in [1, 7, 14]:
        df[f"lag_{lag}"] = df["sales"].shift(lag)
    df["rolling_7"] = df["sales"].shift(1).rolling(7).mean()
    df["rolling_14"] = df["sales"].shift(1).rolling(14).mean()
    train = df.dropna()
    features = ["dow","day_num","lag_1","lag_7","lag_14","rolling_7","rolling_14"]
    model = RandomForestRegressor(n_estimators=250, random_state=42, min_samples_leaf=2)
    model.fit(train[features], train["sales"])

    work = df.copy()
    predictions = []
    for _ in range(horizon):
        next_date = pd.to_datetime(work["date"].iloc[-1]) + pd.Timedelta(days=1)
        next_dow = next_date.dayofweek
        vals = list(work["sales"].astype(float))
        def lag(n): return vals[-n] if len(vals) >= n else float(np.mean(vals[-7:]))
        row = pd.DataFrame([{
            "dow": next_dow, "day_num": len(work),
            "lag_1": lag(1), "lag_7": lag(7), "lag_14": lag(14),
            "rolling_7": np.mean(vals[-7:]), "rolling_14": np.mean(vals[-14:])
        }])
        pred = max(0, float(model.predict(row[features])[0]))
        predictions.append({"date": next_date.date(), "predicted_demand": round(pred, 2)})
        work = pd.concat([work, pd.DataFrame([{"date": next_date.date(), "sales": pred}])], ignore_index=True)
    return predictions

def risk_for(product, forecast):
    total = sum(x["predicted_demand"] for x in forecast[:product.lead_time_days])
    avg_daily = total / max(1, product.lead_time_days)
    projected = product.current_stock - total
    if projected < 0:
        risk = "STOCKOUT"
        severity = "high"
        message = f"Projected shortage of {ceil(abs(projected))} units during lead time."
    elif projected < product.reorder_point * 0.5:
        risk = "LOW STOCK"
        severity = "medium"
        message = "Inventory is approaching a critical level."
    elif projected > product.reorder_point * 2.5:
        risk = "OVERSTOCK"
        severity = "medium"
        message = "Projected inventory is substantially above the reorder threshold."
    else:
        risk = "HEALTHY"
        severity = "low"
        message = "Inventory is within the expected operating range."
    recommended = max(0, ceil(sum(x["predicted_demand"] for x in forecast[:30]) + product.reorder_point - product.current_stock))
    return risk, severity, message, round(avg_daily,2), recommended, round(projected,2)

@app.on_event("startup")
def startup():
    Base.metadata.create_all(engine)
    with SessionLocal() as db:
        seed_database(db)

@app.get("/health")
def health():
    return {"status": "ok", "service": "SupplySense AI"}

@app.get("/api/products")
def products(db: Session = Depends(get_db)):
    return [
        {"sku":p.sku,"name":p.name,"category":p.category,"current_stock":p.current_stock,
         "reorder_point":p.reorder_point,"lead_time_days":p.lead_time_days,"unit_cost":p.unit_cost}
        for p in db.query(Product).order_by(Product.sku).all()
    ]

@app.get("/api/dashboard")
def dashboard(db: Session = Depends(get_db)):
    ps = db.query(Product).all()
    cards = []
    alerts = []
    total_value = 0
    stockout = overstock = healthy = 0
    for p in ps:
        f = train_forecast(db,p,14)
        risk,severity,msg,avg,recommended,projected = risk_for(p,f)
        total_value += p.current_stock*p.unit_cost
        if risk == "STOCKOUT": stockout += 1
        elif risk == "OVERSTOCK": overstock += 1
        else: healthy += 1
        item = {
            "sku":p.sku,"name":p.name,"category":p.category,
            "current_stock":p.current_stock,"risk":risk,"severity":severity,
            "message":msg,"avg_daily_demand":avg,"recommended_order":recommended,
            "projected_after_lead_time":projected
        }
        cards.append(item)
        if risk != "HEALTHY": alerts.append(item)
    return {
        "summary":{"total_skus":len(ps),"stockout_risk":stockout,"overstock_risk":overstock,
                   "healthy":healthy,"inventory_value":round(total_value,2)},
        "alerts":alerts,
        "inventory":cards
    }

@app.get("/api/forecast/{sku}")
def forecast(sku: str, horizon: int = Query(14, ge=1, le=60), db: Session = Depends(get_db)):
    p = db.query(Product).filter(Product.sku == sku).first()
    if not p:
        raise HTTPException(404, "SKU not found")
    preds = train_forecast(db,p,horizon)
    return {"sku":p.sku,"name":p.name,"horizon":horizon,"forecast":preds}

@app.post("/api/retrain")
def retrain(db: Session = Depends(get_db)):
    # Forecasts are calculated on demand; this endpoint validates every SKU.
    results = []
    for p in db.query(Product).all():
        f = train_forecast(db,p,14)
        results.append({"sku":p.sku,"points":len(f)})
    return {"message":"Models refreshed successfully.","models":results}
