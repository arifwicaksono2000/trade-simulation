from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import pandas as pd
import json
import os

app = FastAPI()

# Setup templates
templates = Jinja2Templates(directory="templates")

# Path to CSV
CSV_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'staging', 'datecorrected-raw-price.csv')

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/api/data")
async def get_data():
    if not os.path.exists(CSV_PATH):
        return {"error": "CSV file not found"}
    
    # Read CSV
    df = pd.read_csv(CSV_PATH)
    
    # Parse Date
    df['Date'] = pd.to_datetime(df['Date'])
    
    # Optimized conversion for speed
    df['time'] = df['Date'].astype('int64') // 10**9 
    
    # Rename and select columns
    data = df[['time', 'BidOpen', 'BidHigh', 'BidLow', 'BidClose']].rename(columns={
        'BidOpen': 'open',
        'BidHigh': 'high',
        'BidLow': 'low',
        'BidClose': 'close'
    })
    
    chart_data = data.to_dict('records')
        
    return chart_data

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
