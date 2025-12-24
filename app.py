from fastapi import FastAPI, Depends, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
import os
from database import get_db
from models import ForexData

app = FastAPI()

# Setup templates
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/api/data")
async def get_data(db: Session = Depends(get_db)):
    # Query database
    # Assuming we want all data for now, ordered by timestamp
    # Optimization: Select only necessary columns
    results = db.query(ForexData).order_by(ForexData.timestamp).all()
    
    # Format for chart
    chart_data = [
        {
            "time": row.timestamp,
            "open": row.bid_open,
            "high": row.bid_high,
            "low": row.bid_low,
            "close": row.bid_close
        }
        for row in results
    ]
        
    return chart_data

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
