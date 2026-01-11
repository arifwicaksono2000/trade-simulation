from sqlalchemy import Column, Integer, Float, DateTime, BigInteger, String, ForeignKey, Numeric, Boolean, JSON
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

class Milestone(Base):
    __tablename__ = "botcore_milestone"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    starting_balance = Column(Numeric(15, 4), nullable=False)
    loss = Column(Numeric(15, 4), nullable=False)
    profit_goal = Column(Numeric(15, 4), nullable=False)
    lot_size = Column(Numeric(10, 4), nullable=False)
    ending_balance = Column(Numeric(15, 4), nullable=False)

class User(Base):
    __tablename__ = "auth_user"

    id = Column(Integer, primary_key=True, autoincrement=True)
    password = Column(String(128), nullable=False)
    last_login = Column(DateTime, nullable=True)
    is_superuser = Column(Boolean, nullable=False)
    username = Column(String(150), unique=True, nullable=False)
    first_name = Column(String(150), nullable=False)
    last_name = Column(String(150), nullable=False)
    email = Column(String(254), nullable=False)
    is_staff = Column(Boolean, nullable=False)
    is_active = Column(Boolean, nullable=False)
    date_joined = Column(DateTime, nullable=False)

class Subaccount(Base):
    __tablename__ = "botcore_subaccount"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    platform = Column(String(20), nullable=False)
    account_id = Column(String(50), unique=True, nullable=False)
    balance = Column(Numeric(15, 4), nullable=False)
    is_default = Column(Boolean, nullable=False)
    user_id = Column(Integer, ForeignKey("auth_user.id"), nullable=False)

class Segment(Base):
    __tablename__ = "botcore_segments"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    uuid = Column(String(36), unique=True, nullable=False)
    total_positions = Column(Integer, nullable=False)
    total_balance = Column(Numeric(15, 4), nullable=False)
    pair = Column(String(10), nullable=False)
    opened_at = Column(DateTime, nullable=False)
    closed_at = Column(DateTime, nullable=True)
    status = Column(String(10), nullable=False)
    is_pivot = Column(Boolean, nullable=False)
    subaccount_id = Column(BigInteger, ForeignKey("botcore_subaccount.id"), nullable=True)

class Trade(Base):
    __tablename__ = "botcore_trades"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    uuid = Column(String(36), unique=True, nullable=False)
    curr_active = Column(String(10), nullable=False)
    starting_balance = Column(Numeric(15, 4), nullable=False)
    profit_goal = Column(Numeric(15, 4), nullable=False)
    ending_balance = Column(Numeric(15, 4), nullable=True)
    opened_at = Column(DateTime, nullable=False)
    closed_at = Column(DateTime, nullable=True)
    status = Column(String(10), nullable=False)
    achieved_level_id = Column(BigInteger, ForeignKey("botcore_milestone.id"), nullable=True)
    current_level_id = Column(BigInteger, ForeignKey("botcore_milestone.id"), nullable=True)
    segment_id = Column(BigInteger, ForeignKey("botcore_segments.id"), nullable=True)

class TradeDetail(Base):
    __tablename__ = "botcore_tradedetail"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    uuid = Column(String(36), unique=True, nullable=False)
    position_id = Column(BigInteger, nullable=False)
    position_type = Column(String(10), nullable=False)
    entry_price = Column(Numeric(20, 10), nullable=False)
    exit_price = Column(Numeric(20, 10), nullable=True)
    pips = Column(Numeric(10, 2), nullable=True)
    status = Column(String(10), nullable=False)
    lot_size = Column(Numeric(10, 2), nullable=False)
    opened_at = Column(DateTime, nullable=False)
    closed_at = Column(DateTime, nullable=True)
    segment_id = Column(BigInteger, ForeignKey("botcore_segments.id"), nullable=True)
    trade_id = Column(BigInteger, ForeignKey("botcore_trades.id"), nullable=False)

class EventLog(Base):
    __tablename__ = "botcore_eventlog"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    event_type = Column(String(20), nullable=False)
    position_id = Column(BigInteger, nullable=False)
    details = Column(JSON, nullable=False)
    created_at = Column(DateTime, nullable=False)
    trade_id = Column(BigInteger, ForeignKey("botcore_trades.id"), nullable=False)
