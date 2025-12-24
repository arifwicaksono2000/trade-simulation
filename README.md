# Trade Simulation UI

A simple and efficient web application to visualize Forex trading data using Python (FastAPI) and TradingView Lightweight Charts.

## Features

- **Interactive Charting**: Visualize large datasets (e.g., 1-minute Forex candles) with zoom and pan capabilities.
- **Performance**: Renders 80,000+ data points smoothly.
- **Custom Interface**: Dark mode UI similar to professional trading platforms.
- **Zoom at Cursor**: Standard, intuitive chart navigation.

## Prerequisites

- Python 3.x
- Git

## Installation

1.  **Clone the repository** (if you haven't already):

    ```bash
    git clone https://github.com/arifwicaksono2000/trade-simulation.git
    cd trade-simulation
    ```

2.  **Create a Virtual Environment**:

    ```bash
    python -m venv venv
    ```

3.  **Activate the Virtual Environment**:

    - **Windows**:
      ```powershell
      .\venv\Scripts\Activate
      ```
    - **macOS/Linux**:
      ```bash
      source venv/bin/activate
      ```

4.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

1.  **Start the Server**:
    Ensure your virtual environment is active, then run:

    ```bash
    python app.py
    ```

    _(Or use `uvicorn app:app --reload` for development)_

2.  **View the App**:
    Open your browser and navigate to: [http://127.0.0.1:8000](http://127.0.0.1:8000)

## Project Structure

- `app.py`: Main FastAPI backend application.
- `database.py`: Database connection setup (MySQL ready).
- `templates/`: HTML frontend templates.
- `data/` & `staging/`: Directories for CSV data.
- `requirements.txt`: Python package dependencies.
