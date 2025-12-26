from sqlalchemy import Column, Integer, Float, DateTime, BigInteger, String
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

class TradeDetail(Base):
    __tablename__ = "botcore_tradedetail"

    id = Column(BigInteger, primary_key=True)
    uuid = Column(String(36), unique=True, nullable=False)
    position_id = Column(BigInteger, nullable=False)
    position_type = Column(String(10), nullable=False)
    entry_price = Column(Float, nullable=False)
    exit_price = Column(Float, nullable=True)
    pips = Column(Float, nullable=True)
    status = Column(String(10), nullable=False)
    lot_size = Column(Float, nullable=False)
    opened_at = Column(DateTime, nullable=False)
    closed_at = Column(DateTime, nullable=True)
    segment_id = Column(BigInteger, nullable=True)
    trade_id = Column(BigInteger, nullable=False)
