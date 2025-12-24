import pandas as pd
from database import engine, SessionLocal, Base
from models import ForexData
from sqlalchemy.orm import Session
import os
import time

def import_csv_to_db():
    # Create tables
    Base.metadata.create_all(bind=engine)
    
    csv_path = os.path.join('staging', 'datecorrected-raw-price.csv')
    if not os.path.exists(csv_path):
        print(f"Error: CSV file not found at {csv_path}")
        return

    print("Reading CSV...")
    df = pd.read_csv(csv_path)
    
    print("Processing data...")
    # Convert date to datetime objects
    df['Date'] = pd.to_datetime(df['Date'])
    
    # Create records list
    records = []
    total_rows = len(df)
    
    session = SessionLocal()
    try:
        # Check if data already exists to avoid duplicates (slower but safer) - 
        # For this initial bulk load, assuming empty or overwrite is okay?
        # Let's just truncate/drop first or assume empty?
        # The prompt implies moving to DB, so likely fresh start.
        # Let's check count first.
        count = session.query(ForexData).count()
        if count > 0:
            print(f"Database already has {count} records. Skipping import to avoid duplicates.")
            return

        print(f"Importing {total_rows} records...")
        
        # Batch insert for performance
        batch_size = 10000
        for i in range(0, total_rows, batch_size):
            batch = df.iloc[i:i+batch_size]
            objects = []
            for _, row in batch.iterrows():
                # Timestamp calculation
                ts = int(row['Date'].timestamp())
                
                record = ForexData(
                    date=row['Date'],
                    timestamp=ts,
                    bid_open=row['BidOpen'],
                    bid_high=row['BidHigh'],
                    bid_low=row['BidLow'],
                    bid_close=row['BidClose'],
                    ask_open=row['AskOpen'],
                    ask_high=row['AskHigh'],
                    ask_low=row['AskLow'],
                    ask_close=row['AskClose'],
                    volume=row['Volume']
                )
                objects.append(record)
            
            session.add_all(objects)
            session.commit()
            print(f"Imported {min(i+batch_size, total_rows)} / {total_rows}")
            
        print("Import completed successfully!")
        
    except Exception as e:
        print(f"Error importing data: {e}")
        session.rollback()
    finally:
        session.close()

if __name__ == "__main__":
    start_time = time.time()
    import_csv_to_db()
    print(f"Time taken: {time.time() - start_time:.2f} seconds")
