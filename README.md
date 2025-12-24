# Forex Trading Simulation UI

A visual interface for simulating forex trading data, built with Python (FastAPI) and TradingView Lightweight Charts.

## Features

- **Interactive Chart**: Zoom, pan, and inspect forex candles (1-minute data).
- **High Performance**: Renders 80,000+ data points smoothly using Lightweight Charts.
- **Python Backend**: Built with FastAPI for easy extension.
- **Database Ready**: Prepared for MySQL integration.

## Project Structure

- `app.py`: Main backend application serving the API and HTML.
- `templates/index.html`: Frontend UI.
- `database.py`: MySQL connection setup (prepared).
- `requirements.txt`: Python dependencies.
- `venv/`: Virtual environment.

## How to Run

1. **Navigate to the directory**:

   ```powershell
   cd "C:\Users\arifw\Documents\Personal Documents\Endeavours\Investment\Forex\Programs\trade-simulation\ui_app"
   ```

2. **Activate the Virtual Environment**:

   ```powershell
   .\venv\Scripts\Activate
   ```

3. **Install Dependencies**:

   ```powershell
   pip install -r requirements.txt
   ```

4. **Run the Application**:

   ```powershell
   python app.py
   ```

   _Alternatively, for hot-reloading during development:_

   ```powershell
   uvicorn app:app --reload
   ```

5. **Open in Browser**:
   Go to [http://127.0.0.1:8000](http://127.0.0.1:8000)

## Controls

- **Scroll**: Zoom in/out (centers on cursor).
- **Drag**: Pan the chart.
- **Crosshair**: View price and time details.
