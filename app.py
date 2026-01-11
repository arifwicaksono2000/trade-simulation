from fastapi import FastAPI, Depends, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
import os
from datetime import timezone
from database import get_db
from models import ForexData, TradeDetail, Segment

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

@app.get("/api/trades")
async def get_trades(segment_id: int = None, db: Session = Depends(get_db)):
    query = db.query(TradeDetail)
    if segment_id:
        query = query.filter(TradeDetail.segment_id == segment_id)
        
    results = query.all()
    trades = [
        {
            "id": row.id,
            "position_id": row.position_id,
            "position_type": row.position_type,
            "entry_price": row.entry_price,
            "exit_price": row.exit_price,
            "lot_size": row.lot_size,
            "time": int(row.opened_at.replace(tzinfo=timezone.utc).timestamp()) if row.opened_at else None,
            "opened_at": row.opened_at.isoformat() if row.opened_at else None,
        }
        for row in results
    ]
    return trades

@app.get("/api/segments")
async def get_segments(db: Session = Depends(get_db)):
    results = db.query(Segment).order_by(Segment.opened_at.desc()).all()
    segments = [
        {
            "id": row.id,
            "uuid": row.uuid,
            "pair": row.pair,
            "status": row.status,
            "total_positions": row.total_positions,
            "total_balance": row.total_balance,
            "opened_at": row.opened_at.isoformat() if row.opened_at else None
        }
        for row in results
    ]
    return segments

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
