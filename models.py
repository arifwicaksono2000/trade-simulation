from sqlalchemy import Column, Integer, Float, DateTime, BigInteger
from database import Base

class ForexData(Base):
    __tablename__ = "forex_data"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime, index=True)
    timestamp = Column(BigInteger, index=True) # For faster charting
    bid_open = Column(Float)
    bid_high = Column(Float)
    bid_low = Column(Float)
    bid_close = Column(Float)
    ask_open = Column(Float)
    ask_high = Column(Float)
    ask_low = Column(Float)
    ask_close = Column(Float)
    volume = Column(Integer)
