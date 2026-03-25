from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.analyzer import Analyzer

app = FastAPI(title="AEGIS API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
data_dir = os.path.join(BASE_DIR, "data")

# Initialize Analyzer (which loads and processes data)
analyzer = Analyzer(data_dir=data_dir, ddos_threshold=10)

@app.get("/")
def root():
    return {"status": "ok", "message": "AEGIS Backend is running."}

@app.get("/nodes")
def get_nodes():
    return analyzer.get_nodes()

@app.get("/heatmap")
def get_heatmap():
    return analyzer.get_heatmap_data()

@app.get("/schemas")
def get_schemas():
    return analyzer.get_schemas()

@app.get("/assets")
def get_assets():
    return analyzer.get_assets()

@app.get("/events")
def get_events(limit: int = 50):
    # Returns the latest raw event data for terminal stream
    # Specifically those with anomalies if possible, or just the stream
    data = analyzer.get_latest_data(limit=limit)
    return data
